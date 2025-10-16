import Link from 'next/link'
import { ArrowRight, Sparkles, Brain, TrendingUp, Users, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { config } from '@/lib/config'

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="h-6 w-6 text-brand-orange" />
            <span className="text-xl font-bold text-brand-navy">{config.brand.name}</span>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Button variant="ghost" asChild className="text-brand-navy hover:text-brand-orange">
              <Link href="/auth/login">Sign In</Link>
            </Button>
            <Button asChild className="bg-brand-orange hover:bg-brand-orange-dark text-white">
              <Link href="/auth/register">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section with Gradient Background */}
      <section className="flex-1 flex items-center justify-center px-4 py-16 bg-gradient-to-br from-gradient-from via-white to-gradient-to">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <Badge className="mb-4 bg-brand-orange/10 text-brand-orange hover:bg-brand-orange/20">
              <Sparkles className="mr-2 h-3 w-3" />
              Powered by Advanced AI
            </Badge>
            <h1 className="text-4xl font-bold tracking-tight sm:text-6xl mb-6 text-brand-navy">
              Transform Your Career with
              <span className="text-brand-orange block mt-2">AI Intelligence</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              {config.brand.description} Upload your resume and let our AI agents optimize it for specific job opportunities while streamlining your entire application process.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="text-lg px-8 py-6 bg-brand-orange hover:bg-brand-orange-dark text-white shadow-lg hover:shadow-xl transition-all" asChild>
                <Link href="/auth/register">
                  Start Optimizing
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 py-6 border-brand-orange text-brand-orange hover:bg-brand-orange hover:text-white" asChild>
                <Link href="/demo">
                  View Demo
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50/50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4 text-brand-navy">How It Works</h2>
            <p className="text-lg text-gray-600">
              Our multi-agent AI system handles every aspect of career optimization
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            <Card className="text-center shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-brand-orange rounded-lg flex items-center justify-center mb-4 shadow-md">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-brand-navy">Smart Resume Parsing</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  Upload your resume and our AI extracts key information, skills, and experiences automatically with 90%+ accuracy.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="text-center shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-brand-green rounded-lg flex items-center justify-center mb-4 shadow-md">
                  <TrendingUp className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-brand-navy">AI-Powered Optimization</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  Specify your target job and our agents analyze requirements, suggesting improvements and generating tailored content.
                </CardDescription>
              </CardContent>
            </Card>
            <Card className="text-center shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-brand-amber rounded-lg flex items-center justify-center mb-4 shadow-md">
                  <Users className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-brand-navy">Intelligent Screening</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  For recruiters, batch process resumes with AI matching and ranking to reduce screening time by 70%.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4 text-brand-navy">Trusted by Professionals</h2>
            <p className="text-lg text-gray-600">
              Join thousands of job seekers and recruiters using AI to accelerate hiring
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-brand-navy">
                  <CheckCircle className="h-5 w-5 text-brand-green" />
                  For Job Seekers
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-brand-green flex-shrink-0" />
                    <span className="text-gray-700">AI-powered resume optimization</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-brand-green flex-shrink-0" />
                    <span className="text-gray-700">Real-time match scoring</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-brand-green flex-shrink-0" />
                    <span className="text-gray-700">Career analytics dashboard</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
            <Card className="shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-brand-navy">
                  <CheckCircle className="h-5 w-5 text-brand-green" />
                  For Recruiters
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-brand-green flex-shrink-0" />
                    <span className="text-gray-700">Batch resume processing</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-brand-green flex-shrink-0" />
                    <span className="text-gray-700">Intelligent candidate ranking</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-brand-green flex-shrink-0" />
                    <span className="text-gray-700">Hiring analytics & insights</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-brand-orange to-brand-orange-light">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Your Hiring Process?
          </h2>
          <p className="text-xl text-white/90 mb-8">
            Join the AI-powered revolution in recruitment
          </p>
          <Button size="lg" variant="secondary" className="text-lg px-8 py-6 bg-white text-brand-orange hover:bg-gray-50 shadow-lg" asChild>
            <Link href="/auth/register">
              Start Free Today
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <Brain className="h-5 w-5 text-brand-orange" />
              <span className="font-semibold text-brand-navy">{config.brand.name}</span>
            </div>
            <div className="text-sm text-gray-600">
              Built with ❤️ for career intelligence
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
