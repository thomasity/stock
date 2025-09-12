import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const search = new URL(request.url).search;
  const r = await fetch(`${process.env.API_URL}/api/portfolio/history${search}`, {
    headers: { "content-type": "application/json" },
    cache: "no-store",
  });
  const data = await r.json();
  return NextResponse.json(data, { status: r.status });
}