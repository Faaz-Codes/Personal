import { AudioTrend, Video } from "@/types/video";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch ${path}: ${res.status}`);
  }
  return res.json();
}

export function getTrendingVideos(): Promise<Video[]> {
  return fetchJson<Video[]>("/videos/trending");
}

export function getExplodingVideos(): Promise<Video[]> {
  return fetchJson<Video[]>("/videos/exploding");
}

export function getTopAudios(): Promise<AudioTrend[]> {
  return fetchJson<AudioTrend[]>("/audios/top");
}
