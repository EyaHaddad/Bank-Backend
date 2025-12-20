"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"
import { CheckCircle, XCircle, Clock } from "lucide-react"

export default function ClientRequestsPage() {
  const router = useRouter()
  const { toast } = useToast()

  const handleLogout = () => {
    router.push("/")
  }

  const handleApprove = (clientName: string) => {
    toast({
      title: "Request approved",
      description: `${clientName}'s request has been approved`,
    })
  }

  const handleReject = (clientName: string) => {
    toast({
      title: "Request rejected",
      description: `${clientName}'s request has been rejected`,
      variant: "destructive",
    })
  }

  const requests = [
    {
      id: 1,
      client: "John Smith",
      type: "Account Opening",
      description: "Request to open a new savings account",
      status: "pending",
      date: "2025-01-16",
      priority: "high",
    },
    {
      id: 2,
      client: "Jane Doe",
      type: "Loan Application",
      description: "Personal loan application for $50,000",
      status: "approved",
      date: "2025-01-15",
      priority: "medium",
    },
    {
      id: 3,
      client: "Mike Johnson",
      type: "Card Replacement",
      description: "Debit card replacement due to loss",
      status: "pending",
      date: "2025-01-14",
      priority: "low",
    },
    {
      id: 4,
      client: "Sarah Williams",
      type: "Account Closure",
      description: "Request to close checking account",
      status: "rejected",
      date: "2025-01-13",
      priority: "medium",
    },
    {
      id: 5,
      client: "David Brown",
      type: "Credit Limit Increase",
      description: "Request to increase credit card limit to $20,000",
      status: "pending",
      date: "2025-01-12",
      priority: "high",
    },
    {
      id: 6,
      client: "Emily Davis",
      type: "Dispute Resolution",
      description: "Transaction dispute for $250",
      status: "pending",
      date: "2025-01-11",
      priority: "high",
    },
  ]

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="admin" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Client Requests</h1>
          <p className="text-sm text-muted-foreground">Review and manage client requests</p>
        </div>

        <div className="p-8">
          <div className="mb-6 grid gap-4 md:grid-cols-3">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-500/10">
                    <Clock className="h-6 w-6 text-yellow-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Pending</p>
                    <p className="text-2xl font-bold text-foreground">
                      {requests.filter((r) => r.status === "pending").length}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-accent/10">
                    <CheckCircle className="h-6 w-6 text-accent" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Approved</p>
                    <p className="text-2xl font-bold text-foreground">
                      {requests.filter((r) => r.status === "approved").length}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-destructive/10">
                    <XCircle className="h-6 w-6 text-destructive" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Rejected</p>
                    <p className="text-2xl font-bold text-foreground">
                      {requests.filter((r) => r.status === "rejected").length}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>All Requests</CardTitle>
              <CardDescription>Review and take action on client requests</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {requests.map((request) => (
                  <div key={request.id} className="rounded-lg border border-border bg-card p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="mb-2 flex items-center gap-2">
                          <h3 className="font-semibold text-foreground">{request.client}</h3>
                          <Badge variant="outline" className="text-xs">
                            {request.type}
                          </Badge>
                          <Badge
                            variant={
                              request.priority === "high"
                                ? "destructive"
                                : request.priority === "medium"
                                  ? "secondary"
                                  : "outline"
                            }
                            className="text-xs"
                          >
                            {request.priority}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">{request.description}</p>
                        <p className="mt-2 text-xs text-muted-foreground">Submitted on {request.date}</p>
                      </div>
                      <div className="flex items-center gap-2">
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
                        {request.status === "pending" && (
                          <div className="flex gap-2">
                            <Button size="sm" onClick={() => handleApprove(request.client)}>
                              <CheckCircle className="mr-1 h-4 w-4" />
                              Approve
                            </Button>
                            <Button size="sm" variant="outline" onClick={() => handleReject(request.client)}>
                              <XCircle className="mr-1 h-4 w-4" />
                              Reject
                            </Button>
                          </div>
                        )}
                      </div>
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
