"use client";

import { useEffect, useState } from "react";
import { getExplodingVideos, getTopAudios, getTrendingVideos } from "@/lib/api";
import { VideoTable } from "@/components/video-table";
import { Video } from "@/types/video";

export default function HomePage() {
  const [trending, setTrending] = useState<Video[]>([]);
  const [exploding, setExploding] = useState<Video[]>([]);
  const [audios, setAudios] = useState<{ audio_name: string; count: number }[]>([]);

  async function load() {
    const [t, e, a] = await Promise.all([getTrendingVideos(), getExplodingVideos(), getTopAudios()]);
    setTrending(t); setExploding(e); setAudios(a);
  }

  useEffect(() => { load(); const i = setInterval(load, 60000); return () => clearInterval(i); }, []);

  const gems = trending.filter(v => v.views < 15000).slice(0, 10);
  const fastest = [...trending].sort((a, b) => b.views - a.views).slice(0, 10);

  return <main className="space-y-6"><h1 className="text-3xl font-bold">Viral Cat Trend Radar</h1><div className="grid gap-4 lg:grid-cols-2"><VideoTable title="Exploding Now" videos={exploding} /><VideoTable title="Underexposed Gems" videos={gems} /><div className="bg-slate-900 rounded-xl p-4"><h2 className="font-bold mb-3">Trending Audios</h2><ul>{audios.map(a => <li key={a.audio_name} className="flex justify-between border-b border-slate-800 py-2"><span>{a.audio_name}</span><span>{a.count}</span></li>)}</ul></div><VideoTable title="Fastest Growing Videos" videos={fastest} /></div></main>;
}
