"use client"

import { useEffect, useState, useRef } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { useRouter } from "next/navigation"
import { Download, FileText, Printer, Loader2 } from "lucide-react"
import { logoutUser } from "@/services/auth.service"
import { getMyAccounts } from "@/services/accounts.service"
import { listAccountTransactions } from "@/services/transactions.service"
import type { Account } from "@/types/account"
import type { Transaction } from "@/types/transaction"

export default function StatementsPage() {
  const router = useRouter()
  const [accounts, setAccounts] = useState<Account[]>([])
  const [selectedAccountId, setSelectedAccountId] = useState<string>("")
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isLoadingTransactions, setIsLoadingTransactions] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const printRef = useRef<HTMLDivElement>(null)

  const handleLogout = () => {
    logoutUser()
    router.push("/")
  }

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        setIsLoading(true)
        const data = await getMyAccounts()
        setAccounts(data || [])
        if (data && data.length > 0) {
          setSelectedAccountId(data[0].id)
        }
      } catch (err) {
        console.error("Failed to fetch accounts:", err)
        setError("Failed to load accounts")
      } finally {
        setIsLoading(false)
      }
    }
    fetchAccounts()
  }, [])

  useEffect(() => {
    const fetchTransactions = async () => {
      if (!selectedAccountId) return
      
      try {
        setIsLoadingTransactions(true)
        const data = await listAccountTransactions(selectedAccountId, { page_size: 50 })
        setTransactions(data?.transactions || [])
      } catch (err) {
        console.error("Failed to fetch transactions:", err)
        setTransactions([])
      } finally {
        setIsLoadingTransactions(false)
      }
    }
    fetchTransactions()
  }, [selectedAccountId])

  const selectedAccount = accounts.find(acc => acc.id === selectedAccountId)

  const totalCredits = transactions
    .filter(t => t.type === "CREDIT")
    .reduce((sum, t) => sum + t.amount, 0)

  const totalDebits = transactions
    .filter(t => t.type === "DEBIT")
    .reduce((sum, t) => sum + t.amount, 0)

  const handlePrint = () => {
    const printContent = printRef.current
    if (!printContent) return

    const printWindow = window.open("", "_blank")
    if (!printWindow) return

    printWindow.document.write(`
      <html>
        <head>
          <title>Account Statement - ${selectedAccount?.id.substring(0, 8)}</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #f5f5f5; }
            .credit { color: #22c55e; }
            .debit { color: #333; }
            .header-info { margin-bottom: 20px; }
            .header-info p { margin: 5px 0; }
            .summary { background: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .summary-item { display: inline-block; margin-right: 40px; }
          </style>
        </head>
        <body>
          <h1>Account Statement</h1>
          <div class="header-info">
            <p><strong>Account ID:</strong> ${selectedAccount?.id}</p>
            <p><strong>Currency:</strong> ${selectedAccount?.currency}</p>
            <p><strong>Current Balance:</strong> $${selectedAccount?.balance.toFixed(2)}</p>
            <p><strong>Statement Date:</strong> ${new Date().toLocaleDateString()}</p>
          </div>
          <div class="summary">
            <div class="summary-item"><strong>Total Credits:</strong> $${totalCredits.toFixed(2)}</div>
            <div class="summary-item"><strong>Total Debits:</strong> $${totalDebits.toFixed(2)}</div>
            <div class="summary-item"><strong>Transactions:</strong> ${transactions.length}</div>
          </div>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Reference</th>
                <th>Type</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              ${transactions.map(t => `
                <tr>
                  <td>${new Date(t.created_at).toLocaleDateString()}</td>
                  <td>${t.reference || "-"}</td>
                  <td>${t.type}</td>
                  <td class="${t.type === "CREDIT" ? "credit" : "debit"}">
                    ${t.type === "CREDIT" ? "+" : "-"}$${t.amount.toFixed(2)}
                  </td>
                  <td>${t.status}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
          <p style="margin-top: 30px; font-size: 12px; color: #666;">
            Generated on ${new Date().toLocaleString()} - BankFlow
          </p>
        </body>
      </html>
    `)
    printWindow.document.close()
    printWindow.print()
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
          <h1 className="text-2xl font-bold text-foreground">Account Statements</h1>
          <p className="text-sm text-muted-foreground">View and print your account statements</p>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-4 rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              {error}
            </div>
          )}

          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Select Account</CardTitle>
              <CardDescription>Choose an account to view statement</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-4 md:flex-row md:items-end">
                <div className="flex-1 space-y-2">
                  <Label>Account</Label>
                  <Select value={selectedAccountId} onValueChange={setSelectedAccountId}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select an account" />
                    </SelectTrigger>
                    <SelectContent>
                      {accounts.map((account) => (
                        <SelectItem key={account.id} value={account.id}>
                          {account.currency} - ${account.balance.toFixed(2)} ({account.id.substring(0, 8)}...)
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <Button onClick={handlePrint} disabled={!selectedAccountId || transactions.length === 0}>
                  <Printer className="mr-2 h-4 w-4" />
                  Print Statement
                </Button>
              </div>
            </CardContent>
          </Card>

          {selectedAccount && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Statement Summary</CardTitle>
                <CardDescription>Account overview for selected period</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-4">
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <FileText className="mb-2 h-5 w-5 text-accent" />
                    <p className="text-sm font-medium text-muted-foreground">Current Balance</p>
                    <p className="text-2xl font-bold text-foreground">
                      ${selectedAccount.balance.toFixed(2)}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <p className="text-sm font-medium text-muted-foreground">Total Credits</p>
                    <p className="text-2xl font-bold text-accent">${totalCredits.toFixed(2)}</p>
                  </div>
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <p className="text-sm font-medium text-muted-foreground">Total Debits</p>
                    <p className="text-2xl font-bold text-foreground">${totalDebits.toFixed(2)}</p>
                  </div>
                  <div className="rounded-lg border border-border bg-muted/50 p-4">
                    <p className="text-sm font-medium text-muted-foreground">Transactions</p>
                    <p className="text-2xl font-bold text-foreground">{transactions.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          <Card ref={printRef}>
            <CardHeader>
              <CardTitle>Transaction History</CardTitle>
              <CardDescription>
                {transactions.length} transactions found
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoadingTransactions ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-accent" />
                </div>
              ) : transactions.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">
                  No transactions found for this account
                </p>
              ) : (
                <div className="space-y-3">
                  {transactions.map((transaction) => (
                    <div
                      key={transaction.id}
                      className="flex items-center justify-between rounded-lg border border-border bg-card p-4"
                    >
                      <div className="flex items-center gap-4">
                        <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${
                          transaction.type === "CREDIT" ? "bg-accent/10" : "bg-muted"
                        }`}>
                          <FileText className={`h-5 w-5 ${
                            transaction.type === "CREDIT" ? "text-accent" : "text-foreground"
                          }`} />
                        </div>
                        <div>
                          <p className="font-medium text-foreground">
                            {transaction.reference || transaction.type}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {new Date(transaction.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <p className={`font-semibold ${
                            transaction.type === "CREDIT" ? "text-accent" : "text-foreground"
                          }`}>
                            {transaction.type === "CREDIT" ? "+" : "-"}${transaction.amount.toFixed(2)}
                          </p>
                          <Badge variant="secondary" className="text-xs">
                            {transaction.status.toLowerCase()}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
