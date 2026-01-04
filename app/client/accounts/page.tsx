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
import { Wallet, ArrowLeftRight, Loader2, Landmark, PiggyBank } from "lucide-react"
import { getMyAccounts, transferBetweenAccounts } from "@/services/accounts.service"
import { logoutUser } from "@/services/auth.service"
import type { Account } from "@/types/account"

export default function ClientAccountsPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Dialog states
  const [showTransferDialog, setShowTransferDialog] = useState(false)
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  // Form states
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
              <p className="text-sm text-muted-foreground">View your bank accounts</p>
            </div>
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
                    {totalBalance.toLocaleString("fr-TN", { minimumFractionDigits: 2 })} TND
                  </p>
                </div>
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <Landmark className="mb-2 h-5 w-5 text-accent" />
                  <p className="text-sm font-medium text-muted-foreground">Comptes Courants</p>
                  <p className="text-2xl font-bold text-foreground">
                    {accounts.filter(a => a.account_type === "COURANT").length}
                  </p>
                </div>
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <PiggyBank className="mb-2 h-5 w-5 text-accent" />
                  <p className="text-sm font-medium text-muted-foreground">Comptes Épargne</p>
                  <p className="text-2xl font-bold text-foreground">
                    {accounts.filter(a => a.account_type === "EPARGNE").length}
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
                      <CardTitle className="text-lg flex items-center gap-2">
                        {account.account_type === "EPARGNE" ? (
                          <PiggyBank className="h-5 w-5 text-green-500" />
                        ) : (
                          <Landmark className="h-5 w-5 text-blue-500" />
                        )}
                        {account.account_type === "EPARGNE" ? "Compte Épargne" : "Compte Courant"}
                      </CardTitle>
                      <Badge variant={account.account_type === "EPARGNE" ? "secondary" : "outline"}>
                        {account.currency}
                      </Badge>
                    </div>
                    <CardDescription>ID: {account.id.substring(0, 8)}...</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="mb-2 text-3xl font-bold text-foreground">
                      {account.balance.toLocaleString("fr-TN", { minimumFractionDigits: 2 })} TND
                    </p>
                    <Badge variant={account.status === "ACTIVE" ? "default" : "destructive"} className="mb-4">
                      {account.status}
                    </Badge>
                    <div className="flex flex-wrap gap-2">
                      {accounts.length > 1 && account.status === "ACTIVE" && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => openTransferDialog(account)}
                        >
                          <ArrowLeftRight className="mr-1 h-4 w-4" />
                          Transférer
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

      {/* Transfer Dialog */}
      <Dialog open={showTransferDialog} onOpenChange={setShowTransferDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Transfert Entre Comptes</DialogTitle>
            <DialogDescription>
              {selectedAccount && (
                <>Solde actuel: {selectedAccount.balance.toFixed(2)} {selectedAccount.currency}</>
              )}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="amount">Montant</Label>
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
              <Label htmlFor="targetAccount">Transférer vers</Label>
              <Select value={targetAccountId} onValueChange={setTargetAccountId}>
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner un compte" />
                </SelectTrigger>
                <SelectContent>
                  {accounts
                    .filter((acc) => acc.id !== selectedAccount?.id && acc.status === "ACTIVE")
                    .map((acc) => (
                      <SelectItem key={acc.id} value={acc.id}>
                        {acc.account_type === "EPARGNE" ? "Épargne" : "Courant"} - {acc.balance.toFixed(2)} TND ({acc.id.substring(0, 8)}...)
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowTransferDialog(false)}>
              Annuler
            </Button>
            <Button
              onClick={handleTransfer}
              disabled={isSubmitting || !transferAmount || !targetAccountId}
            >
              {isSubmitting ? "En cours..." : "Confirmer le Transfert"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
