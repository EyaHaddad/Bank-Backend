"use client"

import { useEffect, useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { StatCard } from "@/components/stat-card"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Wallet, TrendingUp, ArrowUpRight, ArrowDownRight, CreditCard, PiggyBank, Loader2 } from "lucide-react"
import { useRouter } from "next/navigation"
import { getMyAccounts } from "@/services/accounts.service"
import { listMyTransactions } from "@/services/transactions.service"
import { logoutUser } from "@/services/auth.service"
import type { Account } from "@/types/account"
import type { Transaction } from "@/types/transaction"

export default function ClientDashboard() {
  const router = useRouter()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true)
        const [accountsData, transactionsData] = await Promise.all([
          getMyAccounts(),
          listMyTransactions({ page: 1, page_size: 5 }),
        ])
        setAccounts(accountsData)
        setTransactions(transactionsData.transactions)
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err)
        setError("Failed to load dashboard data")
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [])

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  const totalBalance = accounts.reduce((sum, account) => sum + account.balance, 0)

  // Calculate monthly income from credit transactions
  const monthlyIncome = transactions
    .filter((t) => t.type === "CREDIT")
    .reduce((sum, t) => sum + t.amount, 0)

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
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <p className="text-sm text-muted-foreground">Welcome back! Here's your financial overview</p>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-4 rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              {error}
            </div>
          )}

          <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Total Balance"
              value={`$${totalBalance.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
              icon={Wallet}
              trend={{ value: "12.5%", positive: true }}
            />
            <StatCard
              title="Monthly Income"
              value={`$${monthlyIncome.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
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
                  {transactions.length === 0 ? (
                    <p className="text-center text-muted-foreground py-4">No transactions yet</p>
                  ) : (
                    transactions.map((transaction) => (
                      <div
                        key={transaction.id}
                        className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0"
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`flex h-10 w-10 items-center justify-center rounded-full ${
                              transaction.type === "CREDIT" ? "bg-accent/10" : "bg-muted"
                            }`}
                          >
                            {transaction.type === "CREDIT" ? (
                              <ArrowDownRight className="h-5 w-5 text-accent" />
                            ) : (
                              <ArrowUpRight className="h-5 w-5 text-foreground" />
                            )}
                          </div>
                          <div>
                            <p className="font-medium text-foreground">
                              {transaction.reference || transaction.type}
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {new Date(transaction.created_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p
                            className={`font-semibold ${
                              transaction.type === "CREDIT" ? "text-accent" : "text-foreground"
                            }`}
                          >
                            {transaction.type === "CREDIT" ? "+" : "-"}${transaction.amount.toFixed(2)}
                          </p>
                          <Badge variant="secondary" className="mt-1 text-xs">
                            {transaction.status.toLowerCase()}
                          </Badge>
                        </div>
                      </div>
                    ))
                  )}
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
                  {accounts.length === 0 ? (
                    <p className="text-center text-muted-foreground py-4">No accounts found</p>
                  ) : (
                    accounts.map((account) => (
                      <div key={account.id} className="rounded-lg border border-border bg-muted/50 p-4">
                        <div className="mb-2 flex items-center justify-between">
                          <span className="text-sm font-medium text-foreground">Account</span>
                          <Badge variant="outline" className="text-xs">
                            {account.currency}
                          </Badge>
                        </div>
                        <p className="text-2xl font-bold text-foreground">
                          ${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                        </p>
                        <p className="mt-1 text-xs text-muted-foreground">
                          ID: {account.id.substring(0, 8)}...
                        </p>
                      </div>
                    ))
                  )}
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
