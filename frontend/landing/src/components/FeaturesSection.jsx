import { FileText, Brain, FileDown, Cpu, Network, Layers } from 'lucide-react'

const features = [
  {
    icon: Cpu,
    title: 'PyMuPDF Extraction',
    description:
      'High-fidelity parsing of academic PDFs using PyMuPDF. Extracts text, structure, metadata, and equations with near-perfect accuracy — even from multi-column layouts.',
    accent: 'from-sky-500 to-blue-500',
    gradient: 'from-sky-500/10 to-blue-500/5',
    border: 'border-sky-500/10',
    iconBg: 'bg-sky-500/10',
    iconColor: 'text-sky-400',
  },
  {
    icon: Network,
    title: 'LLM Multi-Routing',
    description:
      'Route analysis to OpenAI, Google Gemini, or a local Ollama instance. Automatic fallback, provider-agnostic prompts, and full control over your data pipeline.',
    accent: 'from-accent to-accent-light',
    gradient: 'from-accent/10 to-accent-light/5',
    border: 'border-accent/10',
    iconBg: 'bg-accent/10',
    iconColor: 'text-accent-light',
  },
  {
    icon: Layers,
    title: 'Structured Markdown Export',
    description:
      'Every analysis produces a clean, hierarchical Markdown report — executive summary, key findings, methodology, conclusion, and a plain-English breakdown. Ready for sharing or archiving.',
    accent: 'from-purple-500 to-pink-500',
    gradient: 'from-purple-500/10 to-pink-500/5',
    border: 'border-purple-500/10',
    iconBg: 'bg-purple-500/10',
    iconColor: 'text-purple-400',
  },
]

export default function FeaturesSection() {
  return (
    <section id="features" className="relative py-16 md:py-20 px-4">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[500px] bg-accent/[0.03] blur-[150px] rounded-full pointer-events-none" />

      <div className="relative max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full text-xs font-medium tracking-widest uppercase text-accent-light bg-accent/[0.06] border border-accent/10 mb-4">
            Features
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
            Built for research depth
          </h2>
          <p className="mt-4 text-gray-400 text-lg max-w-xl mx-auto">
            Every component is engineered for accuracy, speed, and
            flexibility.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {features.map((feat) => {
            const Icon = feat.icon
            return (
              <div
                key={feat.title}
                className="group relative p-0.5 rounded-2xl transition-all duration-500 hover:scale-[1.02]"
              >
                <div
                  className={`absolute inset-0 rounded-2xl bg-gradient-to-b ${feat.accent} opacity-0 group-hover:opacity-20 blur-sm transition-opacity duration-500`}
                />
                <div
                  className={`relative h-full rounded-2xl border ${feat.border} bg-dark-800/50 backdrop-blur-sm p-8 overflow-hidden`}
                >
                  <div
                    className={`absolute top-0 right-0 w-40 h-40 bg-gradient-to-br ${feat.gradient} rounded-full blur-3xl pointer-events-none`}
                  />

                  <div
                    className={`relative z-10 w-12 h-12 rounded-xl ${feat.iconBg} border ${feat.border} flex items-center justify-center mb-5 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}
                  >
                    <Icon className={`w-5 h-5 ${feat.iconColor}`} strokeWidth={1.5} />
                  </div>

                  <h3 className="relative z-10 text-xl font-semibold text-white mb-3">
                    {feat.title}
                  </h3>
                  <p className="relative z-10 text-gray-400 text-sm leading-relaxed">
                    {feat.description}
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
