'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import {
  Brain,
  Upload,
  FileText,
  TrendingUp,
  BarChart3,
  Settings,
  ChevronRight,
  CheckCircle,
  Clock,
  AlertCircle,
  Sparkles
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

// Mock user data - replace with real auth
const mockUser = {
  name: 'John Doe',
  email: 'john.doe@example.com',
  role: 'applicant' as const,
  avatar: null,
  stats: {
    resumesAnalyzed: 3,
    matchesGenerated: 15,
    optimizationScore: 87,
    lastActivity: '2 hours ago',
  },
}

const quickActions = [
  {
    id: 'upload-resume',
    title: 'Upload Resume',
    description: 'Analyze a new resume with AI',
    icon: Upload,
    href: '/resume/upload',
    color: 'bg-brand-orange',
  },
  {
    id: 'job-description',
    title: 'Analyze Job',
    description: 'Evaluate job requirements & skills',
    icon: FileText,
    href: '/job/analyze',
    color: 'bg-brand-green',
  },
  {
    id: 'generate-match',
    title: 'Generate Match',
    description: 'Create tailored resume for position',
    icon: Sparkles,
    href: '/match/generate',
    color: 'bg-brand-amber',
  },
  {
    id: 'view-analytics',
    title: 'View Analytics',
    description: 'Track performance & insights',
    icon: BarChart3,
    href: '/analytics',
    color: 'bg-brand-navy',
  },
]

const recentActivity = [
  {
    id: 1,
    type: 'resume_upload',
    title: 'Resume uploaded successfully',
    description: 'Software Developer Resume analyzed',
    time: '2 hours ago',
    status: 'success',
  },
  {
    id: 2,
    type: 'match_generated',
    title: 'Match generated',
    description: 'Senior Frontend Developer position',
    time: '4 hours ago',
    status: 'success',
  },
  {
    id: 3,
    type: 'job_analyzed',
    title: 'Job description analyzed',
    description: 'Tech Lead requirements processed',
    time: '1 day ago',
    status: 'success',
  },
]

export default function DashboardPage() {
  const router = useRouter()
  const [stats, setStats] = useState(mockUser.stats)

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setStats(prev => ({
        ...prev,
        optimizationScore: Math.min(95, prev.optimizationScore + Math.random() * 2),
      }))
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gradient-from/30 via-white to-gradient-to/30">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="h-6 w-6 text-brand-orange" />
            <span className="text-xl font-bold text-brand-navy">{mockUser.name}</span>
            <Badge className="capitalize bg-brand-orange/10 text-brand-orange hover:bg-brand-orange/20">
              {mockUser.role}
            </Badge>
          </div>

          <div className="flex items-center gap-4">
            <ThemeToggle />

            {/* User Menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={mockUser.avatar || ''} alt={mockUser.name} />
                    <AvatarFallback>
                      {mockUser.name.split(' ').map(n => n[0]).join('')}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <div className="flex flex-col space-y-1 p-2">
                  <p className="text-sm font-medium">{mockUser.name}</p>
                  <p className="text-xs text-muted-foreground">{mockUser.email}</p>
                </div>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => router.push('/settings')}>
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="text-red-600">
                  Sign out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {mockUser.name.split(' ')[0]}! 👋
          </h1>
          <p className="text-muted-foreground">
          Ready to supercharge your career with AI? Here's your activity overview.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
          <Card className="relative overflow-hidden">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Resumes Analyzed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center">
                <div className="text-2xl font-bold">{stats.resumesAnalyzed}</div>
                <CheckCircle className="ml-2 h-4 w-4 text-mr-success-green" />
              </div>
            </CardContent>
          </Card>

          <Card className="relative overflow-hidden">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Matches Generated</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center">
                <div className="text-2xl font-bold">{stats.matchesGenerated}</div>
                <TrendingUp className="ml-2 h-4 w-4 text-mr-energy-blue" />
              </div>
            </CardContent>
          </Card>

          <Card className="relative overflow-hidden">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Optimization Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center">
                <div className="text-2xl font-bold">{Math.round(stats.optimizationScore)}</div>
                <div className="ml-2 text-sm text-muted-foreground">%</div>
              </div>
              <Progress value={stats.optimizationScore} className="mt-2" />
            </CardContent>
          </Card>

          <Card className="relative overflow-hidden">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Last Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center">
                <div className="text-sm font-medium">{stats.lastActivity}</div>
                <Clock className="ml-2 h-4 w-4 text-muted-foreground" />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Quick Actions */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5" />
                  Quick Actions
                </CardTitle>
                <CardDescription>
                  Jump right into the most common tasks
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 sm:grid-cols-2">
                  {quickActions.map((action) => (
                    <Button
                      key={action.id}
                      variant="outline"
                      className="h-auto p-6 justify-start hover:scale-105 transition-transform"
                      onClick={() => router.push(action.href)}
                    >
                      <div className="flex items-start gap-3">
                        <div className={`p-1.5 rounded ${action.color} text-white`}>
                          <action.icon className="h-4 w-4" />
                        </div>
                        <div className="text-left">
                          <div className="font-semibold">{action.title}</div>
                          <div className="text-sm text-muted-foreground">
                            {action.description}
                          </div>
                        </div>
                        <ChevronRight className="h-4 w-4 text-muted-foreground ml-auto" />
                      </div>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>
                  Your latest interactions with AI agents
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivity.map((activity) => (
                    <div key={activity.id} className="flex items-start gap-3">
                      <div className="mt-1">
                        {activity.status === 'success' ? (
                          <CheckCircle className="h-4 w-4 text-mr-success-green" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-mr-neutral-red" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium">{activity.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {activity.description}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* AI Status */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <div className="w-2 h-2 bg-mr-energy-blue rounded-full animate-pulse"></div>
                  AI Service Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Resume Parser</span>
                    <Badge variant="secondary" className="text-xs">Online</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Match Generator</span>
                    <Badge variant="secondary" className="text-xs">Online</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Content Creator</span>
                    <Badge variant="secondary" className="text-xs">Online</Badge>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-3">
                  All AI agents are operating normally
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
