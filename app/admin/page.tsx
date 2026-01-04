"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { StatCard } from "@/components/stat-card"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Users, Building2, TrendingUp, AlertCircle, Loader2, DollarSign } from "lucide-react"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { logoutUser } from "@/services/auth.service"
import { listUsers } from "@/services/users.service"
import { listAllAccounts } from "@/services/admin.service"
import type { User } from "@/types/user"
import type { Account } from "@/types/account"

export default function AdminDashboard() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)
  const [users, setUsers] = useState<User[]>([])
  const [accounts, setAccounts] = useState<Account[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        const [usersData, accountsData] = await Promise.all([
          listUsers(),
          listAllAccounts()
        ])
        setUsers(usersData || [])
        setAccounts(accountsData || [])
      } catch (err) {
        console.error("Failed to fetch data:", err)
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

  // Calculate stats from users
  const totalClients = users.filter(u => u.role === "user").length
  const totalAdmins = users.filter(u => u.role === "admin").length
  const activeUsers = users.filter(u => u.is_active).length
  const inactiveUsers = users.filter(u => !u.is_active).length

  // Calculate stats from accounts
  const totalAccounts = accounts.length
  const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0)
  const currencies = [...new Set(accounts.map(acc => acc.currency))]

  // Get recent users activity
  const recentUsers = users.slice(0, 5)

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
          <h1 className="text-2xl font-bold text-foreground">Admin Dashboard</h1>
          <p className="text-sm text-muted-foreground">Manage your banking operations</p>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-4 rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              {error}
            </div>
          )}

          <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <StatCard 
              title="Total Clients" 
              value={totalClients.toString()} 
              icon={Users} 
              trend={{ value: `${totalAdmins} admins`, positive: true }} 
            />
            <StatCard
              title="Active Users"
              value={activeUsers.toString()}
              icon={Users}
              trend={{ value: users.length > 0 ? `${((activeUsers / users.length) * 100).toFixed(1)}%` : "0%", positive: true }}
            />
            <StatCard
              title="Total Accounts"
              value={totalAccounts.toString()}
              icon={Building2}
              trend={{ value: `${currencies.length} currencies`, positive: true }}
            />
            <StatCard
              title="Total Balance"
              value={`$${totalBalance.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
              icon={DollarSign}
              description="All accounts combined"
            />
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Recent Users</CardTitle>
                    <CardDescription>Latest registered users</CardDescription>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => router.push("/admin/users")}>
                    View All
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentUsers.length === 0 ? (
                    <p className="text-center text-muted-foreground py-4">No users found</p>
                  ) : (
                    recentUsers.map((user) => (
                      <div
                        key={user.id}
                        className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0"
                      >
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                            <Users className="h-5 w-5 text-foreground" />
                          </div>
                          <div>
                            <p className="font-medium text-foreground">{user.firstname} {user.lastname}</p>
                            <p className="text-sm text-muted-foreground">{user.email}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                            user.is_active 
                              ? "bg-accent/10 text-accent" 
                              : "bg-destructive/10 text-destructive"
                          }`}>
                            {user.is_active ? "Active" : "Inactive"}
                          </span>
                          <p className="mt-1 text-xs text-muted-foreground">
                            {new Date(user.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button className="w-full justify-start" onClick={() => router.push("/admin/users")}>
                    <Users className="mr-2 h-4 w-4" />
                    Manage Clients
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full justify-start bg-transparent"
                    onClick={() => router.push("/admin/accounts")}
                  >
                    <Building2 className="mr-2 h-4 w-4" />
                    Manage Accounts
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>System Overview</CardTitle>
                  <CardDescription>Current system status</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Total Users</span>
                      <span className="font-medium">{users.length}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Total Accounts</span>
                      <span className="font-medium">{totalAccounts}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Active Users</span>
                      <span className="font-medium text-accent">{activeUsers}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Inactive Users</span>
                      <span className="font-medium text-destructive">{inactiveUsers}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
