import { FileText, Brain, FileDown } from 'lucide-react'

const steps = [
  {
    icon: FileText,
    title: 'Upload & Extract',
    description:
      'Drop any research PDF. PaperLens uses PyMuPDF to cleanly parse text, structure, and metadata from any academic paper.',
    accent: 'from-blue-500 to-indigo-500',
    gradient: 'from-blue-500/10 to-indigo-500/5',
    border: 'border-blue-500/10',
  },
  {
    icon: Brain,
    title: 'LLM-Powered Analysis',
    description:
      'Multi-provider routing supports OpenAI, Google Gemini, or local Ollama instances. Your data stays under your control.',
    accent: 'from-accent to-accent-light',
    gradient: 'from-accent/10 to-accent-light/5',
    border: 'border-accent/10',
  },
  {
    icon: FileDown,
    title: 'Structured Markdown',
    description:
      'Get clean, organized reports with executive summaries, key findings, methodology breakdowns, and plain-English explanations.',
    accent: 'from-purple-500 to-pink-500',
    gradient: 'from-purple-500/10 to-pink-500/5',
    border: 'border-purple-500/10',
  },
]

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="relative py-16 md:py-20 px-4">
      {/* Section label */}
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full text-xs font-medium tracking-widest uppercase text-accent-light bg-accent/[0.06] border border-accent/10 mb-4">
            How It Works
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
            Three simple steps
          </h2>
          <p className="mt-4 text-gray-400 text-lg max-w-xl mx-auto">
            From PDF to structured insights in seconds.
          </p>
        </div>

        {/* Cards grid */}
        <div className="grid md:grid-cols-3 gap-6">
          {steps.map((step, i) => {
            const Icon = step.icon
            return (
              <div
                key={step.title}
                className="group relative p-0.5 rounded-2xl transition-all duration-500 hover:scale-[1.02]"
              >
                {/* Hover glow border */}
                <div className={`absolute inset-0 rounded-2xl bg-gradient-to-b ${step.accent} opacity-0 group-hover:opacity-20 blur-sm transition-opacity duration-500`} />
                <div className={`relative h-full rounded-2xl border ${step.border} bg-dark-800/50 backdrop-blur-sm p-8 overflow-hidden`}>
                  {/* Inner gradient glow */}
                  <div className={`absolute top-0 right-0 w-40 h-40 bg-gradient-to-br ${step.gradient} rounded-full blur-3xl pointer-events-none`} />

                  {/* Step number */}
                  <span className="relative z-10 inline-flex items-center justify-center w-8 h-8 rounded-full text-xs font-bold text-white bg-white/[0.06] border border-white/[0.08] mb-5">
                    {i + 1}
                  </span>

                  {/* Icon */}
                  <div className="relative z-10 w-12 h-12 rounded-xl bg-white/[0.04] border border-white/[0.06] flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300">
                    <Icon className="w-5 h-5 text-accent-light" strokeWidth={1.5} />
                  </div>

                  {/* Content */}
                  <h3 className="relative z-10 text-xl font-semibold text-white mb-3">
                    {step.title}
                  </h3>
                  <p className="relative z-10 text-gray-400 text-sm leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
