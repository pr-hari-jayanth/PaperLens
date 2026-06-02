import { useState } from 'react'
import { Menu, X, ScanSearch, Plus, Github } from 'lucide-react'

const navLinks = [
  { label: 'Setup', href: '#setup-guide' },
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'Features', href: '#features' },
]

export default function Navbar({ analysisResult, onReset }) {
  const [open, setOpen] = useState(false)

  const scrollTo = (href) => {
    setOpen(false)
    const el = document.querySelector(href)
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }

  const handleNewAnalysis = () => {
    onReset()
    window.scrollTo({ top: 0, behavior: 'smooth' })
    setOpen(false)
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50">
      <div className="absolute inset-0 bg-dark/70 backdrop-blur-[12px] border-b border-white/[0.06]" />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-18">
          <a href="#" className="flex items-center gap-2.5 group shrink-0">
            <div className="relative w-8 h-8 flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-to-br from-accent to-accent-light rounded-lg opacity-20 group-hover:opacity-30 transition-opacity" />
              <ScanSearch className="w-5 h-5 text-accent-light relative z-10" strokeWidth={1.8} />
            </div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-lg font-semibold text-white tracking-tight">
                Paper<span className="text-accent-light">Lens</span>
              </span>
              <span className="hidden sm:inline text-[10px] font-medium text-gray-600 border border-white/[0.06] px-1.5 py-0.5 rounded">
                v1.0
              </span>
            </div>
          </a>

          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <button
                key={link.label}
                onClick={() => scrollTo(link.href)}
                className="px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/[0.04]"
              >
                {link.label}
              </button>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-2">
            <a
              href="https://github.com/your-org/paperlens"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-gray-400 hover:text-white hover:bg-white/[0.06] rounded-lg transition-all"
              title="View on GitHub"
            >
              <Github className="w-4 h-4" strokeWidth={1.5} />
            </a>
            {analysisResult ? (
              <button
                onClick={handleNewAnalysis}
                className="relative px-4 py-2 text-sm font-medium text-white rounded-xl overflow-hidden group"
              >
                <span className="absolute inset-0 bg-gradient-to-r from-accent to-accent-light rounded-xl" />
                <span className="absolute inset-[1px] bg-gradient-to-r from-accent to-accent-light rounded-[11px] opacity-0 group-hover:opacity-100 transition-opacity blur-sm" />
                <span className="absolute inset-[1px] bg-dark rounded-[11px] group-hover:bg-transparent transition-colors" />
                <span className="relative z-10 flex items-center gap-1.5">
                  <Plus className="w-3.5 h-3.5" />
                  New Analysis
                </span>
              </button>
            ) : (
              <button
                onClick={() => scrollTo('#setup-guide')}
                className="px-4 py-2 text-sm font-medium text-white bg-accent/[0.1] border border-accent/20 rounded-xl hover:bg-accent/[0.15] transition-all"
              >
                Get API Key
              </button>
            )}
          </div>

          <button
            onClick={() => setOpen(!open)}
            className="md:hidden p-2 text-gray-400 hover:text-white transition-colors"
            aria-label="Toggle menu"
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {open && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-dark/95 backdrop-blur-xl border-b border-white/[0.06] animate-fade-in-down">
          <div className="px-4 py-4 space-y-1">
            {navLinks.map((link) => (
              <button
                key={link.label}
                onClick={() => scrollTo(link.href)}
                className="block w-full text-left px-4 py-3 text-sm text-gray-400 hover:text-white hover:bg-white/[0.04] rounded-lg transition-colors"
              >
                {link.label}
              </button>
            ))}
            <hr className="border-white/[0.06] my-3" />
            {analysisResult ? (
              <button
                onClick={handleNewAnalysis}
                className="block w-full px-4 py-3 text-sm font-medium text-white bg-gradient-to-r from-accent to-accent-light rounded-xl text-center"
              >
                + New Analysis
              </button>
            ) : (
              <button
                onClick={() => scrollTo('#setup-guide')}
                className="block w-full px-4 py-3 text-sm font-medium text-center text-accent-light border border-accent/20 rounded-xl hover:bg-accent/[0.06] transition-all"
              >
                🔑 Get API Key
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}
