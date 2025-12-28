"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Building2, Lock, Mail } from "lucide-react"
import { useToast } from "@/hooks/useToast"

// This page is for the login functionality for both admin and client users.

const VALID_CREDENTIALS = {
  admin: {
    email: "admin@example.com",
    password: "admin123",
  },
  client: {
    email: "client@example.com",
    password: "client123",
  },
}

export default function LoginPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    setTimeout(() => {
      // Check admin credentials
      if (email === VALID_CREDENTIALS.admin.email && password === VALID_CREDENTIALS.admin.password) {
        toast({
          title: "Login successful",
          description: `Welcome back, Administrator!`,
        })
        router.push("/admin")
      }
      // Check client credentials
      else if (email === VALID_CREDENTIALS.client.email && password === VALID_CREDENTIALS.client.password) {
        toast({
          title: "Login successful",
          description: `Welcome back!`,
        })
        router.push("/client")
      }
      // Invalid credentials
      else {
        toast({
          title: "Login failed",
          description: "Invalid email or password",
          variant: "destructive",
        })
        setIsLoading(false)
      }
    }, 1000)
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-muted/20 to-background p-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-accent">
            <Building2 className="h-8 w-8 text-accent-foreground" />
          </div>
          <h1 className="text-3xl font-bold text-foreground">Welcome to BankFlow</h1>
          <p className="mt-2 text-muted-foreground">Secure online banking at your fingertips</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Sign In</CardTitle>
            <CardDescription>Enter your credentials to access your account</CardDescription>
          </CardHeader>
          <form onSubmit={handleLogin}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              <div className="flex items-center justify-between text-sm">
                <a href="#" className="text-accent hover:underline">
                  Forgot password?
                </a>
              </div>
            </CardContent>
            <CardFooter className="flex flex-col gap-4">
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Signing in..." : "Sign In"}
              </Button>
              <div className="space-y-1 text-center text-xs text-muted-foreground">
                <p className="font-medium">Demo Credentials:</p>
                <p>Admin: admin@example.com / admin123</p>
                <p>Client: client@example.com / client123</p>
              </div>
            </CardFooter>
          </form>
        </Card>

        <p className="mt-8 text-center text-sm text-muted-foreground">Protected by enterprise-grade security</p>
      </div>
    </div>
  )
}
