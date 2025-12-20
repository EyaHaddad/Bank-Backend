"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { Search, Plus, MoreVertical } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

export default function ManageAccountsPage() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")

  const handleLogout = () => {
    router.push("/")
  }

  const accounts = [
    {
      id: 1,
      accountNumber: "****1234",
      clientName: "John Smith",
      type: "Checking",
      balance: 12450.75,
      status: "active",
      openDate: "2024-01-15",
    },
    {
      id: 2,
      accountNumber: "****5678",
      clientName: "John Smith",
      type: "Savings",
      balance: 28750.0,
      status: "active",
      openDate: "2024-01-15",
    },
    {
      id: 3,
      accountNumber: "****2345",
      clientName: "Jane Doe",
      type: "Checking",
      balance: 15500.0,
      status: "active",
      openDate: "2024-02-20",
    },
    {
      id: 4,
      accountNumber: "****6789",
      clientName: "Mike Johnson",
      type: "Investment",
      balance: 45250.5,
      status: "active",
      openDate: "2023-11-10",
    },
    {
      id: 5,
      accountNumber: "****3456",
      clientName: "Sarah Williams",
      type: "Savings",
      balance: 5200.0,
      status: "frozen",
      openDate: "2024-03-05",
    },
  ]

  const filteredAccounts = accounts.filter(
    (account) =>
      account.clientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      account.accountNumber.includes(searchQuery),
  )

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
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              New Account
            </Button>
          </div>
        </div>

        <div className="p-8">
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
                    <TableHead>Account Number</TableHead>
                    <TableHead>Client Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Balance</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Open Date</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredAccounts.map((account) => (
                    <TableRow key={account.id}>
                      <TableCell className="font-mono font-medium">{account.accountNumber}</TableCell>
                      <TableCell>{account.clientName}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{account.type}</Badge>
                      </TableCell>
                      <TableCell className="font-semibold">${account.balance.toLocaleString()}</TableCell>
                      <TableCell>
                        <Badge variant={account.status === "active" ? "default" : "destructive"}>
                          {account.status}
                        </Badge>
                      </TableCell>
                      <TableCell>{account.openDate}</TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>View Details</DropdownMenuItem>
                            <DropdownMenuItem>Transaction History</DropdownMenuItem>
                            <DropdownMenuItem>Edit Account</DropdownMenuItem>
                            <DropdownMenuItem className="text-destructive">Freeze Account</DropdownMenuItem>
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
    </div>
  )
}
