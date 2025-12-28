"use client"

import { useEffect, useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/useToast"
import { UserPlus, Trash2, User, Loader2, CheckCircle } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  listBeneficiaries,
  createBeneficiary,
  deleteBeneficiary,
  verifyBeneficiary,
} from "@/services/beneficiaries.service"
import { logoutUser } from "@/services/auth.service"
import type { Beneficiary, BeneficiaryCreate } from "@/types/beneficiary"

export default function BeneficiariesPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [showAddDialog, setShowAddDialog] = useState(false)
  const [beneficiaryName, setBeneficiaryName] = useState("")
  const [iban, setIban] = useState("")
  const [bankName, setBankName] = useState("")
  const [email, setEmail] = useState("")
  const [beneficiaries, setBeneficiaries] = useState<Beneficiary[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  const fetchBeneficiaries = async () => {
    try {
      setIsLoading(true)
      const data = await listBeneficiaries()
      setBeneficiaries(data.beneficiaries)
    } catch (err) {
      console.error("Failed to fetch beneficiaries:", err)
      setError("Failed to load beneficiaries")
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchBeneficiaries()
  }, [])

  const handleAddBeneficiary = async () => {
    try {
      setIsSubmitting(true)
      const newBeneficiary: BeneficiaryCreate = {
        name: beneficiaryName,
        bank_name: bankName,
        iban: iban,
        email: email || undefined,
      }
      await createBeneficiary(newBeneficiary)
      toast({
        title: "Beneficiary added",
        description: `${beneficiaryName} has been added to your beneficiaries`,
      })
      setShowAddDialog(false)
      setBeneficiaryName("")
      setIban("")
      setBankName("")
      setEmail("")
      fetchBeneficiaries()
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to add beneficiary",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteBeneficiary = async (id: string, name: string) => {
    try {
      await deleteBeneficiary(id)
      toast({
        title: "Beneficiary removed",
        description: `${name} has been removed`,
        variant: "destructive",
      })
      fetchBeneficiaries()
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to remove beneficiary",
        variant: "destructive",
      })
    }
  }

  const handleVerifyBeneficiary = async (id: string, name: string) => {
    try {
      await verifyBeneficiary(id)
      toast({
        title: "Beneficiary verified",
        description: `${name} has been verified`,
      })
      fetchBeneficiaries()
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to verify beneficiary",
        variant: "destructive",
      })
    }
  }

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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Beneficiaries</h1>
              <p className="text-sm text-muted-foreground">Manage your trusted recipients</p>
            </div>
            <Button onClick={() => setShowAddDialog(true)}>
              <UserPlus className="mr-2 h-4 w-4" />
              Add Beneficiary
            </Button>
          </div>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-4 rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              {error}
            </div>
          )}

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {beneficiaries.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <User className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No beneficiaries yet</p>
                <Button className="mt-4" onClick={() => setShowAddDialog(true)}>
                  Add your first beneficiary
                </Button>
              </div>
            ) : (
              beneficiaries.map((beneficiary) => (
                <Card key={beneficiary.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10">
                          <User className="h-5 w-5 text-accent" />
                        </div>
                        <div>
                          <CardTitle className="text-base">{beneficiary.name}</CardTitle>
                          <CardDescription className="text-xs">{beneficiary.bank_name}</CardDescription>
                        </div>
                      </div>
                      <Badge variant={beneficiary.is_verified ? "default" : "secondary"} className="text-xs">
                        {beneficiary.is_verified ? "verified" : "pending"}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div>
                        <p className="text-xs text-muted-foreground">IBAN</p>
                        <p className="font-mono text-sm font-medium text-foreground">
                          {beneficiary.iban.substring(0, 4)}...{beneficiary.iban.substring(beneficiary.iban.length - 4)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Added on</p>
                        <p className="text-sm text-foreground">
                          {new Date(beneficiary.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex gap-2 pt-2">
                        <Button
                          size="sm"
                          className="flex-1"
                          onClick={() => router.push("/client/transfer")}
                          disabled={!beneficiary.is_verified}
                        >
                          Transfer
                        </Button>
                        {!beneficiary.is_verified && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleVerifyBeneficiary(beneficiary.id, beneficiary.name)}
                          >
                            <CheckCircle className="h-4 w-4" />
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDeleteBeneficiary(beneficiary.id, beneficiary.name)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </main>

      <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Beneficiary</DialogTitle>
            <DialogDescription>Enter the beneficiary details to add them to your list</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="beneficiaryName">Beneficiary Name</Label>
              <Input
                id="beneficiaryName"
                placeholder="Full name"
                value={beneficiaryName}
                onChange={(e) => setBeneficiaryName(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="iban">IBAN</Label>
              <Input
                id="iban"
                placeholder="TN59XXXXXXXXXXXXXXXXXXXX"
                value={iban}
                onChange={(e) => setIban(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="bankName">Bank Name</Label>
              <Input
                id="bankName"
                placeholder="Bank name"
                value={bankName}
                onChange={(e) => setBankName(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email (Optional)</Label>
              <Input
                id="email"
                type="email"
                placeholder="beneficiary@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="rounded-lg border border-border bg-muted/50 p-3">
              <p className="text-xs text-muted-foreground">
                New beneficiaries require verification before transfers can be made. This typically takes 1-2 business
                days.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddDialog(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleAddBeneficiary}
              disabled={!beneficiaryName || !iban || !bankName || isSubmitting}
            >
              {isSubmitting ? "Adding..." : "Add Beneficiary"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
