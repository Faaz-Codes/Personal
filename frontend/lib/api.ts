import { Video } from "@/types/video";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function getTrendingVideos(): Promise<Video[]> {
  const res = await fetch(`${API_BASE}/videos/trending`, { cache: "no-store" });
  return res.json();
}

export async function getExplodingVideos(): Promise<Video[]> {
  const res = await fetch(`${API_BASE}/videos/exploding`, { cache: "no-store" });
  return res.json();
}

export async function getTopAudios(): Promise<{audio_name: string; count: number}[]> {
  const res = await fetch(`${API_BASE}/videos/top-audios`, { cache: "no-store" });
  return res.json();
}
