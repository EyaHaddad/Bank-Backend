"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { useToast } from "@/hooks/use-toast"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export default function TransferPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [amount, setAmount] = useState("")
  const [beneficiary, setBeneficiary] = useState("")
  const [fromAccount, setFromAccount] = useState("")
  const [reference, setReference] = useState("")

  const handleLogout = () => {
    router.push("/")
  }

  const handleTransfer = () => {
    setShowConfirmation(true)
  }

  const confirmTransfer = () => {
    toast({
      title: "Transfer successful",
      description: `$${amount} has been transferred successfully`,
    })
    setShowConfirmation(false)
    setAmount("")
    setBeneficiary("")
    setReference("")
  }

  const beneficiaries = [
    { id: "1", name: "John Smith", account: "****1234" },
    { id: "2", name: "Jane Doe", account: "****5678" },
    { id: "3", name: "Mike Johnson", account: "****9012" },
  ]

  const accounts = [
    { id: "1", name: "Main Checking (****1234)", balance: 12450.75 },
    { id: "2", name: "Savings Account (****5678)", balance: 28750.0 },
  ]

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
                          {account.name} - ${account.balance.toLocaleString()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="beneficiary">To Beneficiary</Label>
                  <Select value={beneficiary} onValueChange={setBeneficiary}>
                    <SelectTrigger id="beneficiary">
                      <SelectValue placeholder="Select beneficiary" />
                    </SelectTrigger>
                    <SelectContent>
                      {beneficiaries.map((ben) => (
                        <SelectItem key={ben.id} value={ben.id}>
                          {ben.name} - {ben.account}
                        </SelectItem>
                      ))}
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
                    disabled={!amount || !beneficiary || !fromAccount}
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
              <span className="font-medium text-foreground">{accounts.find((a) => a.id === fromAccount)?.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">To:</span>
              <span className="font-medium text-foreground">
                {beneficiaries.find((b) => b.id === beneficiary)?.name}
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
            <Button onClick={confirmTransfer}>Confirm Transfer</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
