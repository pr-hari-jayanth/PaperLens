import { useState, useRef, useEffect } from 'react'
import { Upload, CheckCircle2, Loader2, Sparkles, AlertCircle, FileText, ArrowDown } from 'lucide-react'

export default function Hero({ onUpload, uploading, error, analysisResult }) {
  const [dragOver, setDragOver] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const inputRef = useRef(null)
  const progressTimer = useRef(null)

  useEffect(() => {
    if (uploading) {
      setUploadProgress(0)
      // Simulate upload progress for UX
      progressTimer.current = setInterval(() => {
        setUploadProgress((p) => Math.min(p + 5, 90))
      }, 400)
    } else {
      clearInterval(progressTimer.current)
      setUploadProgress(100)
    }
    return () => clearInterval(progressTimer.current)
  }, [uploading])

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f && f.type === 'application/pdf') {
      onUpload(f)
    }
  }

  const handleChange = (e) => {
    const f = e.target.files[0]
    if (f) onUpload(f)
  }

  const handleClick = () => {
    if (uploading || analysisResult) return
    inputRef.current?.click()
  }

  const scrollToDashboard = () => {
    document.querySelector('#analysis-results')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <section className="relative pt-24 pb-12 md:pt-28 md:pb-16 px-4">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-radial-glow-hero pointer-events-none" />

      <div className="relative max-w-4xl mx-auto text-center">
        <div
          className="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full text-sm text-gray-300 border border-accent/20 bg-accent/[0.04] animate-fade-in-down"
          style={{ animationDelay: '0.1s', animationFillMode: 'both' }}
        >
          <Sparkles className="w-3.5 h-3.5 text-accent-light" />
          <span>
            <span className="text-accent-light font-medium">v1.0 &mdash;</span>
            Upload a PDF, get instant AI analysis
          </span>
        </div>

        <h1
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-[1.1] tracking-tight text-white animate-fade-in-up"
          style={{ animationDelay: '0.2s', animationFillMode: 'both' }}
        >
          Analyze research papers
          <br />
          with <span className="text-gradient">PaperLens</span>
        </h1>

        <p
          className="mt-6 text-lg md:text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed animate-fade-in-up"
          style={{ animationDelay: '0.35s', animationFillMode: 'both' }}
        >
          Drop a research PDF below and let AI extract structured
          summaries, key findings, methodology, and plain-English
          explanations &mdash; all running locally.
        </p>

        <div
          className="mt-10 animate-fade-in-up"
          style={{ animationDelay: '0.5s', animationFillMode: 'both' }}
        >
          {/* Uploading state */}
          {uploading ? (
            <div className="max-w-lg mx-auto p-8 rounded-2xl border border-accent/20 bg-accent/[0.04]">
              <div className="flex flex-col items-center gap-4">
                <div className="relative">
                  <Loader2 className="w-10 h-10 text-accent-light animate-spin" />
                  <div className="absolute inset-0 bg-accent/20 rounded-full blur-xl animate-glow-pulse" />
                </div>
                <p className="text-white font-medium">Processing with AI&hellip;</p>
                <div className="w-full max-w-xs h-1.5 bg-white/[0.06] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-accent to-accent-light rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="text-sm text-gray-500">
                  {uploadProgress < 30
                    ? 'Uploading PDF&hellip;'
                    : uploadProgress < 70
                      ? 'Extracting text&hellip;'
                      : 'Generating insights&hellip;'}
                </p>
              </div>
            </div>
          ) : analysisResult ? (
            /* Success state */
            <div className="max-w-lg mx-auto p-8 rounded-2xl border border-green-500/20 bg-green-500/[0.04]">
              <div className="flex flex-col items-center gap-4">
                <div className="w-14 h-14 rounded-xl bg-green-500/[0.1] flex items-center justify-center border border-green-500/10">
                  <CheckCircle2 className="w-7 h-7 text-green-400" strokeWidth={1.5} />
                </div>
                <div>
                  <p className="text-white font-medium text-lg">Analysis complete</p>
                  <p className="text-gray-400 text-sm mt-0.5">
                    {analysisResult.title || 'Untitled paper'}
                  </p>
                </div>
                <button
                  onClick={scrollToDashboard}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-accent/[0.1] border border-accent/20 text-sm font-medium text-accent-light hover:bg-accent/[0.15] transition-all"
                >
                  View Results <ArrowDown className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            /* Default: upload zone */
            <>
              {error && (
                <div className="max-w-lg mx-auto mb-4 p-4 rounded-xl bg-red-500/[0.06] border border-red-500/20 flex items-start gap-3 text-left">
                  <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                  <div>
                    <p className="text-red-300 text-sm font-medium">Upload failed</p>
                    <p className="text-red-400/80 text-sm mt-0.5">{error}</p>
                  </div>
                </div>
              )}

              <div
                onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
                onClick={handleClick}
                className={`
                  max-w-lg mx-auto p-10 rounded-2xl cursor-pointer transition-all duration-300
                  ${dragOver
                    ? 'border-accent/50 bg-accent/[0.06] scale-[1.02]'
                    : 'border-white/[0.08] bg-white/[0.02] hover:border-accent/30 hover:bg-accent/[0.03]'
                  }
                  border-2 border-dashed backdrop-blur-sm
                `}
              >
                <input
                  ref={inputRef}
                  type="file"
                  accept=".pdf"
                  className="hidden"
                  onChange={handleChange}
                />
                <div className="flex flex-col items-center gap-4">
                  <div className="w-14 h-14 rounded-xl bg-accent/[0.08] flex items-center justify-center border border-accent/10">
                    <Upload className="w-6 h-6 text-accent-light" strokeWidth={1.5} />
                  </div>
                  <div>
                    <p className="text-white font-medium text-lg">
                      Drag &amp; drop your research PDF here
                    </p>
                    <p className="text-gray-500 text-sm mt-1">
                      or browse files &middot; Max 50 MB &middot; Runs locally
                    </p>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        <div
          className="mt-12 flex flex-wrap items-center justify-center gap-8 text-sm text-gray-500 animate-fade-in-up"
          style={{ animationDelay: '0.65s', animationFillMode: 'both' }}
        >
          <span className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-accent-light" />
            Multi-provider AI
          </span>
          <span className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-accent-light" />
            PyMuPDF extraction
          </span>
          <span className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-accent-light" />
            Markdown export
          </span>
        </div>
      </div>
    </section>
  )
}
