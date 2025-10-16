'use client'

import { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Upload, FileText, X, AlertCircle, Brain, Sparkles, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { config } from '@/lib/config'

const ACCEPTED_FILES = config.upload.acceptedExtensions.join(', ')
const MAX_SIZE = config.upload.maxSize / (1024 * 1024)
const ACCEPTED_TYPES = config.upload.acceptedTypes

export default function ResumeUploadPage() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'processing' | 'completed' | 'error'>('idle')
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState('')
  const [processingStatus, setProcessingStatus] = useState('')

  const validateFile = (file: File): string | null => {
    if (!ACCEPTED_TYPES.includes(file.type as typeof ACCEPTED_TYPES[number])) {
      return `Please upload a valid file type: ${ACCEPTED_FILES}`
    }
    if (file.size > config.upload.maxSize) {
      return `File size must be less than ${MAX_SIZE}MB`
    }
    return null
  }

  const handleFileSelect = (selectedFile: File) => {
    const validationError = validateFile(selectedFile)
    if (validationError) {
      setError(validationError)
      return
    }

    setFile(selectedFile)
    setError('')
    setUploadState('idle')
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      handleFileSelect(droppedFile)
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      handleFileSelect(selectedFile)
    }
  }

  const removeFile = () => {
    setFile(null)
    setUploadState('idle')
    setError('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const uploadFile = async () => {
    if (!file) return

    setUploadState('uploading')
    setUploadProgress(0)
    setError('')

    try {
      // Simulate upload progress
      for (let progress = 0; progress <= 100; progress += 10) {
        setUploadProgress(progress)
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      setUploadState('processing')
      setProcessingStatus('Analyzing your resume with AI...')

      // Simulate AI processing
      const processingSteps = [
        'Extracting text and structure...',
        'Identifying key skills and experience...',
        'Analyzing job relevance...',
        'Generating optimization insights...',
        'Creating ATS-friendly format...'
      ]

      for (const step of processingSteps) {
        setProcessingStatus(step)
        await new Promise(resolve => setTimeout(resolve, 1500))
      }

      setUploadState('completed')
      setProcessingStatus('Resume processed successfully!')

      // Auto-redirect to results after success message
      setTimeout(() => {
        router.push('/resume/analyze')
      }, 2000)

    } catch (err) {
      setUploadState('error')
      setError('Upload failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gradient-from/30 via-white to-gradient-to/30 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-brand-orange p-3 rounded-xl shadow-lg">
              <Upload className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold mb-4 text-brand-navy">Upload Your Resume</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Let our AI agents analyze your resume and unlock career optimization insights
          </p>
        </div>

        {/* Upload Area */}
        <div className="grid gap-8 lg:grid-cols-2">
          {/* Upload Card */}
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Resume Upload
              </CardTitle>
            </CardHeader>
            <CardContent>
              {/* Drop Zone */}
              {!file ? (
                <div
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-mr-energy-blue transition-colors cursor-pointer"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-lg font-semibold mb-2">Drop your resume here</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    or click to browse files
                  </p>
                  <div className="flex items-center justify-center gap-2 mb-4">
                    <Badge variant="secondary">{ACCEPTED_FILES}</Badge>
                    <Badge variant="outline">Max {MAX_SIZE}MB</Badge>
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept={ACCEPTED_TYPES.join(',')}
                    onChange={handleFileInput}
                    className="hidden"
                  />
                  <Button variant="outline" size="sm">
                    Browse Files
                  </Button>
                </div>
              ) : (
                /* File Preview */
                <div className="border rounded-lg p-6 bg-gradient-to-r from-mr-energy-blue/5 to-mr-success-green/5">
                  <div className="flex items-center gap-4">
                    <div className="bg-mr-energy-blue p-2 rounded-lg">
                      <FileText className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">{file.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(file.size / (1024 * 1024)).toFixed(1)}MB
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={removeFile}
                      className="text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}

              {/* Error Alert */}
              {error && (
                <Alert variant="destructive" className="mt-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {/* Progress */}
              {uploadState !== 'idle' && (
                <div className="mt-6 space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">
                      {uploadState === 'uploading' && 'Uploading resume...'}
                      {uploadState === 'processing' && 'Processing with AI...'}
                      {uploadState === 'completed' && 'Processing complete!'}
                      {uploadState === 'error' && 'Upload failed'}
                    </span>
                    <Badge variant={
                      uploadState === 'completed' ? 'default' :
                      uploadState === 'error' ? 'destructive' :
                      'secondary'
                    }>
                      {uploadState}
                    </Badge>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                  {processingStatus && (
                    <p className="text-sm text-muted-foreground text-center">
                      {processingStatus}
                    </p>
                  )}
                </div>
              )}

              {/* Action Buttons */}
              <div className="mt-6 flex gap-3">
                {file && uploadState === 'idle' && (
                  <Button
                    onClick={uploadFile}
                    className="flex-1"
                    size="lg"
                  >
                    <Sparkles className="mr-2 h-4 w-4" />
                    Analyze with AI
                  </Button>
                )}
                {file && (
                  <Button
                    variant="outline"
                    onClick={removeFile}
                    disabled={uploadState !== 'idle'}
                  >
                    Remove
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Feature Preview */}
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                What Our AI Does
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="bg-brand-green rounded-full p-1">
                    <CheckCircle className="h-3 w-3 text-white" />
                  </div>
                  <div>
                    <div className="font-medium text-brand-navy">Smart Text Extraction</div>
                    <div className="text-sm text-gray-600">
                      Parses all resume sections accurately
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="bg-brand-orange rounded-full p-1">
                    <CheckCircle className="h-3 w-3 text-white" />
                  </div>
                  <div>
                    <div className="font-medium text-brand-navy">AI Skill Analysis</div>
                    <div className="text-sm text-gray-600">
                      Identifies and categorizes your skills
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="bg-brand-amber rounded-full p-1">
                    <CheckCircle className="h-3 w-3 text-white" />
                  </div>
                  <div>
                    <div className="font-medium text-brand-navy">ATS Optimization</div>
                    <div className="text-sm text-gray-600">
                      Makes your resume ATS-friendly
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="bg-brand-navy rounded-full p-1">
                    <CheckCircle className="h-3 w-3 text-white" />
                  </div>
                  <div>
                    <div className="font-medium text-brand-navy">Career Insights</div>
                    <div className="text-sm text-gray-600">
                      Provides optimization recommendations
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 p-4 bg-gradient-to-r from-brand-orange/10 to-brand-green/10 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles className="h-4 w-4 text-brand-orange" />
                  <span className="font-medium text-sm text-brand-navy">Processing Time</span>
                </div>
                <p className="text-sm text-gray-600">
                  Most resumes are analyzed in under 30 seconds
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Stats */}
        <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-brand-green">90%</div>
            <div className="text-sm text-gray-600">Parse Accuracy</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-brand-orange">30s</div>
            <div className="text-sm text-gray-600">Avg Processing</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-brand-amber">500+</div>
            <div className="text-sm text-gray-600">Keywords Detected</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-brand-navy">100%</div>
            <div className="text-sm text-gray-600">ATS Compatible</div>
          </div>
        </div>
      </div>
    </div>
  )
}
