"use client";

import { useEffect, useMemo, useState } from "react";
import { getExplodingVideos, getTopAudios, getTrendingVideos } from "@/lib/api";
import { AudioTrend, Video } from "@/types/video";

const navItems = ["Overview", "Exploding Now", "Trending Videos", "Audio Trends", "Settings"];

function scoreStyle(score: number) {
  if (score >= 80) return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
  if (score >= 50) return "bg-amber-500/20 text-amber-300 border-amber-500/30";
  return "bg-rose-500/20 text-rose-300 border-rose-500/30";
}

function formatNumber(n: number) {
  return new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(n);
}

function videoCard(video: Video) {
  return (
    <a
      key={video.id}
      href={video.url}
      target="_blank"
      rel="noreferrer"
      className="group rounded-xl border border-slate-800 bg-slate-900/70 p-3 transition hover:border-cyan-400/50"
    >
      <div className="mb-3 flex h-36 items-center justify-center rounded-lg bg-gradient-to-br from-slate-800 to-slate-700 text-slate-400">
        Mock Thumbnail
      </div>
      <p className="line-clamp-2 text-sm text-slate-200">{video.caption || "Untitled trend"}</p>
      <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
        <span>{video.platform}</span>
        <span>{formatNumber(video.views)} views</span>
      </div>
      <div className={`mt-3 inline-flex rounded-full border px-2 py-1 text-xs font-semibold ${scoreStyle(video.trend_score)}`}>
        Trend Score: {video.trend_score}
      </div>
    </a>
  );
}

export default function HomePage() {
  const [trending, setTrending] = useState<Video[]>([]);
  const [exploding, setExploding] = useState<Video[]>([]);
  const [audios, setAudios] = useState<AudioTrend[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setError(null);
        const [t, e, a] = await Promise.all([getTrendingVideos(), getExplodingVideos(), getTopAudios()]);
        setTrending(t);
        setExploding(e);
        setAudios(a);
      } catch {
        setError("Unable to load dashboard data from backend.");
      }
    }

    load();
    const i = setInterval(load, 60000);
    return () => clearInterval(i);
  }, []);

  const topExploding = useMemo(() => exploding.slice(0, 4), [exploding]);
  const topTrending = useMemo(() => [...trending].sort((a, b) => b.trend_score - a.trend_score).slice(0, 12), [trending]);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6 lg:px-8">
        <aside className="sticky top-6 hidden h-[calc(100vh-3rem)] w-64 rounded-2xl border border-slate-800 bg-slate-900/60 p-5 lg:block">
          <h1 className="mb-8 text-lg font-bold tracking-wide text-cyan-300">TrendScope</h1>
          <nav className="space-y-2">
            {navItems.map((item, idx) => (
              <button
                key={item}
                className={`w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                  idx === 0 ? "bg-cyan-500/15 text-cyan-300" : "text-slate-300 hover:bg-slate-800"
                }`}
              >
                {item}
              </button>
            ))}
          </nav>
        </aside>

        <section className="flex-1 space-y-6">
          <header className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
            <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Dashboard</p>
            <h2 className="mt-2 text-2xl font-semibold">Viral Video Intelligence</h2>
            <p className="mt-2 text-sm text-slate-400">Live signals from your FastAPI trend backend.</p>
            {error && <p className="mt-3 text-sm text-rose-400">{error}</p>}
          </header>

          <div>
            <h3 className="mb-3 text-lg font-semibold">Exploding Now</h3>
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{topExploding.map(videoCard)}</div>
          </div>

          <div>
            <h3 className="mb-3 text-lg font-semibold">Trending Videos</h3>
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{topTrending.map(videoCard)}</div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
            <h3 className="mb-3 text-lg font-semibold">Audio Trends</h3>
            <div className="overflow-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-left text-slate-400">
                    <th className="px-2 py-2 font-medium">Audio</th>
                    <th className="px-2 py-2 font-medium">Usage Count</th>
                    <th className="px-2 py-2 font-medium">Momentum</th>
                  </tr>
                </thead>
                <tbody>
                  {audios.map((audio, idx) => (
                    <tr key={audio.audio_name} className="border-b border-slate-800/70">
                      <td className="px-2 py-2 text-slate-200">{audio.audio_name}</td>
                      <td className="px-2 py-2">{formatNumber(audio.count)}</td>
                      <td className="px-2 py-2">
                        <span
                          className={`inline-flex rounded-full border px-2 py-1 text-xs font-semibold ${scoreStyle(
                            Math.max(20, 100 - idx * 8),
                          )}`}
                        >
                          {idx < 3 ? "Hot" : idx < 7 ? "Rising" : "Emerging"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
