export type Video = {
  id: number;
  platform: string;
  url: string;
  caption?: string;
  views: number;
  likes: number;
  comments: number;
  shares: number;
  trend_score: number;
  audio_name?: string;
};

export type AudioTrend = {
  audio_name: string;
  count: number;
};
