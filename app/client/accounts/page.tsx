"use client"

import { useEffect, useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/useToast"
import { Plus, Wallet, ArrowLeftRight, Loader2 } from "lucide-react"
import { getMyAccounts, createAccount, transferBetweenAccounts } from "@/services/accounts.service"
import { logoutUser } from "@/services/auth.service"
import type { Account } from "@/types/account"

export default function ClientAccountsPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Dialog states
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [showTransferDialog, setShowTransferDialog] = useState(false)
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  // Form states
  const [newAccountCurrency, setNewAccountCurrency] = useState("USD")
  const [initialBalance, setInitialBalance] = useState("")
  const [transferAmount, setTransferAmount] = useState("")
  const [targetAccountId, setTargetAccountId] = useState("")

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  const fetchAccounts = async () => {
    try {
      setIsLoading(true)
      const data = await getMyAccounts()
      setAccounts(data || [])
    } catch (err) {
      console.error("Failed to fetch accounts:", err)
      setError("Failed to load accounts")
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchAccounts()
  }, [])

  const handleCreateAccount = async () => {
    try {
      setIsSubmitting(true)
      await createAccount({
        currency: newAccountCurrency,
        initial_balance: initialBalance ? parseFloat(initialBalance) : 0,
      })
      toast({
        title: "Account created",
        description: "Your new account has been created successfully",
      })
      setShowCreateDialog(false)
      setNewAccountCurrency("USD")
      setInitialBalance("")
      fetchAccounts()
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to create account",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const openTransferDialog = (account: Account) => {
    setSelectedAccount(account)
    setTransferAmount("")
    setTargetAccountId("")
    setShowTransferDialog(true)
  }

  const handleTransfer = async () => {
    if (!selectedAccount || !transferAmount || !targetAccountId) return

    try {
      setIsSubmitting(true)
      const amount = parseFloat(transferAmount)

      await transferBetweenAccounts(selectedAccount.id, {
        target_account_id: targetAccountId,
        amount,
      })
      toast({
        title: "Transfer successful",
        description: `$${amount.toFixed(2)} has been transferred`,
      })

      setShowTransferDialog(false)
      fetchAccounts()
    } catch (err: any) {
      toast({
        title: "Error",
        description: err?.response?.data?.detail || "Transfer failed",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0)

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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">My Accounts</h1>
              <p className="text-sm text-muted-foreground">Manage your bank accounts</p>
            </div>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="mr-2 h-4 w-4" />
              New Account
            </Button>
          </div>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-4 rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              {error}
            </div>
          )}

          {/* Summary Card */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Account Summary</CardTitle>
              <CardDescription>Overview of all your accounts</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <Wallet className="mb-2 h-5 w-5 text-accent" />
                  <p className="text-sm font-medium text-muted-foreground">Total Balance</p>
                  <p className="text-2xl font-bold text-foreground">
                    ${totalBalance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                  </p>
                </div>
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <p className="text-sm font-medium text-muted-foreground">Total Accounts</p>
                  <p className="text-2xl font-bold text-foreground">{accounts.length}</p>
                </div>
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <p className="text-sm font-medium text-muted-foreground">Currencies</p>
                  <p className="text-2xl font-bold text-foreground">
                    {[...new Set(accounts.map(a => a.currency))].join(", ") || "N/A"}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Accounts List */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {accounts.length === 0 ? (
              <Card className="col-span-full">
                <CardContent className="py-8 text-center">
                  <p className="text-muted-foreground">No accounts found. Create your first account!</p>
                </CardContent>
              </Card>
            ) : (
              accounts.map((account) => (
                <Card key={account.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">Account</CardTitle>
                      <Badge variant="outline">{account.currency}</Badge>
                    </div>
                    <CardDescription>ID: {account.id.substring(0, 8)}...</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="mb-4 text-3xl font-bold text-foreground">
                      ${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {accounts.length > 1 && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => openTransferDialog(account)}
                        >
                          <ArrowLeftRight className="mr-1 h-4 w-4" />
                          Transfer
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </main>

      {/* Create Account Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Account</DialogTitle>
            <DialogDescription>Set up a new bank account</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="currency">Currency</Label>
              <Select value={newAccountCurrency} onValueChange={setNewAccountCurrency}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="USD">USD - US Dollar</SelectItem>
                  <SelectItem value="EUR">EUR - Euro</SelectItem>
                  <SelectItem value="GBP">GBP - British Pound</SelectItem>
                  <SelectItem value="MAD">MAD - Moroccan Dirham</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="initialBalance">Initial Balance (Optional)</Label>
              <Input
                id="initialBalance"
                type="number"
                min="0"
                step="0.01"
                placeholder="0.00"
                value={initialBalance}
                onChange={(e) => setInitialBalance(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreateAccount} disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create Account"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Transfer Dialog */}
      <Dialog open={showTransferDialog} onOpenChange={setShowTransferDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Transfer Between Accounts</DialogTitle>
            <DialogDescription>
              {selectedAccount && (
                <>Current balance: ${selectedAccount.balance.toFixed(2)} {selectedAccount.currency}</>
              )}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="amount">Amount</Label>
              <Input
                id="amount"
                type="number"
                min="0.01"
                step="0.01"
                placeholder="0.00"
                value={transferAmount}
                onChange={(e) => setTransferAmount(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="targetAccount">Transfer To</Label>
              <Select value={targetAccountId} onValueChange={setTargetAccountId}>
                <SelectTrigger>
                  <SelectValue placeholder="Select target account" />
                </SelectTrigger>
                <SelectContent>
                  {accounts
                    .filter((acc) => acc.id !== selectedAccount?.id)
                    .map((acc) => (
                      <SelectItem key={acc.id} value={acc.id}>
                        {acc.currency} - ${acc.balance.toFixed(2)} ({acc.id.substring(0, 8)}...)
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowTransferDialog(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleTransfer}
              disabled={isSubmitting || !transferAmount || !targetAccountId}
            >
              {isSubmitting ? "Processing..." : "Confirm Transfer"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
