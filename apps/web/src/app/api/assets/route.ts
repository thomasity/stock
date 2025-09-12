import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
    const url = new URL(req.url);
    const status = url.searchParams.get("status") ?? "active";
    const asset_class = url.searchParams.get("asset_class") ?? "us_equity";
    const tradable = url.searchParams.get("tradable") ?? "true";

    const r = await fetch(
        `${process.env.API_URL}/api/broker/assets?status=${status}&asset_class=${asset_class}&tradable=${tradable}`,
        {
            headers: {
                "content-type": "application/json",
                ...(process.env.API_INTERNAL_KEY ? {"x-internal-auth": process.env.API_INTERNAL_KEY } : {}),
            },
            cache: "no-store",
        }
    );
    const data = await r.json();
    return NextResponse.json(data, { status: r.status });
}