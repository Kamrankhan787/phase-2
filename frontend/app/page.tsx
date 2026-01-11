import Link from 'next/link';
import { Navbar } from '@/components/Navbar';
import { CheckCircle2, Shield, Zap, ArrowRight } from 'lucide-react';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-[#0f172a] text-white selection:bg-cyan-500/30">
      <Navbar />

      {/* Background Gradients */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-[120px] animate-pulse delay-1000" />
      </div>

      <div className="relative z-10 flex-1 flex flex-col items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-4xl text-center space-y-8">

          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 backdrop-blur-md">
            <span className="flex h-2 w-2 rounded-full bg-green-400 animate-pulse"></span>
            <span className="text-xs font-medium tracking-wide text-gray-300 uppercase">Phase II Live</span>
          </div>

          {/* Hero Title */}
          <h1 className="text-5xl sm:text-7xl font-bold tracking-tight">
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-indigo-400">
              Evolution of Todo
            </span>
            <span className="block mt-2 text-3xl sm:text-5xl text-gray-400 font-light">
              Master Your Workflow
            </span>
          </h1>

          {/* Hero Description */}
          <p className="max-w-2xl mx-auto text-lg sm:text-xl text-gray-400 leading-relaxed">
            Experience the next generation of task management.
            Persistent, secure, and beautifully designed for the modern web.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
            <Link
              href="/auth/signup"
              className="group relative px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-2xl transition-all hover:scale-105 shadow-[0_0_40px_-10px_rgba(37,99,235,0.5)] flex items-center gap-2"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/auth/signin"
              className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold rounded-2xl transition-all hover:scale-105 backdrop-blur-sm"
            >
              Sign In
            </Link>
          </div>

          {/* Feature Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-20 text-left">
            {[
              { icon: Shield, title: "Secure Auth", desc: "JWT-based security standards." },
              { icon: Zap, title: "Lightning Fast", desc: "Built with Next.js & FastAPI." },
              { icon: CheckCircle2, title: "Persistent", desc: "Your data, safe & sound." },
            ].map((feature, i) => (
              <div key={i} className="p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-white/10 transition-colors backdrop-blur-sm">
                <feature.icon className="w-8 h-8 text-blue-400 mb-4" />
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-400">{feature.desc}</p>
              </div>
            ))}
          </div>

        </div>

        <footer className="mt-20 text-gray-600 text-sm">
          &copy; 2026 Evolution of Todo. Crafted with precision.
        </footer>
      </div>
    </main>
  );
}
