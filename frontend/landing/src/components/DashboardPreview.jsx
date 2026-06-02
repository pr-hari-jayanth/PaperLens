import { useState } from 'react'
import {
  FileText,
  Lightbulb,
  Target,
  FlaskConical,
  Download,
  Copy,
  Check,
  BookOpen,
  Sparkles,
  Quote,
} from 'lucide-react'

const tabs = [
  { id: 'summary', label: 'Executive Summary', icon: FileText },
  { id: 'findings', label: 'Key Findings', icon: Lightbulb },
  { id: 'methodology', label: 'Methodology & Conclusion', icon: FlaskConical },
  { id: 'simple', label: 'Simple Explanation', icon: Quote },
]

function contentForTab(tab, data) {
  const s = data.summary || {}
  switch (tab) {
    case 'summary':
      return s.executive_summary || ''
    case 'findings':
      return s.key_findings || []
    case 'methodology':
      return {
        methodology: s.methodology || '',
        conclusion: s.conclusion || '',
      }
    case 'simple':
      return data.simple_explanation || ''
    default:
      return ''
  }
}

export default function DashboardPreview({ data }) {
  const [activeTab, setActiveTab] = useState('summary')
  const [copied, setCopied] = useState(false)
  const [downloading, setDownloading] = useState(false)

  const handleCopy = () => {
    const content = contentForTab(activeTab, data)
    const text = typeof content === 'string' ? content : JSON.stringify(content, null, 2)
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = async () => {
    if (!data.report_path) return
    setDownloading(true)
    try {
      const resp = await fetch(`/api/reports/${encodeURIComponent(data.report_path)}`)
      if (!resp.ok) throw new Error('Download failed')
      const blob = await resp.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = data.report_path.split('/').pop() || 'report.md'
      a.click()
      URL.revokeObjectURL(url)
    } catch {
      // silent
    } finally {
      setDownloading(false)
    }
  }

  const s = data.summary || {}
  const findingsCount = (s.key_findings || []).length
  const keywordCount = (s.keywords || []).length

  return (
    <section id="analysis-results" className="relative py-16 md:py-20 px-4 scroll-mt-20">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full text-xs font-medium tracking-widest uppercase text-accent-light bg-accent/[0.06] border border-accent/10 mb-4">
            Results
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
            {data.title || 'Analysis Complete'}
          </h2>
          {data.abstract && (
            <p className="mt-3 text-gray-500 text-sm max-w-2xl mx-auto line-clamp-2">
              {data.abstract}
            </p>
          )}
        </div>

        {/* Metric cards */}
        <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto mb-10">
          <div className="text-center p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
            <div className="text-2xl font-bold text-white">{findingsCount}</div>
            <div className="text-xs text-gray-500 mt-0.5">Findings</div>
          </div>
          <div className="text-center p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
            <div className="text-2xl font-bold text-white">{keywordCount}</div>
            <div className="text-xs text-gray-500 mt-0.5">Keywords</div>
          </div>
          <div className="text-center p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
            <div className="text-2xl font-bold text-white">{data.abstract ? 'Yes' : 'No'}</div>
            <div className="text-xs text-gray-500 mt-0.5">Abstract</div>
          </div>
        </div>

        {/* Main dashboard */}
        <div className="relative rounded-2xl border border-white/[0.08] bg-dark-800/30 backdrop-blur-sm overflow-hidden glow-purple">
          <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06]">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-accent/[0.1] flex items-center justify-center border border-accent/10">
                <BookOpen className="w-4 h-4 text-accent-light" strokeWidth={1.5} />
              </div>
              <div>
                <h3 className="text-white font-semibold text-sm">{data.title || 'Untitled'}</h3>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleCopy}
                className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-all"
                title="Copy content"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-green-400" />
                ) : (
                  <Copy className="w-4 h-4" strokeWidth={1.5} />
                )}
              </button>
              {data.report_path && (
                <button
                  onClick={handleDownload}
                  disabled={downloading}
                  className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-all"
                  title="Download report"
                >
                  <Download className="w-4 h-4" strokeWidth={1.5} />
                </button>
              )}
            </div>
          </div>

          <div className="flex flex-col md:flex-row">
            <div className="md:w-56 shrink-0 border-b md:border-b-0 md:border-r border-white/[0.06] p-2">
              {tabs.map((tab) => {
                const Icon = tab.icon
                const active = activeTab === tab.id
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`
                      w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all text-left
                      ${active
                        ? 'bg-accent/[0.08] text-accent-light border border-accent/10'
                        : 'text-gray-400 hover:text-white hover:bg-white/[0.04] border border-transparent'
                      }
                    `}
                  >
                    <Icon className="w-4 h-4 shrink-0" strokeWidth={1.5} />
                    <span className="truncate">{tab.label}</span>
                  </button>
                )
              })}
            </div>

            <div className="flex-1 p-6 md:p-8 overflow-hidden">
              <ContentDisplay tab={activeTab} data={data} />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

function ContentDisplay({ tab, data }) {
  const s = data.summary || {}

  switch (tab) {
    case 'summary':
      return (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white font-semibold">
            <Sparkles className="w-4 h-4 text-accent-light" />
            <span>Executive Summary</span>
          </div>
          <p className="text-gray-300 leading-relaxed text-sm md:text-base">
            {s.executive_summary || 'No summary available.'}
          </p>
        </div>
      )

    case 'findings': {
      const findings = s.key_findings || []
      return (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white font-semibold">
            <Lightbulb className="w-4 h-4 text-yellow-400" />
            <span>Key Findings</span>
          </div>
          {findings.length === 0 ? (
            <p className="text-gray-500 text-sm">No key findings available.</p>
          ) : (
            <ul className="space-y-3">
              {findings.map((finding, i) => (
                <li key={i} className="flex gap-3 text-sm md:text-base text-gray-300">
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-accent-light shrink-0" />
                  <span>{finding}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )
    }

    case 'methodology':
      return (
        <div className="space-y-6">
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-white font-semibold">
              <FlaskConical className="w-4 h-4 text-accent-light" />
              <span>Methodology</span>
            </div>
            <p className="text-gray-300 leading-relaxed text-sm md:text-base">
              {s.methodology || 'No methodology available.'}
            </p>
          </div>
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-white font-semibold">
              <Target className="w-4 h-4 text-green-400" />
              <span>Conclusion</span>
            </div>
            <p className="text-gray-300 leading-relaxed text-sm md:text-base">
              {s.conclusion || 'No conclusion available.'}
            </p>
          </div>
        </div>
      )

    case 'simple':
      return (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white font-semibold">
            <Quote className="w-4 h-4 text-accent-light" />
            <span>Simple Explanation</span>
          </div>
          {data.simple_explanation ? (
            <div className="relative p-5 rounded-xl bg-accent/[0.04] border border-accent/10">
              <div className="absolute top-3 left-3 text-accent/20 text-4xl leading-none font-serif">
                &ldquo;
              </div>
              <p className="relative z-10 text-gray-300 leading-relaxed text-sm md:text-base pt-3">
                {data.simple_explanation}
              </p>
              <div className="absolute bottom-2 right-4 text-accent/20 text-4xl leading-none font-serif">
                &rdquo;
              </div>
            </div>
          ) : (
            <p className="text-gray-500 text-sm">No simple explanation available.</p>
          )}
        </div>
      )

    default:
      return null
  }
}
