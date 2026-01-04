"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/useToast"
import { useRouter } from "next/navigation"
import { useState, useRef } from "react"
import { Loader2, ArrowLeft, Shield, Mail, KeyRound, CheckCircle } from "lucide-react"
import Link from "next/link"
import { forgotPassword, resetPassword } from "@/services/auth.service"
import { AxiosError } from "axios"

type Step = 'email' | 'otp' | 'newPassword' | 'success'

export default function ForgotPasswordPage() {
  const router = useRouter()
  const { toast } = useToast()
  
  // Step state
  const [step, setStep] = useState<Step>('email')
  const [isLoading, setIsLoading] = useState(false)
  
  // Form state
  const [email, setEmail] = useState("")
  const [otpCode, setOtpCode] = useState(["", "", "", "", "", ""])
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  
  // OTP refs
  const otpInputRefs = useRef<(HTMLInputElement | null)[]>([])

  // Handle OTP input change
  const handleOtpChange = (index: number, value: string) => {
    if (value && !/^\d+$/.test(value)) return
    
    const newOtp = [...otpCode]
    newOtp[index] = value.slice(-1)
    setOtpCode(newOtp)
    
    if (value && index < 5) {
      otpInputRefs.current[index + 1]?.focus()
    }
  }

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
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
    
    const nextEmpty = newOtp.findIndex(v => !v)
    otpInputRefs.current[nextEmpty === -1 ? 5 : nextEmpty]?.focus()
  }

  // Step 1: Request password reset (send OTP)
  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!email) {
      toast({
        title: "Email required",
        description: "Please enter your email address",
        variant: "destructive",
      })
      return
    }

    try {
      setIsLoading(true)
      await forgotPassword({ email })
      setStep('otp')
      toast({
        title: "Code sent",
        description: "A verification code has been sent to your email.",
      })
    } catch (error) {
      let errorMessage = "Failed to send reset code"
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Step 2: Verify OTP and go to password step
  const handleVerifyOtp = () => {
    const code = otpCode.join("")
    if (code.length !== 6) {
      toast({
        title: "Invalid code",
        description: "Please enter the complete 6-digit code",
        variant: "destructive",
      })
      return
    }
    setStep('newPassword')
  }

  // Step 3: Reset password with OTP
  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (newPassword.length < 8) {
      toast({
        title: "Password too short",
        description: "Password must be at least 8 characters",
        variant: "destructive",
      })
      return
    }
    
    if (newPassword !== confirmPassword) {
      toast({
        title: "Passwords don't match",
        description: "Please make sure your passwords match",
        variant: "destructive",
      })
      return
    }

    try {
      setIsLoading(true)
      const code = otpCode.join("")
      await resetPassword({
        email,
        code,
        new_password: newPassword,
        confirm_password: confirmPassword,
      })
      setStep('success')
      toast({
        title: "Password reset successful",
        description: "Your password has been changed successfully.",
      })
    } catch (error) {
      let errorMessage = "Failed to reset password"
      if (error instanceof AxiosError && error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleBackToEmail = () => {
    setStep('email')
    setOtpCode(["", "", "", "", "", ""])
  }

  const handleResendCode = async () => {
    try {
      setIsLoading(true)
      await forgotPassword({ email })
      setOtpCode(["", "", "", "", "", ""])
      toast({
        title: "Code resent",
        description: "A new verification code has been sent to your email.",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to resend code. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-background to-muted/30 p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-foreground">SecureBank</h1>
          <p className="text-muted-foreground">Password Recovery</p>
        </div>

        {/* Step: Email */}
        {step === 'email' && (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-accent/10">
                <Mail className="h-8 w-8 text-accent" />
              </div>
              <CardTitle>Forgot your password?</CardTitle>
              <CardDescription>
                Enter your email address and we'll send you a verification code to reset your password.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleRequestReset} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                
                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Sending code...
                    </>
                  ) : (
                    "Send Reset Code"
                  )}
                </Button>
                
                <div className="text-center">
                  <Link 
                    href="/" 
                    className="text-sm text-muted-foreground hover:text-accent inline-flex items-center gap-1"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    Back to Login
                  </Link>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Step: OTP */}
        {step === 'otp' && (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-accent/10">
                <Shield className="h-8 w-8 text-accent" />
              </div>
              <CardTitle>Enter Verification Code</CardTitle>
              <CardDescription>
                We've sent a 6-digit code to <span className="font-medium text-foreground">{email}</span>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* OTP Input */}
              <div className="space-y-4">
                <div className="flex justify-center gap-2" onPaste={handleOtpPaste}>
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
                      className="h-14 w-12 text-center text-2xl font-bold"
                    />
                  ))}
                </div>
              </div>

              <Button 
                onClick={handleVerifyOtp}
                disabled={otpCode.join("").length !== 6 || isLoading}
                className="w-full"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  "Continue"
                )}
              </Button>

              <div className="text-center space-y-2">
                <p className="text-sm text-muted-foreground">
                  Didn't receive the code?{" "}
                  <button
                    onClick={handleResendCode}
                    disabled={isLoading}
                    className="text-accent hover:underline disabled:opacity-50"
                  >
                    Resend
                  </button>
                </p>
                <button 
                  onClick={handleBackToEmail}
                  className="text-sm text-muted-foreground hover:text-foreground inline-flex items-center gap-1"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Change email
                </button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step: New Password */}
        {step === 'newPassword' && (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-accent/10">
                <KeyRound className="h-8 w-8 text-accent" />
              </div>
              <CardTitle>Create New Password</CardTitle>
              <CardDescription>
                Please enter your new password. Make sure it's at least 8 characters.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleResetPassword} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="newPassword">New Password</Label>
                  <Input
                    id="newPassword"
                    type="password"
                    placeholder="••••••••"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    minLength={8}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={8}
                  />
                </div>

                <div className="rounded-lg border border-border bg-muted/50 p-3">
                  <p className="text-xs text-muted-foreground">
                    Password must be at least 8 characters long and contain a mix of letters, numbers, and special characters for better security.
                  </p>
                </div>
                
                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Resetting password...
                    </>
                  ) : (
                    "Reset Password"
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Step: Success */}
        {step === 'success' && (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-500/10">
                <CheckCircle className="h-8 w-8 text-green-500" />
              </div>
              <CardTitle>Password Reset Successful!</CardTitle>
              <CardDescription>
                Your password has been changed successfully. You can now sign in with your new password.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={() => router.push("/")} className="w-full">
                Back to Login
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
