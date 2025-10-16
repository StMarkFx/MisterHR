import type { Config } from 'tailwindcss'
import tailwindcssAnimate from 'tailwindcss-animate'

/** @type {Config} */
const config: Config = {
  darkMode: 'class',
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: '',
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      // Modern SaaS Color System - Orange/Peach Theme
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary-orange))',
          foreground: 'hsl(0 0% 100%)',
          light: 'hsl(var(--primary-orange-light))',
          dark: 'hsl(var(--primary-orange-dark))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--gradient-peach-from))',
          foreground: 'hsl(var(--navy-trust))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--neutral-red))',
          foreground: 'hsl(0 0% 100%)',
        },
        muted: {
          DEFAULT: 'hsl(var(--gradient-peach-from))',
          foreground: 'hsl(var(--navy-trust) / 0.7)',
        },
        accent: {
          DEFAULT: 'hsl(var(--warm-amber))',
          foreground: 'hsl(0 0% 100%)',
        },
        popover: {
          DEFAULT: 'hsl(0 0% 100%)',
          foreground: 'hsl(var(--navy-trust))',
        },
        card: {
          DEFAULT: 'hsl(0 0% 100%)',
          foreground: 'hsl(var(--navy-trust))',
        },
        // Modern SaaS Brand Tokens
        'brand': {
          orange: 'hsl(var(--primary-orange))',
          'orange-light': 'hsl(var(--primary-orange-light))',
          'orange-dark': 'hsl(var(--primary-orange-dark))',
          peach: 'hsl(var(--gradient-peach-from))',
          'peach-light': 'hsl(var(--gradient-peach-to))',
          navy: 'hsl(var(--navy-trust))',
          green: 'hsl(var(--success-green))',
          amber: 'hsl(var(--warm-amber))',
          red: 'hsl(var(--neutral-red))',
        },
        // Gradient backgrounds
        'gradient-from': 'hsl(var(--gradient-peach-from))',
        'gradient-to': 'hsl(var(--gradient-peach-to))',
        'gradient-orange-from': 'hsl(var(--gradient-orange-from))',
        'gradient-orange-to': 'hsl(var(--gradient-orange-to))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 0.2rem)',
        sm: 'calc(var(--radius) - 0.4rem)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
        'fade-in': {
          '0%': {
            opacity: '0',
          },
          '100%': {
            opacity: '1',
          },
        },
        'slide-in': {
          '0%': {
            transform: 'translateX(-100%)',
          },
          '100%': {
            transform: 'translateX(0)',
          },
        },
        'scale-in': {
          '0%': {
            transform: 'scale(0.95)',
            opacity: '0',
          },
          '100%': {
            transform: 'scale(1)',
            opacity: '1',
          },
        },
        'glow': {
          '0%, 100%': {
            boxShadow: '0 0 5px rgba(14, 165, 233, 0.2)',
          },
          '50%': {
            boxShadow: '0 0 20px rgba(14, 165, 233, 0.5)',
          },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.5s ease-out',
        'slide-in': 'slide-in 0.3s ease-out',
        'scale-in': 'scale-in 0.2s ease-out',
        'glow': 'glow 2s ease-in-out infinite',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['var(--font-jetbrains-mono)', 'JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [tailwindcssAnimate],
}

export default config
