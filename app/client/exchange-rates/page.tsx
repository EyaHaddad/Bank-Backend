"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { TrendingUp, TrendingDown, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function ExchangeRatesPage() {
  const router = useRouter()

  const handleLogout = () => {
    router.push("/")
  }

  const exchangeRates = [
    { currency: "EUR", name: "Euro", rate: 0.92, change: "+0.25%", trend: "up", flag: "🇪🇺" },
    { currency: "GBP", name: "British Pound", rate: 0.79, change: "-0.15%", trend: "down", flag: "🇬🇧" },
    { currency: "JPY", name: "Japanese Yen", rate: 149.82, change: "+0.38%", trend: "up", flag: "🇯🇵" },
    { currency: "CHF", name: "Swiss Franc", rate: 0.88, change: "+0.12%", trend: "up", flag: "🇨🇭" },
    { currency: "CAD", name: "Canadian Dollar", rate: 1.35, change: "-0.22%", trend: "down", flag: "🇨🇦" },
    { currency: "AUD", name: "Australian Dollar", rate: 1.52, change: "+0.18%", trend: "up", flag: "🇦🇺" },
    { currency: "CNY", name: "Chinese Yuan", rate: 7.24, change: "+0.05%", trend: "up", flag: "🇨🇳" },
    { currency: "INR", name: "Indian Rupee", rate: 83.15, change: "-0.08%", trend: "down", flag: "🇮🇳" },
    { currency: "MXN", name: "Mexican Peso", rate: 17.05, change: "+0.32%", trend: "up", flag: "🇲🇽" },
    { currency: "BRL", name: "Brazilian Real", rate: 4.95, change: "-0.45%", trend: "down", flag: "🇧🇷" },
  ]

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Exchange Rates</h1>
              <p className="text-sm text-muted-foreground">Current foreign exchange rates (USD base)</p>
            </div>
            <Button variant="outline">
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh Rates
            </Button>
          </div>
        </div>

        <div className="p-8">
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Rate Information</CardTitle>
              <CardDescription>Exchange rates are updated every 15 minutes during market hours</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-lg border border-border bg-muted/50 p-4">
                <p className="text-sm text-muted-foreground">
                  Last updated: <span className="font-medium text-foreground">Today at 2:45 PM EST</span>
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Rates are indicative and may vary for actual transactions. Contact us for live rates.
                </p>
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {exchangeRates.map((rate) => (
              <Card key={rate.currency}>
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{rate.flag}</span>
                      <div>
                        <h3 className="font-semibold text-foreground">{rate.currency}</h3>
                        <p className="text-sm text-muted-foreground">{rate.name}</p>
                      </div>
                    </div>
                    <Badge variant={rate.trend === "up" ? "default" : "secondary"} className="gap-1">
                      {rate.trend === "up" ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                      {rate.change}
                    </Badge>
                  </div>
                  <div className="mt-4 flex items-baseline gap-2">
                    <span className="text-2xl font-bold text-foreground">{rate.rate}</span>
                    <span className="text-sm text-muted-foreground">{rate.currency}/USD</span>
                  </div>
                  <div className="mt-4 rounded-lg bg-muted/50 p-3">
                    <p className="text-xs text-muted-foreground">
                      1 USD = {rate.rate} {rate.currency}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      1 {rate.currency} = {(1 / rate.rate).toFixed(4)} USD
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
