"use client"

import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { useToast } from "@/hooks/useToast"
import { UserPlus, Trash2, User } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export default function BeneficiariesPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [showAddDialog, setShowAddDialog] = useState(false)
  const [beneficiaryName, setBeneficiaryName] = useState("")
  const [accountNumber, setAccountNumber] = useState("")
  const [bankName, setBankName] = useState("")

  const handleLogout = () => {
    router.push("/")
  }

  const handleAddBeneficiary = () => {
    toast({
      title: "Beneficiary added",
      description: `${beneficiaryName} has been added to your beneficiaries`,
    })
    setShowAddDialog(false)
    setBeneficiaryName("")
    setAccountNumber("")
    setBankName("")
  }

  const beneficiaries = [
    { id: 1, name: "John Smith", account: "****1234", bank: "Chase Bank", status: "verified", addedDate: "2024-12-01" },
    {
      id: 2,
      name: "Jane Doe",
      account: "****5678",
      bank: "Bank of America",
      status: "verified",
      addedDate: "2024-11-15",
    },
    {
      id: 3,
      name: "Mike Johnson",
      account: "****9012",
      bank: "Wells Fargo",
      status: "pending",
      addedDate: "2025-01-10",
    },
    {
      id: 4,
      name: "Sarah Williams",
      account: "****3456",
      bank: "Citibank",
      status: "verified",
      addedDate: "2024-10-20",
    },
  ]

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
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {beneficiaries.map((beneficiary) => (
              <Card key={beneficiary.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10">
                        <User className="h-5 w-5 text-accent" />
                      </div>
                      <div>
                        <CardTitle className="text-base">{beneficiary.name}</CardTitle>
                        <CardDescription className="text-xs">{beneficiary.bank}</CardDescription>
                      </div>
                    </div>
                    <Badge variant={beneficiary.status === "verified" ? "default" : "secondary"} className="text-xs">
                      {beneficiary.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <p className="text-xs text-muted-foreground">Account Number</p>
                      <p className="font-mono text-sm font-medium text-foreground">{beneficiary.account}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Added on</p>
                      <p className="text-sm text-foreground">{beneficiary.addedDate}</p>
                    </div>
                    <div className="flex gap-2 pt-2">
                      <Button size="sm" className="flex-1" onClick={() => router.push("/client/transfer")}>
                        Transfer
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          toast({
                            title: "Beneficiary removed",
                            description: `${beneficiary.name} has been removed`,
                            variant: "destructive",
                          })
                        }
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
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
              <Label htmlFor="accountNumber">Account Number</Label>
              <Input
                id="accountNumber"
                placeholder="1234567890"
                value={accountNumber}
                onChange={(e) => setAccountNumber(e.target.value)}
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
            <Button onClick={handleAddBeneficiary} disabled={!beneficiaryName || !accountNumber || !bankName}>
              Add Beneficiary
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
