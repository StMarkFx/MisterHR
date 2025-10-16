# MisterHR Frontend - Next.js Application

*Modern React application for the AI-powered hiring platform featuring TypeScript, Tailwind CSS, and shadcn/ui components*

[![Next.js](https://img.shields.io/badge/Next.js-15.5.5-000000.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.1.0-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0-38bdf8.svg)](https://tailwindcss.com/)

---

## 📋 **Table of Contents**
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [🎨 UI Components](#-ui-components)
- [📱 Pages & Routes](#-pages--routes)
- [🧪 Testing](#-testing)
- [📚 Documentation](#-documentation)

---

## ✨ **Features**

### **Core Functionality**
- **Resume Upload Interface** - Drag-and-drop file upload for PDF/DOCX CVs
- **Job Description Analysis** - AI-powered job requirements extraction
- **Real-time Matching** - Live candidate-job fit calculations
- **Content Generation** - AI-tailored resume and cover letter creation

### **User Experience**
- **Responsive Design** - Mobile-first approach with adaptive layouts
- **Dark/Light Theme** - System preference detection with manual toggle
- **Progressive Loading** - Smooth animations and skeleton states
- **Accessible UI** - WCAG 2.1 AA compliance with shadcn/ui components

### **Technical Features**
- **Type-Safe APIs** - End-to-end TypeScript with Zod validation
- **Modern React Patterns** - Server/client components, Suspense, Error boundaries
- **Performance Optimized** - Image optimization, bundle splitting, caching
- **Development Experience** - Hot reload, ESLint, Turbopack bundling

---

## 🏗️ **Architecture**

### **Technology Stack**
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Framework** | Next.js | 15.5.5 | React framework with App Router |
| **Language** | TypeScript | 5.0 | Type-safe JavaScript |
| **Styling** | Tailwind CSS | 4.0 | Utility-first CSS framework |
| **UI Components** | shadcn/ui | - | Accessible component library |
| **Forms** | React Hook Form | 7.65.0 | Performant form management |
| **Validation** | Zod | 4.1.12 | Schema validation |
| **State Management** | Zustand | - | Client-side state (planned) |
| **API Layer** | SWR | - | Server state management (planned) |

### **Project Structure**
```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Authentication routes (grouped)
│   │   │   ├── register/
│   │   │   │   └── page.tsx   # Registration page
│   │   ├── dashboard/         # Protected dashboard routes
│   │   │   └── page.tsx       # User dashboard
│   │   ├── resume/            # Resume processing routes
│   │   │   ├── upload/
│   │   │   │   └── page.tsx   # File upload interface
│   │   ├── globals.css        # Global styles & Tailwind
│   │   ├── layout.tsx         # Root layout component
│   │   ├── page.tsx           # Homepage
│   │   └── loading.tsx        # Global loading component
│   ├── components/            # Reusable React components
│   │   ├── ui/                # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── progress.tsx
│   │   │   └── ...
│   │   └── layout/            # Layout components
│   ├── lib/                   # Utilities and configuration
│   │   ├── config.ts          # App configuration
│   │   ├── types.ts           # TypeScript type definitions
│   │   ├── providers.tsx      # React context providers
│   │   └── utils.ts           # Utility functions
│   └── hooks/                 # Custom React hooks (planned)
├── public/                    # Static assets
├── package.json               # Dependencies and scripts
├── tailwind.config.ts         # Tailwind CSS configuration
├── next.config.ts             # Next.js configuration
└── tsconfig.json              # TypeScript configuration
```

---

## 🚀 **Quick Start**

### **Prerequisites**
- Node.js 18+
- npm or yarn

### **Local Development**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### **Build for Production**
```bash
# Build the application
npm run build

# Start production server
npm start

# Or deploy to Vercel
npm run deploy
```

### **Environment Configuration**
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

---

## 🎨 **UI Components**

### **Design System**

#### **Color Palette**
- **Primary**: Indigo (#6366f1) for interactive elements
- **Secondary**: Slate (#64748b) for supporting elements
- **Success**: Emerald (#10b981) for positive actions
- **Warning**: Amber (#f59e0b) for caution states
- **Error**: Red (#ef4444) for error states

#### **Typography**
- **Font Family**: Geist Sans (Google Fonts)
- **Scale**: Consistent text sizing with Tailwind classes
- **Accessibility**: Minimum contrast ratio of 4.5:1

### **Component Library**
Built with shadcn/ui components featuring:
- **Buttons** - Multiple variants with loading states
- **Forms** - Validation, error handling, and accessibility
- **Cards** - Content containers with consistent styling
- **Progress** - File upload and processing indicators
- **Dialogs** - Modal overlays for confirmations
- **Navigation** - Responsive header and breadcrumbs

---

## 📱 **Pages & Routes**

### **Public Routes**
- **`/`** - Landing page with service overview
- **`/auth/register`** - User registration form
- **`/auth/login`** - User authentication (planned)

### **Protected Routes**
- **`/dashboard`** - User dashboard with analytics
- **`/resume/upload`** - File upload interface
- **`/resume/results/[id]`** - Processing results (planned)
- **`/jobs/analyze`** - Job description analysis (planned)

### **Page Components**

#### **Homepage (`app/page.tsx`)**
```tsx
export default function HomePage() {
  return (
    <div className="container mx-auto px-4">
      <HeroSection />
      <FeaturesSection />
      <PricingSection />
    </div>
  )
}
```

#### **Resume Upload (`app/resume/upload/page.tsx`)**
```tsx
'use client'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  const handleUpload = async () => {
    setUploading(true)
    // Upload and processing logic
  }

  return (
    <div className="max-w-2xl mx-auto">
      <FileUploadArea onFileSelect={setFile} />
      <ProgressBar progress={75} />
      <ResultsDisplay data={results} />
    </div>
  )
}
```

---

## 🧪 **Testing**

### **Test Setup**
```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### **Test Categories**
- **Unit Tests**: Component functionality and utilities
- **Integration Tests**: User flows and API interactions
- **E2E Tests**: Full application workflows (planned)
- **Accessibility Tests**: WCAG compliance verification

### **Testing Tools**
- **Framework**: Jest + React Testing Library
- **Coverage**: Minimum 80% target
- **Linting**: ESLint with React rules
- **Type Checking**: TypeScript compiler checks

---

## 📚 **Documentation**

### **Component Documentation**
Each component includes:
- **TypeScript interfaces** for props and state
- **JSDoc comments** explaining functionality
- **Usage examples** in component files
- **Storybook stories** (planned)

### **Development Guidelines**
- **Component Composition**: Prefer composition over inheritance
- **Performance**: Memoize expensive operations with `useMemo`
- **Accessibility**: Include ARIA labels and keyboard navigation
- **Responsive Design**: Mobile-first with breakpoint utilities

---

## 🔧 **Development**

### **Adding a New Component**

1. **Create Component File**
```tsx
// src/components/ui/new-component.tsx
interface NewComponentProps {
  title: string
  onClick: () => void
}

export function NewComponent({ title, onClick }: NewComponentProps) {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
    >
      {title}
    </button>
  )
}
```

2. **Export from UI Index**
```tsx
// src/components/ui/index.ts
export { NewComponent } from './new-component'
```

3. **Add to Component Library** (if shadcn/ui style)
```bash
npx shadcn@latest add new-component
```

### **Adding a New Page**

1. **Create Directory Structure**
```bash
mkdir -p src/app/new-route
touch src/app/new-route/page.tsx
```

2. **Implement Page Component**
```tsx
// src/app/new-route/page.tsx
export default function NewRoutePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">New Route</h1>
      {/* Page content */}
    </div>
  )
}
```

---

## 📊 **Performance**

### **Optimization Strategies**
- **Image Optimization**: Next.js automatic optimization
- **Bundle Splitting**: Automatic code splitting by routes
- **Caching**: Static generation where possible
- **Lazy Loading**: Dynamic imports for heavy components

### **Performance Metrics**
- **First Contentful Paint**: <1.5s target
- **Lighthouse Score**: >90 overall target
- **Bundle Size**: <500KB for main bundle
- **Runtime Performance**: Smooth 60fps animations

---

## 🔒 **Security**

### **Frontend Security**
- **Content Security Policy** (CSP) headers
- **Input Sanitization** in components
- **Secure API communications** with HTTPS
- **Authentication flow** protection

### **Data Protection**
- **No sensitive data** in local storage
- **Secure token handling** with httpOnly cookies (planned)
- **Input validation** with Zod schemas
- **XSS prevention** with proper escaping

---

## 📱 **Responsive Design**

### **Breakpoint Strategy**
- **Mobile**: < 768px (sm)
- **Tablet**: 768px - 1024px (md)
- **Desktop**: > 1024px (lg)
- **Large Desktop**: > 1280px (xl)

### **Responsive Patterns**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid that adapts to screen size */}
</div>
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Build Errors**
- Clear `.next` cache: `rm -rf .next`
- Check TypeScript errors: `npm run type-check`
- Verify Node.js version compatibility

#### **Styling Issues**
- Check Tailwind classes are included in `globals.css`
- Verify component imports in consuming files
- Use browser dev tools to inspect CSS

#### **Component Rendering**
- Check prop types match interface definitions
- Verify component is properly imported and used
- Debug with React DevTools

---

## 🤝 **Contributing**

### **Frontend Development Principles**
1. **Accessibility First**: WCAG AA compliance requirement
2. **Performance Conscious**: Optimize for Core Web Vitals
3. **Type Safety**: Leverage TypeScript for reliability
4. **Consistent Styling**: Use design system consistently
5. **User Experience**: Prioritize usability and feedback

### **Code Standards**
- **Linting**: ESLint with Next.js rules
- **Formatting**: Consistent formatting (Prettier planned)
- **Testing**: 80%+ coverage requirement
- **Documentation**: JSDoc for component APIs

---

## 📈 **Roadmap**

### **Immediate Priorities**
- [x] Core component library setup
- [x] Resume upload functionality
- [x] Basic responsive design
- [ ] User dashboard implementation
- [ ] Authentication system integration
- [ ] Real-time processing feedback

### **Short Term Goals**
- [ ] Advanced UI animations and transitions
- [ ] Offline functionality and caching
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

### **Future Enhancements**
- [ ] Progressive Web App (PWA) capabilities
- [ ] Advanced drag-and-drop interfaces
- [ ] Collaborative features for recruiters
- [ ] Integration with job board APIs

---

Built with ❤️ to empower the hiring process ✨
