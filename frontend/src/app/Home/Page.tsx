"use client";
import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-zinc-100 font-sans scroll-smooth">
      <nav className="fixed top-0 w-full z-50 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-zinc-800/50">
        <div className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 bg-white text-black flex items-center justify-center font-bold text-xs rounded-sm">
              BV
            </div>
            <span className="text-lg font-semibold tracking-tight">Buddhi Vetta</span>
          </div>

          <div className="hidden md:flex items-center gap-4">
            <Link href="#about" className="text-sm font-medium text-zinc-400 hover:text-white transition-colors px-4 py-2">
              Platform
            </Link>
            <Link href="/Dashboard" className="text-sm font-medium text-zinc-400 hover:text-white transition-colors px-4 py-2">
              Dashboard
            </Link>
            <div className="h-4 w-px bg-zinc-800 mx-2"></div>
            <Link href="/login" className="text-sm font-medium text-zinc-300 hover:text-white px-4 py-2">
              Log in
            </Link>
            <Link href="/signup" className="text-sm font-medium bg-white text-black px-4 py-2 rounded-md hover:bg-zinc-200 transition-colors">
              Sign up
            </Link>
          </div>
        </div>
      </nav>

      <section id="about" className="min-h-screen flex items-center pt-20 border-b border-zinc-800/50">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center w-full">
          <div className="flex flex-col gap-6">
            <div className="inline-flex items-center rounded-full border border-zinc-800 bg-zinc-900/50 px-3 py-1 text-xs font-medium text-zinc-300 w-fit">
              <span className="flex h-1.5 w-1.5 rounded-full bg-blue-500 mr-2"></span>
              Predictive Maintenance Engine v2.0
            </div>

            <h1 className="text-5xl lg:text-6xl font-semibold leading-[1.15] tracking-tight">
              Intelligent fleet <br />
              <span className="text-zinc-500">maintenance prediction.</span>
            </h1>

            <p className="text-zinc-400 text-lg max-w-lg leading-relaxed mt-2 font-light">
              Streamline your vehicle operations. Our machine learning models predict failures before they happen, minimizing downtime and optimizing maintenance schedules.
            </p>

            <div className="flex items-center gap-4 mt-6">
              <Link href="/Dashboard" className="px-6 py-3 rounded-md bg-white text-black font-medium hover:bg-zinc-200 transition-colors text-sm">
                Start Predicting
              </Link>
            </div>
          </div>

          <div className="relative w-full aspect-[4/3] bg-zinc-900/20 rounded-2xl border border-zinc-800/50 flex flex-col items-center justify-center p-8 overflow-hidden">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[length:24px_24px]"></div>
            <svg className="relative z-10 text-zinc-700 mb-4" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="16" x="4" y="4" rx="2" /><rect width="6" height="6" x="9" y="9" rx="1" /><path d="M15 2v2" /><path d="M15 20v2" /><path d="M2 15h2" /><path d="M2 9h2" /><path d="M20 15h2" /><path d="M20 9h2" /><path d="M9 2v2" /><path d="M9 20v2" /></svg>
            <p className="relative z-10 text-zinc-600 text-xs font-medium tracking-widest">SYSTEM OVERVIEW</p>
          </div>
        </div>
      </section>

      <section id="explore" className="min-h-[80vh] flex flex-col items-center justify-center py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(59,130,246,0.05),transparent_50%)]"></div>
        <div className="relative z-10 text-center max-w-2xl px-6">
          <h2 className="text-3xl md:text-4xl font-semibold tracking-tight mb-6">Actionable Insights</h2>
          <p className="text-zinc-400 font-light mb-10 text-lg">
            Visualize your prediction history, track asset health across your entire fleet, and generate comprehensive maintenance reports.
          </p>
          <Link href="/Dashboard" className="px-8 py-3 rounded-md bg-white text-black font-medium hover:bg-zinc-200 transition-colors text-sm">
            View Dashboard
          </Link>
        </div>
      </section>

      <footer className="py-8 border-t border-zinc-800/50 text-center text-zinc-600 text-sm font-light mt-auto">
        <p>© 2026 Buddhi Vetta. All rights reserved.</p>
      </footer>
    </div>
  );
}
