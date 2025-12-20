"use client"

import type React from "react"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  ArrowLeftRight,
  Users,
  Receipt,
  DollarSign,
  MessageCircle,
  User,
  LogOut,
  Building2,
  Settings,
  FileText,
  HelpCircle,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface SidebarLink {
  href: string
  label: string
  icon: React.ComponentType<{ className?: string }>
}

interface DashboardSidebarProps {
  role: "client" | "admin"
  onLogout?: () => void
}

const clientLinks: SidebarLink[] = [
  { href: "/client", label: "Dashboard", icon: LayoutDashboard },
  { href: "/client/transfer", label: "Transfer Money", icon: ArrowLeftRight },
  { href: "/client/beneficiaries", label: "Beneficiaries", icon: Users },
  { href: "/client/transactions", label: "Transactions", icon: Receipt },
  { href: "/client/statements", label: "Statements", icon: FileText },
  { href: "/client/exchange-rates", label: "Exchange Rates", icon: DollarSign },
  { href: "/client/contact", label: "Contact Bank", icon: MessageCircle },
  { href: "/client/profile", label: "My Profile", icon: User },
]

const adminLinks: SidebarLink[] = [
  { href: "/admin", label: "Dashboard", icon: LayoutDashboard },
  { href: "/admin/clients", label: "Manage Clients", icon: Users },
  { href: "/admin/accounts", label: "Manage Accounts", icon: Building2 },
  { href: "/admin/requests", label: "Client Requests", icon: HelpCircle },
  { href: "/admin/relationships", label: "Relationships", icon: MessageCircle },
  { href: "/admin/exchange-rates", label: "Exchange Rates", icon: DollarSign },
  { href: "/admin/settings", label: "Settings", icon: Settings },
]

export function DashboardSidebar({ role, onLogout }: DashboardSidebarProps) {
  const pathname = usePathname()
  const links = role === "client" ? clientLinks : adminLinks

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-border bg-card">
      <div className="flex h-16 items-center gap-2 border-b border-border px-6">
        <Building2 className="h-6 w-6 text-accent" />
        <span className="text-lg font-semibold text-foreground">BankFlow</span>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-4">
        {links.map((link) => {
          const Icon = link.icon
          const isActive = pathname === link.href

          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <Icon className="h-4 w-4" />
              {link.label}
            </Link>
          )
        })}
      </nav>

      <div className="border-t border-border p-4">
        <Button
          variant="ghost"
          className="w-full justify-start gap-3 text-muted-foreground hover:text-foreground"
          onClick={onLogout}
        >
          <LogOut className="h-4 w-4" />
          Logout
        </Button>
      </div>
    </aside>
  )
}
