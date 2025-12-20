"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { useToast } from "@/hooks/use-toast"
import { TrendingUp, TrendingDown, Edit, Save } from "lucide-react"

export default function AdminExchangeRatesPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [editingId, setEditingId] = useState<number | null>(null)

  const handleLogout = () => {
    router.push("/")
  }

  const handleSave = (currency: string) => {
    toast({
      title: "Rate updated",
      description: `Exchange rate for ${currency} has been updated`,
    })
    setEditingId(null)
  }

  const exchangeRates = [
    { id: 1, currency: "EUR", name: "Euro", rate: 0.92, change: "+0.25%", trend: "up", flag: "🇪🇺" },
    { id: 2, currency: "GBP", name: "British Pound", rate: 0.79, change: "-0.15%", trend: "down", flag: "🇬🇧" },
    { id: 3, currency: "JPY", name: "Japanese Yen", rate: 149.82, change: "+0.38%", trend: "up", flag: "🇯🇵" },
    { id: 4, currency: "CHF", name: "Swiss Franc", rate: 0.88, change: "+0.12%", trend: "up", flag: "🇨🇭" },
    { id: 5, currency: "CAD", name: "Canadian Dollar", rate: 1.35, change: "-0.22%", trend: "down", flag: "🇨🇦" },
    { id: 6, currency: "AUD", name: "Australian Dollar", rate: 1.52, change: "+0.18%", trend: "up", flag: "🇦🇺" },
  ]

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="admin" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Manage Exchange Rates</h1>
          <p className="text-sm text-muted-foreground">Update and manage currency exchange rates</p>
        </div>

        <div className="p-8">
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Rate Management</CardTitle>
              <CardDescription>Update exchange rates for all supported currencies</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-lg border border-border bg-muted/50 p-4">
                <p className="text-sm text-muted-foreground">
                  Last system update: <span className="font-medium text-foreground">Today at 2:45 PM EST</span>
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Changes will be reflected immediately across all client accounts
                </p>
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-2">
            {exchangeRates.map((rate) => (
              <Card key={rate.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{rate.flag}</span>
                      <div>
                        <CardTitle className="text-base">{rate.name}</CardTitle>
                        <CardDescription>{rate.currency}/USD</CardDescription>
                      </div>
                    </div>
                    <Badge variant={rate.trend === "up" ? "default" : "secondary"} className="gap-1">
                      {rate.trend === "up" ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                      {rate.change}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {editingId === rate.id ? (
                    <>
                      <div className="space-y-2">
                        <Label htmlFor={`rate-${rate.id}`}>Exchange Rate</Label>
                        <Input id={`rate-${rate.id}`} type="number" step="0.0001" defaultValue={rate.rate} />
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" onClick={() => handleSave(rate.currency)}>
                          <Save className="mr-2 h-4 w-4" />
                          Save
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => setEditingId(null)}>
                          Cancel
                        </Button>
                      </div>
                    </>
                  ) : (
                    <>
                      <div>
                        <p className="text-sm text-muted-foreground">Current Rate</p>
                        <p className="text-2xl font-bold text-foreground">{rate.rate}</p>
                      </div>
                      <Button size="sm" variant="outline" onClick={() => setEditingId(rate.id)}>
                        <Edit className="mr-2 h-4 w-4" />
                        Edit Rate
                      </Button>
                    </>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
