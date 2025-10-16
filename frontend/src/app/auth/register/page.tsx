'use client'

import Link from 'next/link'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Eye, EyeOff, Mail, Lock, User, Briefcase, AlertCircle, Brain, Check } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { UserRole } from '@/lib/types'

export default function RegisterPage() {
  const router = useRouter()
  const [step, setStep] = useState<'role' | 'details'>('role')
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [selectedRole, setSelectedRole] = useState<UserRole | null>(null)
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  })

  const handleRoleSelect = (role: UserRole) => {
    setSelectedRole(role)
  }

  const handleNext = () => {
    if (!selectedRole) return
    setStep('details')
  }

  const handleBack = () => {
    setStep('role')
    setError('')
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
    if (error) setError('')
  }

  const validateForm = () => {
    if (!formData.firstName || !formData.lastName) {
      throw new Error('Please fill in your full name')
    }
    if (!formData.email) {
      throw new Error('Please enter your email address')
    }
    if (!formData.password) {
      throw new Error('Please enter a password')
    }
    if (formData.password.length < 8) {
      throw new Error('Password must be at least 8 characters')
    }
    if (formData.password !== formData.confirmPassword) {
      throw new Error('Passwords do not match')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      validateForm()

      // Placeholder for registration logic
      // This will integrate with Supabase Auth later

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Success - redirect to dashboard or verification page
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gradient-from via-white to-gradient-to px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-brand-orange p-3 rounded-xl shadow-lg">
              <Brain className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold mb-2 text-brand-navy">Join MisterHR</h1>
          <p className="text-gray-600">
            Start your AI-powered career transformation
          </p>
        </div>

        {/* Registration Form */}
        <Card className="shadow-lg border-0">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl font-semibold">Create Account</CardTitle>
            <CardDescription>
              {step === 'role' ? 'Choose your role to get started' : 'Enter your details'}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Step Indicator */}
            <div className="flex items-center justify-center space-x-2">
              <Badge variant={step === 'role' ? 'default' : 'secondary'} className="w-8 h-8 rounded-full flex items-center justify-center">1</Badge>
              <div className="w-12 h-0.5 bg-gray-300 dark:bg-gray-600"></div>
              <Badge variant={step === 'details' ? 'default' : 'secondary'} className="w-8 h-8 rounded-full flex items-center justify-center">2</Badge>
            </div>

            {/* Role Selection Step */}
            {step === 'role' && (
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground text-center">
                  How do you plan to use MisterHR?
                </p>

                <div className="grid gap-3">
                  <button
                    onClick={() => handleRoleSelect('applicant')}
                    className={`p-4 rounded-lg border-2 transition-all hover:scale-105 ${
                      selectedRole === 'applicant'
                        ? 'border-brand-orange bg-brand-orange/10'
                        : 'border-gray-200 hover:border-brand-orange/50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <User className={`h-6 w-6 ${selectedRole === 'applicant' ? 'text-brand-orange' : 'text-gray-500'}`} />
                      <div className="text-left">
                        <div className="font-medium text-brand-navy">Job Applicant</div>
                        <div className="text-sm text-gray-600">Optimize resumes & find opportunities</div>
                      </div>
                      {selectedRole === 'applicant' && (
                        <Check className="h-5 w-5 text-brand-orange ml-auto" />
                      )}
                    </div>
                  </button>

                  <button
                    onClick={() => handleRoleSelect('recruiter')}
                    className={`p-4 rounded-lg border-2 transition-all hover:scale-105 ${
                      selectedRole === 'recruiter'
                        ? 'border-brand-orange bg-brand-orange/10'
                        : 'border-gray-200 hover:border-brand-orange/50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Briefcase className={`h-6 w-6 ${selectedRole === 'recruiter' ? 'text-brand-orange' : 'text-gray-500'}`} />
                      <div className="text-left">
                        <div className="font-medium text-brand-navy">Recruiter</div>
                        <div className="text-sm text-gray-600">Find and evaluate candidates faster</div>
                      </div>
                      {selectedRole === 'recruiter' && (
                        <Check className="h-5 w-5 text-brand-orange ml-auto" />
                      )}
                    </div>
                  </button>
                </div>

                <Button
                  onClick={handleNext}
                  className="w-full"
                  disabled={!selectedRole}
                >
                  Continue →
                </Button>
              </div>
            )}

            {/* Details Form Step */}
            {step === 'details' && (
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Error Alert */}
                {error && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                {/* Name Fields */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName">First Name</Label>
                    <Input
                      id="firstName"
                      name="firstName"
                      placeholder="John"
                      value={formData.firstName}
                      onChange={handleChange}
                      disabled={isLoading}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input
                      id="lastName"
                      name="lastName"
                      placeholder="Doe"
                      value={formData.lastName}
                      onChange={handleChange}
                      disabled={isLoading}
                      required
                    />
                  </div>
                </div>

                {/* Email Field */}
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="john@example.com"
                      className="pl-10"
                      value={formData.email}
                      onChange={handleChange}
                      disabled={isLoading}
                      required
                    />
                  </div>
                </div>

                {/* Password Fields */}
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      placeholder="Create a strong password"
                      className="pl-10 pr-10"
                      value={formData.password}
                      onChange={handleChange}
                      disabled={isLoading}
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                      disabled={isLoading}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Must be at least 8 characters long
                  </p>
                </div>

                {/* Confirm Password */}
                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      placeholder="Confirm your password"
                      className="pl-10"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      disabled={isLoading}
                      required
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleBack}
                    disabled={isLoading}
                    className="flex-1"
                  >
                    ← Back
                  </Button>
                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="flex-[2]"
                  >
                    {isLoading ? (
                      <>
                        <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-white"></div>
                        Creating Account...
                      </>
                    ) : (
                      'Create Account'
                    )}
                  </Button>
                </div>
              </form>
            )}

            {/* Separator */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <Separator />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  Already have an account?
                </span>
              </div>
            </div>

            {/* Login Link */}
            <div className="text-center">
              <Link
                href="/auth/login"
                className="text-brand-orange hover:text-brand-orange-dark font-medium transition-colors"
              >
                Sign in instead →
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Back to Home */}
        <div className="text-center mt-8">
          <Link
            href="/"
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  )
}
