import AccountCard from "@/components/AccountCard";
import PositionsTable from "@/components/PositionsTable";
import NewsList from "@/components/NewsList";
import OrdersTable from "@/components/OrdersTable";
import dynamic from "next/dynamic";
// const PortfolioHistoryChart = dynamic(() => import("@/components/PortfolioHistoryChart"), { ssr: false });
import PortfolioHistoryChart from "@/components/PortfolioHistoryChart";

async function getJSON<T>(url: string, sort_key?: string, descending?: boolean): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000";
  console.log(`Fetching ${url}`);
  const r = await fetch(`${baseUrl}${url}`, { cache: "no-store" });
  if (!r.ok) throw new Error(`Failed: ${r.status}`);
  console.log(`Response: ${r.status}`);
  if (sort_key) {
    const data = await r.json();
    return data.sort((a: any, b: any) => {
      if (descending) {
        return a[sort_key] < b[sort_key] ? 1 : -1;
      }
      return a[sort_key] > b[sort_key] ? 1 : -1;
    });
  }
  return r.json();
}

export default async function Page() {
  const [news, positions, account, orders] = await Promise.all([
    getJSON<any>(`/api/news`, "published_at", true),
    getJSON<any>(`/api/broker/positions`),
    getJSON<any>(`/api/broker/account`),
    getJSON<any>(`/api/broker/orders`),
  ]);

  console.log(news, positions, account, orders);

  return (
    <main className="mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Tommy's Investments</h1>

      <section className="grid md:grid-cols-4 gap-6">
        <div className="md:col-span-3 space-y-6">
          <AccountCard account={account} />
          <PortfolioHistoryChart />
          <PositionsTable positions={positions} />
          <OrdersTable orders={orders} />
        </div>
        <div className="md:col-span-1">
          <NewsList items={news} />
        </div>
      </section>
    </main>
  )
}