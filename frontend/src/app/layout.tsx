import { Inter, JetBrains_Mono } from 'next/font/google'
import { cn } from '@/lib/utils'
import { Providers } from '@/lib/providers'
import { config } from '@/lib/config'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const jetBrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono'
})

export const metadata = {
  title: config.brand.name,
  description: config.brand.description,
  keywords: ['AI', 'Hiring', 'Resume', 'Recruitment', 'HR', 'Career'],
  authors: [{ name: 'MisterHR Team' }],
  creator: 'MisterHR',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://misterhr.com',
    title: config.brand.name,
    description: config.brand.description,
    siteName: config.brand.name,
  },
  twitter: {
    card: 'summary_large_image',
    title: config.brand.name,
    description: config.brand.description,
    creator: '@misterhr',
  },
  robots: {
    index: true,
    follow: true,
  },
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(
          inter.variable,
          jetBrainsMono.variable,
          'font-sans antialiased'
        )}
      >
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
