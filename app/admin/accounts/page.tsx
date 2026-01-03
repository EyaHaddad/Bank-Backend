"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useRouter } from "next/navigation"
import { useState, useEffect } from "react"
import { useToast } from "@/hooks/useToast"
import { Search, MoreVertical, Loader2, CheckCircle, XCircle, Lock, Trash2, DollarSign } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { logoutUser } from "@/services/auth.service"
import { 
  listAllAccounts, 
  activateAccount, 
  blockAccount, 
  closeAccount, 
  deleteAccount,
  updateAccountBalance,
  type AdminAccount 
} from "@/services/admin.service"

export default function ManageAccountsPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [searchQuery, setSearchQuery] = useState("")
  const [accounts, setAccounts] = useState<AdminAccount[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Dialog states
  const [showBalanceDialog, setShowBalanceDialog] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedAccount, setSelectedAccount] = useState<AdminAccount | null>(null)
  const [newBalance, setNewBalance] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  const fetchAccounts = async () => {
    try {
      setIsLoading(true)
      const data = await listAllAccounts()
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

  const handleActivateAccount = async (account: AdminAccount) => {
    try {
      await activateAccount(account.id)
      toast({
        title: "Account activated",
        description: `Account for ${account.user_name} has been activated`,
      })
      fetchAccounts()
    } catch (err: any) {
      toast({
        title: "Error",
        description: err?.response?.data?.detail || "Failed to activate account",
        variant: "destructive",
      })
    }
  }

  const handleBlockAccount = async (account: AdminAccount) => {
    try {
      await blockAccount(account.id)
      toast({
        title: "Account blocked",
        description: `Account for ${account.user_name} has been blocked`,
        variant: "destructive",
      })
      fetchAccounts()
    } catch (err: any) {
      toast({
        title: "Error",
        description: err?.response?.data?.detail || "Failed to block account",
        variant: "destructive",
      })
    }
  }

  const handleCloseAccount = async (account: AdminAccount) => {
    try {
      await closeAccount(account.id)
      toast({
        title: "Account closed",
        description: `Account for ${account.user_name} has been permanently closed`,
        variant: "destructive",
      })
      fetchAccounts()
    } catch (err: any) {
      toast({
        title: "Error",
        description: err?.response?.data?.detail || "Failed to close account",
        variant: "destructive",
      })
    }
  }

  const handleDeleteAccount = async () => {
    if (!selectedAccount) return
    try {
      setIsSubmitting(true)
      await deleteAccount(selectedAccount.id)
      toast({
        title: "Account deleted",
        description: `Account for ${selectedAccount.user_name} has been permanently deleted`,
        variant: "destructive",
      })
      setShowDeleteDialog(false)
      setSelectedAccount(null)
      fetchAccounts()
    } catch (err: any) {
      toast({
        title: "Error",
        description: err?.response?.data?.detail || "Failed to delete account",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleUpdateBalance = async () => {
    if (!selectedAccount || !newBalance) return
    try {
      setIsSubmitting(true)
      await updateAccountBalance(selectedAccount.id, parseFloat(newBalance))
      toast({
        title: "Balance updated",
        description: `Account balance for ${selectedAccount.user_name} has been updated`,
      })
      setShowBalanceDialog(false)
      setSelectedAccount(null)
      setNewBalance("")
      fetchAccounts()
    } catch (err: any) {
      toast({
        title: "Error",
        description: err?.response?.data?.detail || "Failed to update balance",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const openBalanceDialog = (account: AdminAccount) => {
    setSelectedAccount(account)
    setNewBalance(account.balance.toString())
    setShowBalanceDialog(true)
  }

  const openDeleteDialog = (account: AdminAccount) => {
    setSelectedAccount(account)
    setShowDeleteDialog(true)
  }

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case "ACTIVE":
        return "default"
      case "BLOCKED":
        return "destructive"
      case "CLOSED":
        return "secondary"
      default:
        return "outline"
    }
  }

  const filteredAccounts = accounts.filter(
    (account) =>
      account.user_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      account.user_email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      account.id.includes(searchQuery),
  )

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-accent" />
      </div>
    )
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="admin" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Manage Accounts</h1>
              <p className="text-sm text-muted-foreground">View and manage all bank accounts</p>
            </div>
          </div>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-4 rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              {error}
            </div>
          )}

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>All Accounts</CardTitle>
                  <CardDescription>Total {filteredAccounts.length} accounts</CardDescription>
                </div>
                <div className="w-64">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search accounts..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Account ID</TableHead>
                    <TableHead>Client Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Currency</TableHead>
                    <TableHead>Balance</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredAccounts.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} className="text-center text-muted-foreground py-8">
                        No accounts found
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredAccounts.map((account) => (
                      <TableRow key={account.id}>
                        <TableCell className="font-mono font-medium">
                          {account.id.substring(0, 8)}...
                        </TableCell>
                        <TableCell>{account.user_name}</TableCell>
                        <TableCell>{account.user_email}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{account.currency}</Badge>
                        </TableCell>
                        <TableCell className="font-semibold">
                          ${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                        </TableCell>
                        <TableCell>
                          <Badge variant={getStatusBadgeVariant(account.status)}>
                            {account.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="sm">
                                <MoreVertical className="h-4 w-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem onClick={() => openBalanceDialog(account)}>
                                <DollarSign className="mr-2 h-4 w-4" />
                                Update Balance
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              {account.status !== "ACTIVE" && account.status !== "CLOSED" && (
                                <DropdownMenuItem onClick={() => handleActivateAccount(account)}>
                                  <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                                  Activate Account
                                </DropdownMenuItem>
                              )}
                              {account.status === "ACTIVE" && (
                                <DropdownMenuItem onClick={() => handleBlockAccount(account)}>
                                  <Lock className="mr-2 h-4 w-4 text-yellow-500" />
                                  Block Account
                                </DropdownMenuItem>
                              )}
                              {account.status !== "CLOSED" && (
                                <DropdownMenuItem onClick={() => handleCloseAccount(account)}>
                                  <XCircle className="mr-2 h-4 w-4 text-orange-500" />
                                  Close Account
                                </DropdownMenuItem>
                              )}
                              <DropdownMenuSeparator />
                              <DropdownMenuItem 
                                className="text-destructive"
                                onClick={() => openDeleteDialog(account)}
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Delete Account
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Update Balance Dialog */}
      <Dialog open={showBalanceDialog} onOpenChange={setShowBalanceDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Update Account Balance</DialogTitle>
            <DialogDescription>
              {selectedAccount && (
                <>Update balance for {selectedAccount.user_name}'s account</>
              )}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="newBalance">New Balance ({selectedAccount?.currency})</Label>
              <Input
                id="newBalance"
                type="number"
                min="0"
                step="0.01"
                placeholder="0.00"
                value={newBalance}
                onChange={(e) => setNewBalance(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowBalanceDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdateBalance} disabled={isSubmitting || !newBalance}>
              {isSubmitting ? "Updating..." : "Update Balance"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the account
              {selectedAccount && ` for ${selectedAccount.user_name}`}.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteAccount}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {isSubmitting ? "Deleting..." : "Delete Account"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
