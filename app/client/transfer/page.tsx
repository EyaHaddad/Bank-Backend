"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useRouter } from "next/navigation"
import { useState, useEffect, useRef } from "react"
import { useToast } from "@/hooks/useToast"
import { Loader2, Shield, ArrowLeft } from "lucide-react"
import { logoutUser } from "@/services/auth.service"
import { getMyAccounts } from "@/services/accounts.service"
import { listBeneficiaries } from "@/services/beneficiaries.service"
import { initiateTransfer, confirmTransfer } from "@/services/transfers.service"
import type { Account } from "@/types/account"
import type { Beneficiary } from "@/types/beneficiary"
import type { TransferInitiateRequest, TransferInitiateResponse } from "@/types/transfer"
import { AxiosError } from "axios"

export default function TransferPage() {
  const router = useRouter()
  const { toast } = useToast()
  
  // Form state
  const [amount, setAmount] = useState("")
  const [beneficiaryId, setBeneficiaryId] = useState("")
  const [fromAccount, setFromAccount] = useState("")
  const [reference, setReference] = useState("")
  const [accounts, setAccounts] = useState<Account[]>([])
  const [beneficiaries, setBeneficiaries] = useState<Beneficiary[]>([])
  const [isLoading, setIsLoading] = useState(true)
  
  // Transfer flow state
  const [step, setStep] = useState<'form' | 'otp'>('form')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [pendingTransfer, setPendingTransfer] = useState<TransferInitiateResponse | null>(null)
  
  // OTP state
  const [otpCode, setOtpCode] = useState(["", "", "", "", "", ""])
  const otpInputRefs = useRef<(HTMLInputElement | null)[]>([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        const [accountsData, beneficiariesData] = await Promise.all([
          getMyAccounts(),
          listBeneficiaries(),
        ])
        setAccounts(accountsData)
        setBeneficiaries(beneficiariesData.beneficiaries.filter((b: Beneficiary) => b.is_verified))
      } catch (error) {
        console.error("Failed to fetch data:", error)
        toast({
          title: "Error",
          description: "Failed to load accounts and beneficiaries",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [toast])

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  // Handle OTP input change
  const handleOtpChange = (index: number, value: string) => {
    if (value && !/^\d+$/.test(value)) return
    
    const newOtp = [...otpCode]
    newOtp[index] = value.slice(-1)
    setOtpCode(newOtp)
    
    if (value && index < 5) {
      otpInputRefs.current[index + 1]?.focus()
    }
  }

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !otpCode[index] && index > 0) {
      otpInputRefs.current[index - 1]?.focus()
    }
  }

  const handleOtpPaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text").slice(0, 6)
    if (!/^\d+$/.test(pastedData)) return
    
    const newOtp = [...otpCode]
    for (let i = 0; i < pastedData.length && i < 6; i++) {
      newOtp[i] = pastedData[i]
    }
    setOtpCode(newOtp)
    
    const nextEmpty = newOtp.findIndex(v => !v)
    otpInputRefs.current[nextEmpty === -1 ? 5 : nextEmpty]?.focus()
  }

  // Step 1: Initiate transfer (send OTP)
  const handleInitiateTransfer = async () => {
    try {
      setIsSubmitting(true)
      
      const transferData: TransferInitiateRequest = {
        sender_account_id: fromAccount,
        beneficiary_id: beneficiaryId,
        amount: parseFloat(amount),
        reference: reference || undefined,
      }
      
      const response = await initiateTransfer(transferData)
      setPendingTransfer(response)
      setStep('otp')
      
      toast({
        title: "OTP Sent",
        description: "A verification code has been sent to your email.",
      })
    } catch (error) {
      let errorMessage = "Failed to initiate transfer"
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      toast({
        title: "Transfer failed",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  // Step 2: Confirm transfer with OTP
  const handleConfirmTransfer = async () => {
    const code = otpCode.join("")
    if (code.length !== 6) {
      toast({
        title: "Invalid code",
        description: "Please enter the complete 6-digit code",
        variant: "destructive",
      })
      return
    }

    if (!pendingTransfer) return

    try {
      setIsSubmitting(true)
      
      await confirmTransfer(pendingTransfer.transfer_token, code)
      
      toast({
        title: "Transfer successful",
        description: `$${amount} has been transferred to ${pendingTransfer.beneficiary_name}`,
      })
      
      // Reset form
      setAmount("")
      setBeneficiaryId("")
      setFromAccount("")
      setReference("")
      setOtpCode(["", "", "", "", "", ""])
      setPendingTransfer(null)
      setStep('form')
      
      router.push("/client/transactions")
    } catch (error) {
      let errorMessage = "Failed to confirm transfer"
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      toast({
        title: "Verification failed",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleBackToForm = () => {
    setStep('form')
    setOtpCode(["", "", "", "", "", ""])
    setPendingTransfer(null)
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-accent" />
      </div>
    )
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Transfer Money</h1>
          <p className="text-sm text-muted-foreground">Send money to your beneficiaries securely</p>
        </div>

        <div className="p-8">
          <div className="mx-auto max-w-2xl">
            {step === 'form' ? (
              <Card>
                <CardHeader>
                  <CardTitle>New Transfer</CardTitle>
                  <CardDescription>Fill in the details to transfer money</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="fromAccount">From Account</Label>
                    <Select value={fromAccount} onValueChange={setFromAccount}>
                      <SelectTrigger id="fromAccount">
                        <SelectValue placeholder="Select source account" />
                      </SelectTrigger>
                      <SelectContent>
                        {accounts.map((account) => (
                          <SelectItem key={account.id} value={account.id}>
                            {account.currency} Account (ID: {account.id.slice(0, 8)}...) - {account.currency} {account.balance.toLocaleString()}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="beneficiary">To Beneficiary</Label>
                    <Select value={beneficiaryId} onValueChange={setBeneficiaryId}>
                      <SelectTrigger id="beneficiary">
                        <SelectValue placeholder="Select beneficiary" />
                      </SelectTrigger>
                      <SelectContent>
                        {beneficiaries.length === 0 ? (
                          <SelectItem value="no-beneficiaries" disabled>No verified beneficiaries</SelectItem>
                        ) : (
                          beneficiaries.map((ben) => (
                            <SelectItem key={ben.id} value={ben.id}>
                              {ben.name} - ****{ben.iban.slice(-4)}
                            </SelectItem>
                          ))
                        )}
                      </SelectContent>
                    </Select>
                    <p className="text-xs text-muted-foreground">
                      Don't see your beneficiary?{" "}
                      <button
                        onClick={() => router.push("/client/beneficiaries")}
                        className="text-accent hover:underline"
                      >
                        Add new beneficiary
                      </button>
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="amount">Amount</Label>
                    <div className="relative">
                      <span className="absolute left-3 top-3 text-muted-foreground">$</span>
                      <Input
                        id="amount"
                        type="number"
                        placeholder="0.00"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="pl-7"
                        min="0"
                        step="0.01"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="reference">Reference (Optional)</Label>
                    <Input
                      id="reference"
                      placeholder="Payment description"
                      value={reference}
                      onChange={(e) => setReference(e.target.value)}
                    />
                  </div>

                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <h3 className="mb-2 font-semibold text-foreground">Transfer Summary</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Amount:</span>
                        <span className="font-medium text-foreground">${amount || "0.00"}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Transfer Fee:</span>
                        <span className="font-medium text-foreground">$0.00</span>
                      </div>
                      <div className="flex justify-between border-t border-border pt-2">
                        <span className="font-semibold text-foreground">Total:</span>
                        <span className="font-semibold text-foreground">${amount || "0.00"}</span>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-lg border border-accent/30 bg-accent/5 p-4">
                    <div className="flex items-center gap-2 text-accent">
                      <Shield className="h-5 w-5" />
                      <span className="font-medium">Secure Transfer</span>
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">
                      For your security, you will receive an OTP code via email to confirm this transfer.
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      onClick={handleInitiateTransfer}
                      disabled={!amount || !beneficiaryId || !fromAccount || isSubmitting}
                      className="flex-1"
                    >
                      {isSubmitting ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Sending OTP...
                        </>
                      ) : (
                        "Continue to Verification"
                      )}
                    </Button>
                    <Button variant="outline" onClick={() => router.push("/client")}>
                      Cancel
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={handleBackToForm}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      <ArrowLeft className="h-5 w-5" />
                    </button>
                    <div>
                      <CardTitle>Verify Transfer</CardTitle>
                      <CardDescription>Enter the OTP sent to your email</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Transfer Summary */}
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <h3 className="mb-3 font-semibold text-foreground">Transfer Details</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">To:</span>
                        <span className="font-medium text-foreground">{pendingTransfer?.beneficiary_name}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Amount:</span>
                        <span className="text-lg font-bold text-accent">${pendingTransfer?.amount}</span>
                      </div>
                    </div>
                  </div>

                  {/* OTP Input */}
                  <div className="space-y-4">
                    <Label className="text-center block">Enter Verification Code</Label>
                    <div className="flex justify-center gap-2" onPaste={handleOtpPaste}>
                      {otpCode.map((digit, index) => (
                        <Input
                          key={index}
                          ref={(el) => { otpInputRefs.current[index] = el }}
                          type="text"
                          inputMode="numeric"
                          maxLength={1}
                          value={digit}
                          onChange={(e) => handleOtpChange(index, e.target.value)}
                          onKeyDown={(e) => handleOtpKeyDown(index, e)}
                          className="h-14 w-12 text-center text-2xl font-bold"
                        />
                      ))}
                    </div>
                    <p className="text-center text-sm text-muted-foreground">
                      Code expires at {pendingTransfer && new Date(pendingTransfer.expires_at).toLocaleTimeString()}
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      onClick={handleConfirmTransfer}
                      disabled={otpCode.join("").length !== 6 || isSubmitting}
                      className="flex-1"
                    >
                      {isSubmitting ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Processing...
                        </>
                      ) : (
                        "Confirm Transfer"
                      )}
                    </Button>
                    <Button variant="outline" onClick={handleBackToForm}>
                      Cancel
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
