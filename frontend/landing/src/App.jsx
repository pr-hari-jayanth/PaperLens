import { useState, useCallback, useEffect } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import FeaturesSection from './components/FeaturesSection'
import HowItWorks from './components/HowItWorks'
import DashboardPreview from './components/DashboardPreview'
import SetupGuide from './components/SetupGuide'
import Footer from './components/Footer'

const API_BASE = ''

export default function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)

  const handleUpload = useCallback(async (file) => {
    setError(null)
    setUploading(true)
    setAnalysisResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const resp = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!resp.ok) {
        let detail = `Server error (${resp.status})`
        try {
          const body = await resp.json()
          detail = body.detail || detail
        } catch {}
        throw new Error(detail)
      }

      const data = await resp.json()
      setAnalysisResult(data)
    } catch (err) {
      setError(err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }, [])

  const handleReset = useCallback(() => {
    setAnalysisResult(null)
    setError(null)
  }, [])

  useEffect(() => {
    if (analysisResult) {
      const el = document.querySelector('#analysis-results')
      if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth' }), 200)
    }
  }, [analysisResult])

  return (
    <div className="relative min-h-screen bg-dark overflow-hidden">
      <div className="fixed top-[-300px] left-[-200px] w-[600px] h-[600px] rounded-full bg-accent/5 blur-[120px] pointer-events-none" />
      <div className="fixed bottom-[-200px] right-[-200px] w-[500px] h-[500px] rounded-full bg-accent-light/5 blur-[100px] pointer-events-none" />

      <Navbar analysisResult={analysisResult} onReset={handleReset} />

      <Hero
        onUpload={handleUpload}
        uploading={uploading}
        error={error}
        analysisResult={analysisResult}
      />

      <FeaturesSection />
      <HowItWorks />

      <SetupGuide />

      {analysisResult && (
        <DashboardPreview data={analysisResult} />
      )}

      <Footer />
    </div>
  )
}
