import { ScanSearch, Github, Bug } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="relative border-t border-white/[0.06] px-4">
      <div className="max-w-7xl mx-auto py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="col-span-2 md:col-span-1">
            <a href="#" className="flex items-center gap-2.5 group mb-4">
              <div className="relative w-8 h-8 flex items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-br from-accent to-accent-light rounded-lg opacity-20" />
                <ScanSearch className="w-5 h-5 text-accent-light relative z-10" strokeWidth={1.8} />
              </div>
              <span className="text-lg font-semibold text-white tracking-tight">
                Paper<span className="text-accent-light">Lens</span>
              </span>
            </a>
            <p className="text-gray-500 text-sm max-w-xs leading-relaxed">
              Run PaperLens locally. Powered by PyMuPDF &amp; your local or
              cloud LLM providers.
            </p>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold mb-4">Repository</h4>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-gray-500 hover:text-white text-sm transition-colors inline-flex items-center gap-2">
                  <Github className="w-3.5 h-3.5" />
                  GitHub
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-500 hover:text-white text-sm transition-colors inline-flex items-center gap-2">
                  <Bug className="w-3.5 h-3.5" />
                  Issue Tracker
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold mb-4">Product</h4>
            <ul className="space-y-3">
              <li>
                <button
                  onClick={() => document.querySelector('#features')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-500 hover:text-white text-sm transition-colors"
                >
                  Features
                </button>
              </li>
              <li>
                <button
                  onClick={() => document.querySelector('#how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-500 hover:text-white text-sm transition-colors"
                >
                  How It Works
                </button>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold mb-4">Legal</h4>
            <ul className="space-y-3">
              <li>
                <span className="text-gray-500 text-sm">Privacy Policy</span>
              </li>
              <li>
                <span className="text-gray-500 text-sm">Terms of Service</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-white/[0.06] flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <p>&copy; 2026 PaperLens. All rights reserved.</p>
          <p>Built with attention.</p>
        </div>
      </div>
    </footer>
  )
}
