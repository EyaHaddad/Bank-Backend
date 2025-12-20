"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { StatCard } from "@/components/stat-card"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Users, Building2, TrendingUp, AlertCircle, CheckCircle, Clock } from "lucide-react"
import { useRouter } from "next/navigation"

export default function AdminDashboard() {
  const router = useRouter()

  const handleLogout = () => {
    router.push("/")
  }

  const recentRequests = [
    { id: 1, client: "John Smith", type: "Account Opening", status: "pending", date: "2025-01-16" },
    { id: 2, client: "Jane Doe", type: "Loan Application", status: "approved", date: "2025-01-15" },
    { id: 3, client: "Mike Johnson", type: "Card Replacement", status: "pending", date: "2025-01-14" },
    { id: 4, client: "Sarah Williams", type: "Account Closure", status: "rejected", date: "2025-01-13" },
  ]

  const recentActivity = [
    { id: 1, action: "New client registered", user: "John Smith", time: "2 hours ago" },
    { id: 2, action: "Account updated", user: "Admin User", time: "4 hours ago" },
    { id: 3, action: "Exchange rate updated", user: "System", time: "6 hours ago" },
    { id: 4, action: "Client request approved", user: "Admin User", time: "1 day ago" },
  ]

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="admin" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Admin Dashboard</h1>
          <p className="text-sm text-muted-foreground">Manage your banking operations</p>
        </div>

        <div className="p-8">
          <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <StatCard title="Total Clients" value="1,284" icon={Users} trend={{ value: "12.5%", positive: true }} />
            <StatCard
              title="Active Accounts"
              value="2,847"
              icon={Building2}
              trend={{ value: "8.2%", positive: true }}
            />
            <StatCard
              title="Total Balance"
              value="$45.2M"
              icon={TrendingUp}
              trend={{ value: "15.3%", positive: true }}
            />
            <StatCard
              title="Pending Requests"
              value="23"
              icon={AlertCircle}
              description="Requires attention"
              trend={{ value: "5", positive: false }}
            />
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Recent Requests</CardTitle>
                    <CardDescription>Client requests requiring review</CardDescription>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => router.push("/admin/requests")}>
                    View All
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentRequests.map((request) => (
                    <div
                      key={request.id}
                      className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                          {request.status === "pending" ? (
                            <Clock className="h-5 w-5 text-foreground" />
                          ) : request.status === "approved" ? (
                            <CheckCircle className="h-5 w-5 text-accent" />
                          ) : (
                            <AlertCircle className="h-5 w-5 text-destructive" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium text-foreground">{request.client}</p>
                          <p className="text-sm text-muted-foreground">{request.type}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <Badge
                          variant={
                            request.status === "pending"
                              ? "secondary"
                              : request.status === "approved"
                                ? "default"
                                : "destructive"
                          }
                        >
                          {request.status}
                        </Badge>
                        <p className="mt-1 text-xs text-muted-foreground">{request.date}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button className="w-full justify-start" onClick={() => router.push("/admin/clients")}>
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
                  <Button
                    variant="outline"
                    className="w-full justify-start bg-transparent"
                    onClick={() => router.push("/admin/exchange-rates")}
                  >
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Update Exchange Rates
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                  <CardDescription>System activity log</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentActivity.map((activity) => (
                      <div key={activity.id} className="space-y-1">
                        <p className="text-sm font-medium text-foreground">{activity.action}</p>
                        <p className="text-xs text-muted-foreground">
                          {activity.user} • {activity.time}
                        </p>
                      </div>
                    ))}
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
