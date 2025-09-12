import { NextResponse } from "next/server";

export async function GET() {
  const r = await fetch(`${process.env.API_URL}/api/news`, {
    headers: { "content-type": "application/json" },
    cache: "no-store",
  });
  const data = await r.json();
  return NextResponse.json(data, { status: r.status });
}
