"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { ArrowUpRight, ArrowDownRight, Search, Download } from "lucide-react"

export default function TransactionsPage() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")
  const [filterType, setFilterType] = useState("all")
  const [filterDate, setFilterDate] = useState("all")

  const handleLogout = () => {
    router.push("/")
  }

  const transactions = [
    {
      id: 1,
      description: "Salary Deposit",
      amount: 5000.0,
      type: "credit",
      date: "2025-01-15",
      status: "completed",
      account: "Main Checking",
      category: "Income",
    },
    {
      id: 2,
      description: "Grocery Store",
      amount: -125.5,
      type: "debit",
      date: "2025-01-14",
      status: "completed",
      account: "Main Checking",
      category: "Shopping",
    },
    {
      id: 3,
      description: "Transfer to John Doe",
      amount: -500.0,
      type: "debit",
      date: "2025-01-13",
      status: "completed",
      account: "Main Checking",
      category: "Transfer",
    },
    {
      id: 4,
      description: "Restaurant",
      amount: -75.25,
      type: "debit",
      date: "2025-01-12",
      status: "completed",
      account: "Main Checking",
      category: "Dining",
    },
    {
      id: 5,
      description: "Investment Return",
      amount: 250.0,
      type: "credit",
      date: "2025-01-11",
      status: "completed",
      account: "Investment",
      category: "Income",
    },
    {
      id: 6,
      description: "Utility Bill Payment",
      amount: -150.0,
      type: "debit",
      date: "2025-01-10",
      status: "completed",
      account: "Main Checking",
      category: "Bills",
    },
    {
      id: 7,
      description: "Online Shopping",
      amount: -89.99,
      type: "debit",
      date: "2025-01-09",
      status: "completed",
      account: "Main Checking",
      category: "Shopping",
    },
    {
      id: 8,
      description: "Freelance Payment",
      amount: 1200.0,
      type: "credit",
      date: "2025-01-08",
      status: "completed",
      account: "Main Checking",
      category: "Income",
    },
    {
      id: 9,
      description: "Gas Station",
      amount: -45.0,
      type: "debit",
      date: "2025-01-07",
      status: "completed",
      account: "Main Checking",
      category: "Transport",
    },
    {
      id: 10,
      description: "Pending Transfer",
      amount: -200.0,
      type: "debit",
      date: "2025-01-16",
      status: "pending",
      account: "Main Checking",
      category: "Transfer",
    },
  ]

  const filteredTransactions = transactions.filter((transaction) => {
    const matchesSearch = transaction.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesType = filterType === "all" || transaction.type === filterType
    return matchesSearch && matchesType
  })

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Transaction History</h1>
              <p className="text-sm text-muted-foreground">View and filter your transactions</p>
            </div>
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
          </div>
        </div>

        <div className="p-8">
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Filters</CardTitle>
              <CardDescription>Search and filter your transactions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="search">Search</Label>
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="search"
                      placeholder="Search transactions..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="type">Transaction Type</Label>
                  <Select value={filterType} onValueChange={setFilterType}>
                    <SelectTrigger id="type">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Types</SelectItem>
                      <SelectItem value="credit">Credits</SelectItem>
                      <SelectItem value="debit">Debits</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date">Date Range</Label>
                  <Select value={filterDate} onValueChange={setFilterDate}>
                    <SelectTrigger id="date">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Time</SelectItem>
                      <SelectItem value="today">Today</SelectItem>
                      <SelectItem value="week">This Week</SelectItem>
                      <SelectItem value="month">This Month</SelectItem>
                      <SelectItem value="year">This Year</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>All Transactions</CardTitle>
              <CardDescription>Showing {filteredTransactions.length} transactions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredTransactions.map((transaction) => (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0"
                  >
                    <div className="flex items-center gap-4">
                      <div
                        className={`flex h-12 w-12 items-center justify-center rounded-full ${
                          transaction.type === "credit" ? "bg-accent/10" : "bg-muted"
                        }`}
                      >
                        {transaction.type === "credit" ? (
                          <ArrowDownRight className="h-6 w-6 text-accent" />
                        ) : (
                          <ArrowUpRight className="h-6 w-6 text-foreground" />
                        )}
                      </div>
                      <div>
                        <p className="font-medium text-foreground">{transaction.description}</p>
                        <div className="mt-1 flex items-center gap-2">
                          <p className="text-sm text-muted-foreground">{transaction.date}</p>
                          <span className="text-muted-foreground">•</span>
                          <p className="text-sm text-muted-foreground">{transaction.account}</p>
                          <Badge variant="outline" className="text-xs">
                            {transaction.category}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p
                        className={`text-lg font-semibold ${
                          transaction.type === "credit" ? "text-accent" : "text-foreground"
                        }`}
                      >
                        {transaction.type === "credit" ? "+" : ""}${Math.abs(transaction.amount).toFixed(2)}
                      </p>
                      <Badge
                        variant={transaction.status === "completed" ? "default" : "secondary"}
                        className="mt-1 text-xs"
                      >
                        {transaction.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
