import { NextResponse } from "next/server";

export async function GET() {
    const r = await fetch(`${process.env.API_URL}/api/broker/positions`, {
        headers: {
            "content-type": "application/json",
            ...(process.env.API_INTERNAL_KEY ? {"x-internal-auth": process.env.API_INTERNAL_KEY } : {}),
        },
        cache: "no-store",
    });
    const data = await r.json();
    return NextResponse.json(data, { status: r.status });
}