"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { Search, MessageSquare, Phone, Mail } from "lucide-react"

export default function RelationshipsPage() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")

  const handleLogout = () => {
    router.push("/")
  }

  const relationships = [
    {
      id: 1,
      client: "John Smith",
      status: "excellent",
      lastContact: "2025-01-15",
      accountValue: 41200.75,
      interactions: 12,
      notes: "Long-term client, high satisfaction",
    },
    {
      id: 2,
      client: "Jane Doe",
      status: "good",
      lastContact: "2025-01-10",
      accountValue: 15500.0,
      interactions: 8,
      notes: "Interested in investment products",
    },
    {
      id: 3,
      client: "Mike Johnson",
      status: "excellent",
      lastContact: "2025-01-14",
      accountValue: 89750.25,
      interactions: 15,
      notes: "Premium client, requires dedicated support",
    },
    {
      id: 4,
      client: "Sarah Williams",
      status: "at-risk",
      lastContact: "2024-12-20",
      accountValue: 5200.0,
      interactions: 3,
      notes: "Low engagement, follow up needed",
    },
    {
      id: 5,
      client: "David Brown",
      status: "good",
      lastContact: "2025-01-12",
      accountValue: 32450.5,
      interactions: 10,
      notes: "Regular communication, satisfied customer",
    },
  ]

  const filteredRelationships = relationships.filter((rel) =>
    rel.client.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="admin" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Customer Relationships</h1>
          <p className="text-sm text-muted-foreground">Manage client relationships and interactions</p>
        </div>

        <div className="p-8">
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Client Relationships</CardTitle>
                  <CardDescription>Overview of customer relationship status</CardDescription>
                </div>
                <div className="w-64">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search clients..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredRelationships.map((relationship) => (
                  <div key={relationship.id} className="rounded-lg border border-border bg-card p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="mb-2 flex items-center gap-2">
                          <h3 className="font-semibold text-foreground">{relationship.client}</h3>
                          <Badge
                            variant={
                              relationship.status === "excellent"
                                ? "default"
                                : relationship.status === "good"
                                  ? "secondary"
                                  : "destructive"
                            }
                          >
                            {relationship.status}
                          </Badge>
                        </div>
                        <div className="mb-3 grid gap-2 text-sm md:grid-cols-3">
                          <div>
                            <p className="text-muted-foreground">Account Value</p>
                            <p className="font-medium text-foreground">${relationship.accountValue.toLocaleString()}</p>
                          </div>
                          <div>
                            <p className="text-muted-foreground">Last Contact</p>
                            <p className="font-medium text-foreground">{relationship.lastContact}</p>
                          </div>
                          <div>
                            <p className="text-muted-foreground">Interactions</p>
                            <p className="font-medium text-foreground">{relationship.interactions}</p>
                          </div>
                        </div>
                        <p className="text-sm text-muted-foreground">{relationship.notes}</p>
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">
                          <MessageSquare className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Phone className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Mail className="h-4 w-4" />
                        </Button>
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
