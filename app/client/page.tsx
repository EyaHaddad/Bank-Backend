"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { StatCard } from "@/components/stat-card"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Wallet, TrendingUp, ArrowUpRight, ArrowDownRight, CreditCard, PiggyBank } from "lucide-react"
import { useRouter } from "next/navigation"

export default function ClientDashboard() {
  const router = useRouter()

  const handleLogout = () => {
    router.push("/")
  }

  // Mock data
  const recentTransactions = [
    { id: 1, description: "Salary Deposit", amount: 5000.0, type: "credit", date: "2025-01-15", status: "completed" },
    {
      id: 2,
      description: "Grocery Store",
      amount: -125.5,
      type: "debit",
      date: "2025-01-14",
      status: "completed",
    },
    {
      id: 3,
      description: "Transfer to John Doe",
      amount: -500.0,
      type: "debit",
      date: "2025-01-13",
      status: "completed",
    },
    { id: 4, description: "Restaurant", amount: -75.25, type: "debit", date: "2025-01-12", status: "completed" },
    {
      id: 5,
      description: "Investment Return",
      amount: 250.0,
      type: "credit",
      date: "2025-01-11",
      status: "completed",
    },
  ]

  const accounts = [
    { id: 1, name: "Main Checking", type: "Checking", balance: 12450.75, number: "****1234" },
    { id: 2, name: "Savings Account", type: "Savings", balance: 28750.0, number: "****5678" },
    { id: 3, name: "Investment", type: "Investment", balance: 45250.5, number: "****9012" },
  ]

  const totalBalance = accounts.reduce((sum, account) => sum + account.balance, 0)

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <p className="text-sm text-muted-foreground">Welcome back! Here's your financial overview</p>
        </div>

        <div className="p-8">
          <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Total Balance"
              value={`$${totalBalance.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
              icon={Wallet}
              trend={{ value: "12.5%", positive: true }}
            />
            <StatCard
              title="Monthly Income"
              value="$5,000.00"
              icon={TrendingUp}
              description="Last updated today"
              trend={{ value: "8.2%", positive: true }}
            />
            <StatCard
              title="Active Accounts"
              value={accounts.length.toString()}
              icon={CreditCard}
              description="All accounts active"
            />
            <StatCard
              title="Savings Goal"
              value="68%"
              icon={PiggyBank}
              description="$20,400 of $30,000"
              trend={{ value: "5.3%", positive: true }}
            />
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Recent Transactions</CardTitle>
                <CardDescription>Your latest account activity</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentTransactions.map((transaction) => (
                    <div
                      key={transaction.id}
                      className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0"
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`flex h-10 w-10 items-center justify-center rounded-full ${
                            transaction.type === "credit" ? "bg-accent/10" : "bg-muted"
                          }`}
                        >
                          {transaction.type === "credit" ? (
                            <ArrowDownRight className="h-5 w-5 text-accent" />
                          ) : (
                            <ArrowUpRight className="h-5 w-5 text-foreground" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium text-foreground">{transaction.description}</p>
                          <p className="text-sm text-muted-foreground">{transaction.date}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p
                          className={`font-semibold ${
                            transaction.type === "credit" ? "text-accent" : "text-foreground"
                          }`}
                        >
                          {transaction.type === "credit" ? "+" : ""}${Math.abs(transaction.amount).toFixed(2)}
                        </p>
                        <Badge variant="secondary" className="mt-1 text-xs">
                          {transaction.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
                <Button
                  variant="outline"
                  className="mt-4 w-full bg-transparent"
                  onClick={() => router.push("/client/transactions")}
                >
                  View All Transactions
                </Button>
              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>My Accounts</CardTitle>
                  <CardDescription>Overview of your accounts</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {accounts.map((account) => (
                    <div key={account.id} className="rounded-lg border border-border bg-muted/50 p-4">
                      <div className="mb-2 flex items-center justify-between">
                        <span className="text-sm font-medium text-foreground">{account.name}</span>
                        <Badge variant="outline" className="text-xs">
                          {account.type}
                        </Badge>
                      </div>
                      <p className="text-2xl font-bold text-foreground">
                        ${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                      </p>
                      <p className="mt-1 text-xs text-muted-foreground">{account.number}</p>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button className="w-full justify-start" onClick={() => router.push("/client/transfer")}>
                    <ArrowUpRight className="mr-2 h-4 w-4" />
                    Transfer Money
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full justify-start bg-transparent"
                    onClick={() => router.push("/client/beneficiaries")}
                  >
                    Add Beneficiary
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full justify-start bg-transparent"
                    onClick={() => router.push("/client/statements")}
                  >
                    Download Statement
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
