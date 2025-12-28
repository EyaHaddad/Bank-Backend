"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useRouter } from "next/navigation"
import { useState, useEffect } from "react"
import { useToast } from "@/hooks/useToast"
import { Loader2 } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { logoutUser } from "@/services/auth.service"
import { getMyAccounts } from "@/services/accounts.service"
import { listBeneficiaries } from "@/services/beneficiaries.service"
import { createTransfer } from "@/services/transfers.service"
import type { Account } from "@/types/account"
import type { Beneficiary } from "@/types/beneficiary"
import type { TransferCreate } from "@/types/transfer"

export default function TransferPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [amount, setAmount] = useState("")
  const [beneficiaryId, setBeneficiaryId] = useState("")
  const [fromAccount, setFromAccount] = useState("")
  const [reference, setReference] = useState("")
  const [accounts, setAccounts] = useState<Account[]>([])
  const [beneficiaries, setBeneficiaries] = useState<Beneficiary[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

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

  const handleTransfer = () => {
    setShowConfirmation(true)
  }

  const confirmTransfer = async () => {
    try {
      setIsSubmitting(true)
      const transferData: TransferCreate = {
        sender_account_id: fromAccount,
        beneficiary_id: beneficiaryId,
        amount: parseFloat(amount),
        description: reference || undefined,
      }
      await createTransfer(transferData)
      toast({
        title: "Transfer successful",
        description: `$${amount} has been transferred successfully`,
      })
      setShowConfirmation(false)
      setAmount("")
      setBeneficiaryId("")
      setReference("")
      router.push("/client/transactions")
    } catch (error) {
      toast({
        title: "Transfer failed",
        description: "Unable to complete the transfer. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
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
          <p className="text-sm text-muted-foreground">Send money to your beneficiaries</p>
        </div>

        <div className="p-8">
          <div className="mx-auto max-w-2xl">
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

                <div className="flex gap-2">
                  <Button
                    onClick={handleTransfer}
                    disabled={!amount || !beneficiaryId || !fromAccount}
                    className="flex-1"
                  >
                    Transfer Money
                  </Button>
                  <Button variant="outline" onClick={() => router.push("/client")}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Dialog open={showConfirmation} onOpenChange={setShowConfirmation}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm Transfer</DialogTitle>
            <DialogDescription>Please review the transfer details before confirming</DialogDescription>
          </DialogHeader>
          <div className="space-y-3 py-4">
            <div className="flex justify-between">
              <span className="text-muted-foreground">From:</span>
              <span className="font-medium text-foreground">
                {accounts.find((a) => a.id === fromAccount)?.currency} Account (ID: {fromAccount.slice(0, 8)}...)
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">To:</span>
              <span className="font-medium text-foreground">
                {beneficiaries.find((b) => b.id === beneficiaryId)?.name}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Amount:</span>
              <span className="text-lg font-bold text-accent">${amount}</span>
            </div>
            {reference && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Reference:</span>
                <span className="font-medium text-foreground">{reference}</span>
              </div>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowConfirmation(false)}>
              Cancel
            </Button>
            <Button onClick={confirmTransfer} disabled={isSubmitting}>
              {isSubmitting ? "Processing..." : "Confirm Transfer"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
