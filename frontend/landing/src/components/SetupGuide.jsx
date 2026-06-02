import { useState } from 'react'
import {
  Settings2,
  Key,
  FileCode,
  Rocket,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Terminal,
  Copy,
  Check,
} from 'lucide-react'

const providers = [
  {
    id: 'openai',
    name: 'OpenAI',
    tip: 'GPT-4o / GPT-4o-mini — best overall quality, requires an API key.',
    url: 'https://platform.openai.com/api-keys',
    envKey: 'OPENAI_API_KEY',
    envValue: 'sk-...',
    accent: 'from-emerald-500 to-teal-500',
    gradient: 'from-emerald-500/10 to-teal-500/5',
    border: 'border-emerald-500/10',
  },
  {
    id: 'gemini',
    name: 'Gemini',
    tip: 'Google Gemini 2.0 Flash — free tier available, great for experimentation.',
    url: 'https://aistudio.google.com/app/apikey',
    envKey: 'GEMINI_API_KEY',
    envValue: 'AIza...',
    accent: 'from-blue-500 to-indigo-500',
    gradient: 'from-blue-500/10 to-indigo-500/5',
    border: 'border-blue-500/10',
  },
  {
    id: 'ollama',
    name: 'Ollama (Local)',
    tip: 'Run models locally with Ollama — no API key needed, fully offline.',
    url: 'https://ollama.ai/download',
    envKey: 'OLLAMA_BASE_URL (default: http://localhost:11434)',
    envValue: 'No key required',
    accent: 'from-orange-500 to-amber-500',
    gradient: 'from-orange-500/10 to-amber-500/5',
    border: 'border-orange-500/10',
  },
]

const steps = [
  {
    icon: Key,
    title: 'Get an API key',
    description: 'Sign up for one of the supported AI providers and grab your API key.',
  },
  {
    icon: FileCode,
    title: 'Edit .env',
    description: 'Set AI_PROVIDER and paste your key into the .env file in the project root.',
  },
  {
    icon: Terminal,
    title: 'Run the app',
    description: 'Run uv run python run.py and open http://127.0.0.1:8000.',
  },
  {
    icon: Rocket,
    title: 'Upload a PDF',
    description: 'Drop any research paper PDF onto the upload zone above to get started.',
  },
]

function DotEnvPreview() {
  const [copied, setCopied] = useState(false)
  const content = `# Pick your provider: openai | gemini | ollama
AI_PROVIDER=openai

# Paste your key (not needed for Ollama)
OPENAI_API_KEY=sk-your-key-here

# Or for Gemini:
# GEMINI_API_KEY=AIza...

# Or for local Ollama (default):
# OLLAMA_BASE_URL=http://localhost:11434`

  const handleCopy = () => {
    navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative rounded-xl bg-dark-800/60 border border-white/[0.06] overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-white/[0.06] bg-white/[0.02]">
        <span className="text-xs font-mono text-gray-400">.env</span>
        <button
          onClick={handleCopy}
          className="p-1 rounded-md text-gray-500 hover:text-white hover:bg-white/[0.06] transition-all"
          title="Copy .env template"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
        </button>
      </div>
      <pre className="p-4 text-xs leading-relaxed font-mono text-gray-300 overflow-x-auto">
        {content.split('\n').map((line, i) => (
          <div key={i}>
            {line.startsWith('#') ? (
              <span className="text-gray-500">{line}</span>
            ) : line.includes('=') ? (
              <>
                <span className="text-accent-light">{line.split('=')[0]}</span>
                <span>=</span>
                <span className="text-gray-300">{line.split('=').slice(1).join('=')}</span>
              </>
            ) : (
              <span>{line}</span>
            )}
            {'\n'}
          </div>
        ))}
      </pre>
    </div>
  )
}

export default function SetupGuide() {
  const [expanded, setExpanded] = useState(null)

  const toggle = (id) => setExpanded(expanded === id ? null : id)

  return (
    <section id="setup-guide" className="relative py-16 md:py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full text-xs font-medium tracking-widest uppercase text-accent-light bg-accent/[0.06] border border-accent/10 mb-4">
            Setup Guide
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
            Get started in minutes
          </h2>
          <p className="mt-4 text-gray-400 text-lg max-w-xl mx-auto">
            Choose your AI provider, drop in a key, and start analysing.
          </p>
        </div>

        {/* Quick start steps */}
        <div className="grid md:grid-cols-4 gap-4 mb-12">
          {steps.map((step, i) => {
            const Icon = step.icon
            return (
              <div
                key={step.title}
                className="relative p-5 rounded-xl border border-white/[0.06] bg-white/[0.02] group hover:border-accent/20 hover:bg-accent/[0.03] transition-all"
              >
                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold text-gray-500 bg-white/[0.04] border border-white/[0.06] mb-3">
                  {i + 1}
                </span>
                <Icon className="w-4 h-4 text-accent-light mb-2" strokeWidth={1.5} />
                <h3 className="text-sm font-semibold text-white mb-1">{step.title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{step.description}</p>
              </div>
            )
          })}
        </div>

        <div className="grid md:grid-cols-5 gap-8 items-start">
          {/* Providers */}
          <div className="md:col-span-3 space-y-3">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Key className="w-4 h-4 text-accent-light" />
              Supported AI Providers
            </h3>
            {providers.map((p) => {
              const open = expanded === p.id
              const Icon = open ? ChevronUp : ChevronDown
              return (
                <div
                  key={p.id}
                  className={`rounded-xl border ${p.border} bg-dark-800/40 overflow-hidden transition-all`}
                >
                  <button
                    onClick={() => toggle(p.id)}
                    className="w-full flex items-center justify-between px-5 py-4 text-left"
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full bg-gradient-to-br ${p.accent}`} />
                      <span className="text-white font-medium text-sm">{p.name}</span>
                      <span className="text-xs text-gray-500 hidden sm:inline">{p.tip}</span>
                    </div>
                    <Icon className="w-4 h-4 text-gray-500 shrink-0" />
                  </button>
                  {open && (
                    <div className="px-5 pb-5 space-y-3 animate-fade-in-down">
                      <p className="text-sm text-gray-400 sm:hidden">{p.tip}</p>
                      <a
                        href={p.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 text-xs text-accent-light hover:underline"
                      >
                        <ExternalLink className="w-3 h-3" />
                        {p.url}
                      </a>
                      <div className="pt-1">
                        <p className="text-xs text-gray-500 mb-1">In your .env:</p>
                        <code className="block px-3 py-2 rounded-lg bg-dark text-xs font-mono text-gray-300 border border-white/[0.06]">
                          {p.envKey}={p.envValue}
                        </code>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          {/* .env preview */}
          <div className="md:col-span-2">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Settings2 className="w-4 h-4 text-accent-light" />
              Configuration file
            </h3>
            <DotEnvPreview />
            <p className="mt-3 text-xs text-gray-500 leading-relaxed">
              The <code className="text-accent-light">.env</code> file is created automatically
              by <code className="text-accent-light">setup.sh</code> from{' '}
              <code className="text-accent-light">.env.example</code>.
              Just paste your key and you are ready to go.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
