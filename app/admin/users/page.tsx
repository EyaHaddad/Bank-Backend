"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { useState, useEffect } from "react"
import { useToast } from "@/hooks/useToast"
import { Search, Edit, Trash2, MoreVertical, Shield, Loader2, UserCheck, UserX, Wallet, PlusCircle } from "lucide-react"
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { logoutUser } from "@/services/auth.service"
import { listUsers, updateUser } from "@/services/users.service"
import { 
  promoteUserToAdmin, 
  demoteAdminToUser, 
  activateUser, 
  deactivateUser, 
  adminDeleteUser,
  createAccountForUser,
  type AdminAccountCreate
} from "@/services/admin.service"
import type { User } from "@/types/user"
import type { AccountType } from "@/types/account"

export default function ManageClientsPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [showAddAccountDialog, setShowAddAccountDialog] = useState(false)
  const [showEditDialog, setShowEditDialog] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  
  // Form state for adding account
  const [initialBalance, setInitialBalance] = useState("")
  const [accountType, setAccountType] = useState<AccountType>("COURANT")
  
  // Form state for editing user
  const [editFirstName, setEditFirstName] = useState("")
  const [editLastName, setEditLastName] = useState("")

  const fetchUsers = async () => {
    try {
      setIsLoading(true)
      const data = await listUsers()
      setUsers(data || [])
    } catch (error) {
      console.error("Failed to fetch users:", error)
      toast({
        title: "Error",
        description: "Failed to load users",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  const handleAddAccount = async () => {
    if (!selectedUser) return
    try {
      setIsSubmitting(true)
      const accountData: AdminAccountCreate = {
        user_id: selectedUser.id,
        initial_balance: parseFloat(initialBalance) || 0,
        account_type: accountType,
      }
      await createAccountForUser(accountData)
      toast({
        title: "Account created",
        description: `New ${accountType.toLowerCase()} account created for ${selectedUser.firstname} ${selectedUser.lastname}`,
      })
      setShowAddAccountDialog(false)
      resetAccountForm()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to create account",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteUser = async () => {
    if (!selectedUser) return
    try {
      setIsSubmitting(true)
      await adminDeleteUser(selectedUser.id)
      toast({
        title: "User deleted",
        description: `${selectedUser.firstname} ${selectedUser.lastname} has been removed`,
        variant: "destructive",
      })
      setShowDeleteDialog(false)
      setSelectedUser(null)
      fetchUsers()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to delete user",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const openDeleteDialog = (user: User) => {
    setSelectedUser(user)
    setShowDeleteDialog(true)
  }

  const openEditDialog = (user: User) => {
    setSelectedUser(user)
    setEditFirstName(user.firstname)
    setEditLastName(user.lastname)
    setShowEditDialog(true)
  }

  const openAddAccountDialog = (user: User) => {
    setSelectedUser(user)
    setInitialBalance("")
    setAccountType("COURANT")
    setShowAddAccountDialog(true)
  }

  const handleEditUser = async () => {
    if (!selectedUser) return
    try {
      setIsSubmitting(true)
      await updateUser(selectedUser.id, {
        firstname: editFirstName,
        lastname: editLastName,
      })
      toast({
        title: "User updated",
        description: `${editFirstName} ${editLastName}'s profile has been updated`,
      })
      setShowEditDialog(false)
      setSelectedUser(null)
      fetchUsers()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to update user",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleActivateUser = async (user: User) => {
    try {
      await activateUser(user.id)
      toast({
        title: "User activated",
        description: `${user.firstname} ${user.lastname}'s account has been activated`,
      })
      fetchUsers()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to activate user",
        variant: "destructive",
      })
    }
  }

  const handleDeactivateUser = async (user: User) => {
    try {
      await deactivateUser(user.id)
      toast({
        title: "User deactivated",
        description: `${user.firstname} ${user.lastname}'s account has been deactivated`,
        variant: "destructive",
      })
      fetchUsers()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to deactivate user",
        variant: "destructive",
      })
    }
  }

  const handlePromoteUser = async (user: User) => {
    try {
      await promoteUserToAdmin(user.id)
      toast({
        title: "User promoted",
        description: `${user.firstname} ${user.lastname} is now an admin`,
      })
      fetchUsers()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to promote user",
        variant: "destructive",
      })
    }
  }

  const handleDemoteUser = async (user: User) => {
    try {
      await demoteAdminToUser(user.id)
      toast({
        title: "Admin demoted",
        description: `${user.firstname} ${user.lastname} is now a regular user`,
      })
      fetchUsers()
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.response?.data?.detail || "Failed to demote admin",
        variant: "destructive",
      })
    }
  }

  const resetAccountForm = () => {
    setInitialBalance("")
    setAccountType("COURANT")
    setSelectedUser(null)
  }

  const filteredUsers = users.filter((user) =>
    `${user.firstname} ${user.lastname}`.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.toLowerCase())
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
              <h1 className="text-2xl font-bold text-foreground">Manage Users</h1>
              <p className="text-sm text-muted-foreground">View users and manage their bank accounts</p>
            </div>
          </div>
        </div>

        <div className="p-8">
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>All Users</CardTitle>
                  <CardDescription>Total {filteredUsers.length} users</CardDescription>
                </div>
                <div className="w-64">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search users..."
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
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Phone</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Joined</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell className="font-medium">{user.firstname} {user.lastname}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>{user.phone || "N/A"}</TableCell>
                      <TableCell>
                        <Badge variant={user.role === "admin" ? "default" : "secondary"}>{user.role}</Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={user.is_active ? "default" : "destructive"}>
                          {user.is_active ? "active" : "inactive"}
                        </Badge>
                      </TableCell>
                      <TableCell>{new Date(user.created_at).toLocaleDateString()}</TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            {user.role !== "admin" && (
                              <>
                                <DropdownMenuItem onClick={() => openAddAccountDialog(user)}>
                                  <PlusCircle className="mr-2 h-4 w-4 text-green-500" />
                                  Add Bank Account
                                </DropdownMenuItem>
                                <DropdownMenuSeparator />
                              </>
                            )}
                            <DropdownMenuItem onClick={() => openEditDialog(user)}>
                              <Edit className="mr-2 h-4 w-4" />
                              Edit User
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            {user.is_active ? (
                              <DropdownMenuItem onClick={() => handleDeactivateUser(user)}>
                                <UserX className="mr-2 h-4 w-4 text-yellow-500" />
                                Deactivate User
                              </DropdownMenuItem>
                            ) : (
                              <DropdownMenuItem onClick={() => handleActivateUser(user)}>
                                <UserCheck className="mr-2 h-4 w-4 text-green-500" />
                                Activate User
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuSeparator />
                            {user.role === "user" ? (
                              <DropdownMenuItem onClick={() => handlePromoteUser(user)}>
                                <Shield className="mr-2 h-4 w-4" />
                                Promote to Admin
                              </DropdownMenuItem>
                            ) : (
                              <DropdownMenuItem onClick={() => handleDemoteUser(user)}>
                                <Shield className="mr-2 h-4 w-4" />
                                Demote to User
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              className="text-destructive"
                              onClick={() => openDeleteDialog(user)}
                            >
                              <Trash2 className="mr-2 h-4 w-4" />
                              Delete User
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Add Bank Account Dialog */}
      <Dialog open={showAddAccountDialog} onOpenChange={setShowAddAccountDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create Bank Account</DialogTitle>
            <DialogDescription>
              {selectedUser && `Create a new bank account for ${selectedUser.firstname} ${selectedUser.lastname}`}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="accountType">Account Type</Label>
              <Select value={accountType} onValueChange={(value: AccountType) => setAccountType(value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select account type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="COURANT">
                    <div className="flex items-center">
                      <Wallet className="mr-2 h-4 w-4" />
                      Compte Courant
                    </div>
                  </SelectItem>
                  <SelectItem value="EPARGNE">
                    <div className="flex items-center">
                      <Wallet className="mr-2 h-4 w-4" />
                      Compte Épargne
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="initialBalance">Initial Balance (TND)</Label>
              <Input
                id="initialBalance"
                type="number"
                placeholder="0.00"
                min="0"
                step="0.01"
                value={initialBalance}
                onChange={(e) => setInitialBalance(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddAccountDialog(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleAddAccount}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Creating..." : "Create Account"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit User Dialog */}
      <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit User</DialogTitle>
            <DialogDescription>
              {selectedUser && `Update ${selectedUser.firstname} ${selectedUser.lastname}'s profile`}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="editFirstName">First Name</Label>
                <Input
                  id="editFirstName"
                  placeholder="John"
                  value={editFirstName}
                  onChange={(e) => setEditFirstName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="editLastName">Last Name</Label>
                <Input
                  id="editLastName"
                  placeholder="Doe"
                  value={editLastName}
                  onChange={(e) => setEditLastName(e.target.value)}
                />
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowEditDialog(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleEditUser}
              disabled={isSubmitting || !editFirstName || !editLastName}
            >
              {isSubmitting ? "Saving..." : "Save Changes"}
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
              This action cannot be undone. This will permanently delete
              {selectedUser && ` ${selectedUser.firstname} ${selectedUser.lastname}`}'s account and all associated data.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteUser}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {isSubmitting ? "Deleting..." : "Delete User"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
