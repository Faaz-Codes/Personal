"use client";

import { useMemo, useState } from "react";
import { Video } from "@/types/video";

export function VideoTable({ title, videos }: { title: string; videos: Video[] }) {
  const [sortKey, setSortKey] = useState<keyof Video>("trend_score");
  const sorted = useMemo(() => [...videos].sort((a, b) => Number(b[sortKey] ?? 0) - Number(a[sortKey] ?? 0)), [videos, sortKey]);
  return <div className="bg-slate-900 rounded-xl p-4"><h2 className="font-bold mb-3">{title}</h2><table className="w-full text-sm"><thead><tr><th className="text-left">Caption</th><th onClick={() => setSortKey("trend_score")} className="cursor-pointer">Score</th><th onClick={() => setSortKey("views")} className="cursor-pointer">Views</th><th>Platform</th></tr></thead><tbody>{sorted.slice(0,10).map(v => <tr key={v.id} className="border-t border-slate-800"><td><a href={v.url} target="_blank">{v.caption || "Untitled"}</a></td><td><span className="bg-emerald-600 rounded px-2">{v.trend_score}</span></td><td>{v.views}</td><td>{v.platform}</td></tr>)}</tbody></table></div>;
}
