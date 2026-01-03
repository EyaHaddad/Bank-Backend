"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { logoutUser } from "@/services/auth.service"
import { getBankContact, BankContactInfo } from "@/services/currency.service"
import { 
  Building2, 
  MapPin, 
  Phone, 
  Mail, 
  Globe, 
  Clock, 
  CreditCard,
  Printer,
  Loader2
} from "lucide-react"

export default function ContactPage() {
  const router = useRouter()
  const [contactInfo, setContactInfo] = useState<BankContactInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  useEffect(() => {
    const fetchContact = async () => {
      try {
        setLoading(true)
        const data = await getBankContact()
        setContactInfo(data)
        setError(null)
      } catch (err) {
        setError("Impossible de charger les informations de contact")
        console.error("Error fetching contact info:", err)
      } finally {
        setLoading(false)
      }
    }

    fetchContact()
  }, [])

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DashboardSidebar role="client" onLogout={handleLogout} />

      <main className="flex-1 overflow-y-auto">
        <div className="border-b border-border bg-card px-8 py-6">
          <h1 className="text-2xl font-bold text-foreground">Contact</h1>
          <p className="text-sm text-muted-foreground">
            Coordonnées de la banque pour nous contacter
          </p>
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
              </CardContent>
            </Card>
          ) : contactInfo ? (
            <div className="grid gap-6 md:grid-cols-2">
              {/* Bank Information */}
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent">
                      <Building2 className="h-5 w-5 text-accent-foreground" />
                    </div>
                    <div>
                      <CardTitle>{contactInfo.bank_name}</CardTitle>
                      <CardDescription>Informations générales</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-start gap-3">
                    <MapPin className="mt-0.5 h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-foreground">Adresse</p>
                      <p className="text-sm text-muted-foreground">
                        {contactInfo.address}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {contactInfo.postal_code} {contactInfo.city}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {contactInfo.country}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <CreditCard className="mt-0.5 h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-foreground">Code SWIFT/BIC</p>
                      <p className="text-sm font-mono text-muted-foreground">
                        {contactInfo.swift_code}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Contact Methods */}
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent">
                      <Phone className="h-5 w-5 text-accent-foreground" />
                    </div>
                    <div>
                      <CardTitle>Nous Contacter</CardTitle>
                      <CardDescription>Moyens de communication</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-start gap-3">
                    <Phone className="mt-0.5 h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-foreground">Téléphone</p>
                      <a 
                        href={`tel:${contactInfo.phone}`}
                        className="text-sm text-accent hover:underline"
                      >
                        {contactInfo.phone}
                      </a>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Printer className="mt-0.5 h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-foreground">Fax</p>
                      <p className="text-sm text-muted-foreground">
                        {contactInfo.fax}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Mail className="mt-0.5 h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-foreground">Email</p>
                      <a 
                        href={`mailto:${contactInfo.email}`}
                        className="text-sm text-accent hover:underline"
                      >
                        {contactInfo.email}
                      </a>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Globe className="mt-0.5 h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-foreground">Site Web</p>
                      <a 
                        href={contactInfo.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-accent hover:underline"
                      >
                        {contactInfo.website}
                      </a>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Working Hours */}
              <Card className="md:col-span-2">
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent">
                      <Clock className="h-5 w-5 text-accent-foreground" />
                    </div>
                    <div>
                      <CardTitle>Heures d'Ouverture</CardTitle>
                      <CardDescription>Nos horaires de service</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <p className="text-foreground">{contactInfo.working_hours}</p>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Pour les urgences en dehors des heures d'ouverture, veuillez contacter notre service client 24/7.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          ) : null}
        </div>
      </main>
    </div>
  )
}
