"use client"

import { useEffect, useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from "next/navigation"
import { RefreshCw, ArrowRightLeft, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { logoutUser } from "@/services/auth.service"
import { 
  getExchangeRates, 
  convertCurrency, 
  ExchangeRatesResponse, 
  ConversionResponse
} from "@/services/currency.service"

export default function ExchangeRatesPage() {
  const router = useRouter()
  const [ratesData, setRatesData] = useState<ExchangeRatesResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Conversion state
  const [amount, setAmount] = useState<string>("")
  const [selectedCurrency, setSelectedCurrency] = useState<string>("")
  const [conversionResult, setConversionResult] = useState<ConversionResponse | null>(null)
  const [converting, setConverting] = useState(false)

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  const fetchRates = async (showRefreshing = false) => {
    try {
      if (showRefreshing) {
        setRefreshing(true)
      } else {
        setLoading(true)
      }
      const data = await getExchangeRates()
      setRatesData(data)
      setError(null)
    } catch (err) {
      setError("Impossible de charger les taux de change. Veuillez réessayer.")
      console.error("Error fetching rates:", err)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  const handleConvert = async () => {
    if (!amount || !selectedCurrency) return
    
    const numAmount = parseFloat(amount)
    if (isNaN(numAmount) || numAmount <= 0) {
      return
    }

    try {
      setConverting(true)
      const result = await convertCurrency({
        amount: numAmount,
        target_currency: selectedCurrency
      })
      setConversionResult(result)
    } catch (err) {
      console.error("Error converting:", err)
      setConversionResult(null)
    } finally {
      setConverting(false)
    }
  }

  useEffect(() => {
    fetchRates()
  }, [])

  // Reset conversion result when inputs change
  useEffect(() => {
    setConversionResult(null)
  }, [amount, selectedCurrency])

  const formatDate = (isoString: string) => {
    const date = new Date(isoString)
    return date.toLocaleString("fr-TN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    })
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Taux de Change</h1>
              <p className="text-sm text-muted-foreground">
                Taux de change actuels (base: Dinar Tunisien - TND)
              </p>
            </div>
            <Button 
              variant="outline" 
              onClick={() => fetchRates(true)}
              disabled={refreshing}
            >
              {refreshing ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <RefreshCw className="mr-2 h-4 w-4" />
              )}
              Actualiser
            </Button>
          </div>
        </div>

        <div className="p-8">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : error ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <p className="text-center text-destructive">{error}</p>
                <div className="mt-4 text-center">
                  <Button onClick={() => fetchRates()}>Réessayer</Button>
                </div>
              </CardContent>
            </Card>
          ) : ratesData ? (
            <>
              {/* Rate Information */}
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle>Informations sur les Taux</CardTitle>
                  <CardDescription>
                    Les taux sont mis à jour en temps réel depuis une source externe
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <p className="text-sm text-muted-foreground">
                      Dernière mise à jour:{" "}
                      <span className="font-medium text-foreground">
                        {formatDate(ratesData.last_updated)}
                      </span>
                    </p>
                    <p className="mt-2 text-xs text-muted-foreground">
                      Devise de base: {ratesData.base_currency_name} ({ratesData.base_currency})
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Currency Conversion Tool */}
              <Card className="mb-6">
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <ArrowRightLeft className="h-5 w-5 text-accent" />
                    <div>
                      <CardTitle>Convertisseur de Devises</CardTitle>
                      <CardDescription>
                        Convertir un montant de TND vers une autre devise
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-3">
                    <div className="space-y-2">
                      <Label htmlFor="amount">Montant (TND)</Label>
                      <Input
                        id="amount"
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="Entrez le montant"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="currency">Devise cible</Label>
                      <Select value={selectedCurrency} onValueChange={setSelectedCurrency}>
                        <SelectTrigger id="currency">
                          <SelectValue placeholder="Sélectionner une devise" />
                        </SelectTrigger>
                        <SelectContent>
                          {ratesData.rates.map((rate) => (
                            <SelectItem key={rate.code} value={rate.code}>
                              {rate.flag} {rate.code} - {rate.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="flex items-end">
                      <Button 
                        onClick={handleConvert}
                        disabled={!amount || !selectedCurrency || converting}
                        className="w-full"
                      >
                        {converting ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <ArrowRightLeft className="mr-2 h-4 w-4" />
                        )}
                        Convertir
                      </Button>
                    </div>
                  </div>

                  {conversionResult && (
                    <div className="mt-4 rounded-lg border border-accent bg-accent/10 p-4">
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Résultat de la conversion</p>
                        <p className="mt-2 text-3xl font-bold text-foreground">
                          {conversionResult.converted_amount.toLocaleString("fr-TN", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                          })}{" "}
                          <span className="text-accent">{conversionResult.target_currency}</span>
                        </p>
                        <p className="mt-2 text-sm text-muted-foreground">
                          {conversionResult.original_amount.toLocaleString("fr-TN")} TND × {conversionResult.rate} = {conversionResult.converted_amount.toLocaleString("fr-TN", { minimumFractionDigits: 2 })} {conversionResult.target_currency}
                        </p>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Exchange Rates Grid */}
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {ratesData.rates.map((rate) => (
                  <Card key={rate.code}>
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <span className="text-3xl">{rate.flag}</span>
                          <div>
                            <h3 className="font-semibold text-foreground">{rate.code}</h3>
                            <p className="text-sm text-muted-foreground">{rate.name}</p>
                          </div>
                        </div>
                      </div>
                      <div className="mt-4 flex items-baseline gap-2">
                        <span className="text-2xl font-bold text-foreground">
                          {rate.rate.toFixed(4)}
                        </span>
                        <span className="text-sm text-muted-foreground">{rate.code}/TND</span>
                      </div>
                      <div className="mt-4 rounded-lg bg-muted/50 p-3">
                        <p className="text-xs text-muted-foreground">
                          1 TND = {rate.rate.toFixed(4)} {rate.code}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          1 {rate.code} = {(1 / rate.rate).toFixed(4)} TND
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </>
          ) : null}
        </div>
      </main>
    </div>
  )
}
