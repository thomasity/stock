export default function AccountCard({ account }: { account: any }) {
  const items: [string, string | undefined][] = [
    ["Status", account?.status],
    ["Buying Power", account?.buying_power],
    ["Equity", account?.equity],
    ["Cash", account?.cash],
    ["Portfolio Value", account?.portfolio_value],
  ];
  return (
    <div className="theme-container !border-0">
      {/* <h2 className="text-lg font-medium mb-2">Account {account?.status === "Active" ? <span className="text-green-500">●</span> : <span className="text-red-500">●</span>}</h2> */}
      <div className="grid sm:grid-cols-4 gap-4">
        {items.map(([k,v]) => (
          k === "Status" ? null : (
          <div key={k} className="p-3">
            <div className="text-sm text-gray-500">{k}</div>
            <div className="text-lg font-medium">${v ?? "—"}</div>
          </div>
        )))}
      </div>
    </div>
  );
}
