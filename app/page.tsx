"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Building2, Lock, Mail, User, Phone, ArrowLeft } from "lucide-react"
import { useToast } from "@/hooks/useToast"
import { loginUser, registerUser, verifyEmail, resendOTP } from "@/services/auth.service"
import { AxiosError } from "axios"

export default function LoginPage() {
  const router = useRouter()
  const { toast } = useToast()
  
  // Form mode: 'signin', 'signup', or 'otp'
  const [mode, setMode] = useState<'signin' | 'signup' | 'otp'>('signin')
  
  // Sign In fields
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  
  // Sign Up fields
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [signUpEmail, setSignUpEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [signUpPassword, setSignUpPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  
  // OTP fields
  const [otpCode, setOtpCode] = useState(["", "", "", "", "", ""])
  const [pendingEmail, setPendingEmail] = useState("")
  const [resendCooldown, setResendCooldown] = useState(0)
  const otpInputRefs = useRef<(HTMLInputElement | null)[]>([])
  
  const [isLoading, setIsLoading] = useState(false)

  // Resend cooldown timer
  useEffect(() => {
    if (resendCooldown > 0) {
      const timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [resendCooldown])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const token = await loginUser(email, password)
      
      toast({
        title: "Login successful",
        description: `Welcome back!`,
      })
      
      // Redirect based on role
      if (token.role === "admin") {
        router.push("/admin")
      } else {
        router.push("/client")
      }
    } catch (error) {
      let errorMessage = "Invalid email or password"
      
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
        
        // If email not verified, switch to OTP mode
        if (errorMessage.includes("verify your email")) {
          setPendingEmail(email)
          setMode('otp')
          setResendCooldown(0)
          toast({
            title: "Email not verified",
            description: "Please enter the verification code sent to your email.",
          })
        }
      }
      
      if (mode !== 'otp') {
        toast({
          title: "Login failed",
          description: errorMessage,
          variant: "destructive",
        })
      }
      setIsLoading(false)
    }
  }

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate passwords match
    if (signUpPassword !== confirmPassword) {
      toast({
        title: "Sign up failed",
        description: "Passwords do not match",
        variant: "destructive",
      })
      return
    }
    
    setIsLoading(true)

    try {
      await registerUser({
        first_name: firstName,
        last_name: lastName,
        email: signUpEmail,
        phone: phone,
        password: signUpPassword,
        confirm_password: confirmPassword,
      })
      
      toast({
        title: "Account created",
        description: "Please enter the verification code sent to your email.",
      })
      
      // Switch to OTP verification mode
      setPendingEmail(signUpEmail)
      setMode('otp')
      setResendCooldown(60) // 60 second cooldown for resend
      
    } catch (error) {
      let errorMessage = "Failed to create account"
      
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      
      toast({
        title: "Sign up failed",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleOtpChange = (index: number, value: string) => {
    // Only allow digits
    if (value && !/^\d+$/.test(value)) return
    
    const newOtp = [...otpCode]
    newOtp[index] = value.slice(-1) // Take only the last character
    setOtpCode(newOtp)
    
    // Auto-focus next input
    if (value && index < 5) {
      otpInputRefs.current[index + 1]?.focus()
    }
  }

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    // Handle backspace
    if (e.key === "Backspace" && !otpCode[index] && index > 0) {
      otpInputRefs.current[index - 1]?.focus()
    }
  }

  const handleOtpPaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text").slice(0, 6)
    if (!/^\d+$/.test(pastedData)) return
    
    const newOtp = [...otpCode]
    for (let i = 0; i < pastedData.length && i < 6; i++) {
      newOtp[i] = pastedData[i]
    }
    setOtpCode(newOtp)
    
    // Focus the next empty input or the last one
    const nextEmpty = newOtp.findIndex(v => !v)
    otpInputRefs.current[nextEmpty === -1 ? 5 : nextEmpty]?.focus()
  }

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const code = otpCode.join("")
    if (code.length !== 6) {
      toast({
        title: "Invalid code",
        description: "Please enter the complete 6-digit code",
        variant: "destructive",
      })
      return
    }
    
    setIsLoading(true)

    try {
      const result = await verifyEmail({
        email: pendingEmail,
        code: code,
      })
      
      if (result.success) {
        toast({
          title: "Email verified",
          description: "Your email has been verified. You can now sign in.",
        })
        
        // Switch to sign in mode and pre-fill email
        setEmail(pendingEmail)
        setMode('signin')
        
        // Clear sign up and OTP fields
        setFirstName("")
        setLastName("")
        setSignUpEmail("")
        setPhone("")
        setSignUpPassword("")
        setConfirmPassword("")
        setOtpCode(["", "", "", "", "", ""])
        setPendingEmail("")
      } else {
        toast({
          title: "Verification failed",
          description: result.message,
          variant: "destructive",
        })
      }
    } catch (error) {
      let errorMessage = "Failed to verify code"
      
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      
      toast({
        title: "Verification failed",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleResendOtp = async () => {
    if (resendCooldown > 0) return
    
    setIsLoading(true)

    try {
      await resendOTP({ email: pendingEmail })
      
      toast({
        title: "Code sent",
        description: "A new verification code has been sent to your email.",
      })
      
      setResendCooldown(60)
      setOtpCode(["", "", "", "", "", ""])
      
    } catch (error) {
      let errorMessage = "Failed to resend code"
      
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      
      toast({
        title: "Resend failed",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleBackFromOtp = () => {
    setMode('signin')
    setOtpCode(["", "", "", "", "", ""])
    setPendingEmail("")
  }

  const switchMode = (newMode: 'signin' | 'signup') => {
    setMode(newMode)
    setIsLoading(false)
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

        {mode !== 'otp' && (
          /* Mode Toggle Buttons */
          <div className="mb-4 flex rounded-lg bg-muted p-1">
            <Button
              type="button"
              variant={mode === 'signin' ? 'default' : 'ghost'}
              className="flex-1"
              onClick={() => switchMode('signin')}
            >
              Sign In
            </Button>
            <Button
              type="button"
              variant={mode === 'signup' ? 'default' : 'ghost'}
              className="flex-1"
              onClick={() => switchMode('signup')}
            >
              Sign Up
            </Button>
          </div>
        )}

        <Card>
          {mode === 'signin' ? (
            <>
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
                </CardFooter>
              </form>
            </>
          ) : mode === 'signup' ? (
            <>
              <CardHeader>
                <CardTitle>Create Account</CardTitle>
                <CardDescription>Fill in your details to create a new account</CardDescription>
              </CardHeader>
              <form onSubmit={handleSignUp}>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="firstName">First Name</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="firstName"
                          type="text"
                          placeholder="John"
                          value={firstName}
                          onChange={(e) => setFirstName(e.target.value)}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="lastName">Last Name</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="lastName"
                          type="text"
                          placeholder="Doe"
                          value={lastName}
                          onChange={(e) => setLastName(e.target.value)}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="signUpEmail">Email</Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="signUpEmail"
                        type="email"
                        placeholder="your@email.com"
                        value={signUpEmail}
                        onChange={(e) => setSignUpEmail(e.target.value)}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone Number</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="phone"
                        type="tel"
                        placeholder="+1 234 567 890"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="signUpPassword">Password</Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="signUpPassword"
                        type="password"
                        placeholder="••••••••"
                        value={signUpPassword}
                        onChange={(e) => setSignUpPassword(e.target.value)}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword">Confirm Password</Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4  text-muted-foreground" />
                      <Input
                        id="confirmPassword"
                        type="password"
                        placeholder="••••••••"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex flex-col gap-4">
                  <Button type="submit" className="w-full" disabled={isLoading}>
                    {isLoading ? "Creating account..." : "Create Account"}
                  </Button>
                </CardFooter>
              </form>
            </>
          ) : (
            /* OTP Verification Mode */
            <>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={handleBackFromOtp}
                    className="h-8 w-8"
                  >
                    <ArrowLeft className="h-4 w-4 colo" />
                  </Button>
                  <div>
                    <CardTitle>Verify Your Email</CardTitle>
                    <CardDescription>
                      Enter the 6-digit code sent to {pendingEmail}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <form onSubmit={handleVerifyOtp}>
                <CardContent className="space-y-6">
                  <div className="flex justify-center gap-2">
                    {otpCode.map((digit, index) => (
                      <Input
                        key={index}
                        ref={(el) => { otpInputRefs.current[index] = el }}
                        type="text"
                        inputMode="numeric"
                        maxLength={1}
                        value={digit}
                        onChange={(e) => handleOtpChange(index, e.target.value)}
                        onKeyDown={(e) => handleOtpKeyDown(index, e)}
                        onPaste={index === 0 ? handleOtpPaste : undefined}
                        className="h-12 w-12 text-center text-xl font-semibold"
                        required
                      />
                    ))}
                  </div>
                  <div className="text-center text-sm text-muted-foreground">
                    Didn&apos;t receive the code?{" "}
                    <button
                      type="button"
                      onClick={handleResendOtp}
                      disabled={resendCooldown > 0 || isLoading}
                      className="text-accent hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {resendCooldown > 0 ? `Resend in ${resendCooldown}s` : "Resend"}
                    </button>
                  </div>
                </CardContent>
                <CardFooter className="flex flex-col gap-4">
                  <Button type="submit" className="w-full" disabled={isLoading}>
                    {isLoading ? "Verifying..." : "Verify Email"}
                  </Button>
                </CardFooter>
              </form>
            </>
          )}
        </Card>

      </div>
    </div>
  )
}
