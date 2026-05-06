export type RiskLevel = "low" | "medium" | "high";

export type DemoVideo = {
  id: string;
  title: string;
  channel: string;
  publishedAt: string;
  views: number;
  impressions: number;
  ctr: number;
  retention: number;
  avgViewDuration: number;
  subscribersGained: number;
  subscribersLost: number;
  riskScore: number;
  riskLevel: RiskLevel;
  topFactors: string[];
  action: string;
};

export const demoVideos: DemoVideo[] = [
  {
    id: "video_104",
    title: "Build a Personal Research Agent in 20 Minutes",
    channel: "Signal Studio",
    publishedAt: "May 1",
    views: 24100,
    impressions: 602000,
    ctr: 4.0,
    retention: 30.2,
    avgViewDuration: 247,
    subscribersGained: 161,
    subscribersLost: 92,
    riskScore: 0.82,
    riskLevel: "high",
    topFactors: ["CTR drop", "early retention loss", "subscriber churn"],
    action: "Rework title-thumbnail promise and tighten the opening 30 seconds.",
  },
  {
    id: "video_102",
    title: "I Replaced My Notes App With an AI System",
    channel: "Signal Studio",
    publishedAt: "Apr 17",
    views: 21100,
    impressions: 452000,
    ctr: 4.7,
    retention: 33.2,
    avgViewDuration: 226,
    subscribersGained: 138,
    subscribersLost: 65,
    riskScore: 0.73,
    riskLevel: "high",
    topFactors: ["low CTR", "weak retention", "topic mismatch"],
    action: "Clarify the outcome in the title and compare against top AI workflow videos.",
  },
  {
    id: "video_203",
    title: "I Tested Viral Pasta Hacks",
    channel: "Kitchen Circuit",
    publishedAt: "Apr 23",
    views: 35400,
    impressions: 691000,
    ctr: 5.1,
    retention: 28.8,
    avgViewDuration: 202,
    subscribersGained: 205,
    subscribersLost: 91,
    riskScore: 0.69,
    riskLevel: "medium",
    topFactors: ["retention drop", "broad topic", "subscriber loss"],
    action: "Move the strongest result earlier and cut repeated setup beats.",
  },
  {
    id: "video_105",
    title: "The Truth About AI Browser Agents",
    channel: "Signal Studio",
    publishedAt: "May 4",
    views: 17800,
    impressions: 248000,
    ctr: 7.2,
    retention: 51.6,
    avgViewDuration: 329,
    subscribersGained: 241,
    subscribersLost: 13,
    riskScore: 0.24,
    riskLevel: "low",
    topFactors: ["new upload window"],
    action: "Keep monitoring; the title and retention profile are healthy.",
  },
  {
    id: "video_204",
    title: "Cheap High Protein Lunches",
    channel: "Kitchen Circuit",
    publishedAt: "Apr 30",
    views: 50800,
    impressions: 604000,
    ctr: 8.4,
    retention: 46.3,
    avgViewDuration: 303,
    subscribersGained: 519,
    subscribersLost: 31,
    riskScore: 0.18,
    riskLevel: "low",
    topFactors: ["stable CTR", "strong saves"],
    action: "Use this title structure for the next meal prep upload.",
  },
];

export const weeklyTrend = [
  { label: "Apr 13", ctr: 7.9, retention: 44.6, views: 31880 },
  { label: "Apr 20", ctr: 6.3, retention: 38.9, views: 52980 },
  { label: "Apr 27", ctr: 7.2, retention: 43.1, views: 96830 },
  { label: "May 4", ctr: 6.4, retention: 39.8, views: 120930 },
  { label: "May 6", ctr: 6.5, retention: 41.8, views: 138730 },
];

