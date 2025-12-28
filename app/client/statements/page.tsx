"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { Download, FileText, Calendar } from "lucide-react"
import { logoutUser } from "@/services/auth.service"

export default function StatementsPage() {
  const router = useRouter()

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  // Static data - no backend endpoint for statements
  const statements = [
    { id: 1, month: "January 2025", period: "01/01/2025 - 01/31/2025", account: "Main Checking", size: "2.4 MB" },
    { id: 2, month: "December 2024", period: "12/01/2024 - 12/31/2024", account: "Main Checking", size: "2.1 MB" },
    { id: 3, month: "November 2024", period: "11/01/2024 - 11/30/2024", account: "Main Checking", size: "1.9 MB" },
    { id: 4, month: "October 2024", period: "10/01/2024 - 10/31/2024", account: "Main Checking", size: "2.3 MB" },
    { id: 5, month: "January 2025", period: "01/01/2025 - 01/31/2025", account: "Savings Account", size: "1.2 MB" },
    { id: 6, month: "December 2024", period: "12/01/2024 - 12/31/2024", account: "Savings Account", size: "1.1 MB" },
  ]

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Account Statements</h1>
          <p className="text-sm text-muted-foreground">Download your monthly account statements</p>
        </div>

        <div className="p-8">
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Statement Information</CardTitle>
              <CardDescription>Your account statements are generated monthly</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <FileText className="mb-2 h-5 w-5 text-accent" />
                  <p className="text-sm font-medium text-foreground">Available Statements</p>
                  <p className="text-2xl font-bold text-foreground">{statements.length}</p>
                </div>
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <Calendar className="mb-2 h-5 w-5 text-accent" />
                  <p className="text-sm font-medium text-foreground">Latest Statement</p>
                  <p className="text-lg font-semibold text-foreground">January 2025</p>
                </div>
                <div className="rounded-lg border border-border bg-muted/50 p-4">
                  <Download className="mb-2 h-5 w-5 text-accent" />
                  <p className="text-sm font-medium text-foreground">Format</p>
                  <p className="text-lg font-semibold text-foreground">PDF</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Statements</CardTitle>
              <CardDescription>Download your account statements in PDF format</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {statements.map((statement) => (
                  <div
                    key={statement.id}
                    className="flex items-center justify-between rounded-lg border border-border bg-card p-4"
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-accent/10">
                        <FileText className="h-6 w-6 text-accent" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">{statement.month}</p>
                        <p className="text-sm text-muted-foreground">{statement.period}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <Badge variant="outline" className="mb-1">
                          {statement.account}
                        </Badge>
                        <p className="text-xs text-muted-foreground">{statement.size}</p>
                      </div>
                      <Button size="sm">
                        <Download className="mr-2 h-4 w-4" />
                        Download
                      </Button>
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
