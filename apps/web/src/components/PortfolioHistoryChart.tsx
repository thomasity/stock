"use client";
import { useEffect, useMemo, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

type HistoryResponse = {
    timestamp: (number | string)[];
    equity: (number | string)[];
    profit_loss_pct?: (number | string)[];
    timeframe?: string;
    period?: string;
}

type Point = { t: string; equity?: number; plPct?: number };

const PERIODS = ["1D", "7D", "30D", "90D", "180D", "1Y", "ALL"] as const;
const TIMEFRAMES = ["1Min", "5Min", "15Min", "1D"] as const;

function defaultTimeframe(period: string): string {
    if (period === "1D") return "1Min";
    if (period === "7D") return "15Min";
    return "1D";
}

function toIso(ts: number | string): string {
    if (typeof ts === "number") return new Date(ts * 1000).toISOString();
    return ts;
}

export default function PortfolioHistoryChart() {
    const [period, setPeriod] = useState<string>("30D");
    const [timeframe, setTimeframe] = useState<string>(defaultTimeframe("30D"));
    const [mode, setMode] = useState<"equity" | "plPct">("equity");
    const [data, setData] = useState<Point[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const ctl = new AbortController();
        async function run() {
            setLoading(true); setError(null);
            try {
                const qs = new URLSearchParams({ period, timeframe });
                console.log(qs.toString());
                const r = await fetch(`/api/portfolio/history?${qs.toString()}`,
                    { cache: "no-store", signal: ctl.signal }
                );
                if (!r.ok) throw new Error(`Error fetching history: ${r.status} ${r.statusText}`);
                const json: HistoryResponse = await r.json();
                const t = json.timestamp ?? [];
                const eq = json.equity ?? [];
                const pl = json.profit_loss_pct ?? [];
                const points: Point[] = t.map((v, i) => ({
                    t: toIso(v),
                    equity: typeof eq[i] === "number" ? eq[i] as number : undefined,
                    plPct: typeof pl[i] === "number" ? pl[i] as number : undefined
                }));
                setData(points);
            } catch (error: any) {
                if (error?.name !== "AbortError") setError(error?.message || "Failed to load");
            } finally {
                setLoading(false);
            }
        }
        run();
        return () => ctl.abort();
    }, [period, timeframe]);

    useEffect(() => {
        setTimeframe(defaultTimeframe(period));
    }, [period]);

    const seriesKey = mode === "equity" ? "equity" : "plPct";
    const yLabel = mode === "equity" ? "Equity ($)" : "P/L (%)";
    const formatted = useMemo(() => data, [data]);

    return (
        <div className="theme-container">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-3">
                <h2 className="text-lg font-medium">Portfolio History</h2>
                <div className="flex flex-wrap items-center gap-2">
                <select className="border rounded-md px-2 py-1 bg-white" value={period} onChange={(e) => setPeriod(e.target.value)}>
                    {PERIODS.map((p) => (
                    <option key={p} value={p}>{p}</option>
                    ))}
                </select>
                <select className="border rounded-md px-2 py-1 bg-white" value={timeframe} onChange={(e) => setTimeframe(e.target.value)}>
                    {TIMEFRAMES.map((tf) => (
                    <option key={tf} value={tf}>{tf}</option>
                    ))}
                </select>
                <div className="inline-flex rounded-md border overflow-hidden">
                    <button onClick={() => setMode("equity")} className={`px-3 py-1 text-sm ${mode === "equity" ? "bg-gray-900 text-white" : "bg-white"}`}>Equity</button>
                    <button onClick={() => setMode("plPct")} className={`px-3 py-1 text-sm ${mode === "plPct" ? "bg-gray-900 text-white" : "bg-white"}`}>P/L %</button>
                </div>
                </div>
            </div>


            {loading ? (
            <div className="p-6 text-sm text-gray-500">Loading…</div>
            ) : error ? (
            <div className="p-6 text-sm text-red-600">Error: {error}</div>
            ) : (
            <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                <LineChart data={formatted} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="t" minTickGap={24} tickFormatter={(v) => new Date(v).toLocaleString()} />
                <YAxis
                    yAxisId="left"
                    domain={["auto", "auto"]}
                    tickFormatter={(v) => (mode === "equity" ? `${v}` : `${(v as number).toFixed(3)}%`)}
                    width={80}
                />
                <Tooltip formatter={(val: any) => [mode === "equity" ? val : `${(val as number)}%`, yLabel]} labelFormatter={(l) => new Date(l).toLocaleString()} />
                <Line yAxisId="left" type="monotone" dataKey={seriesKey} dot={false} />
                </LineChart>
                </ResponsiveContainer>
            </div>
            )}
        </div>
    );
}

