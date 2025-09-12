type Position = {
  symbol: string;
  qty: string;
  avg_entry_price?: string;
  market_value?: string;
  unrealized_pl?: string;
  side?: string;
};

export default function PositionsTable({ positions }: { positions: Position[] }) {
  return (
    <div className="theme-container">
      <div className="px-4 py-3 border-b">
        <h2 className="text-lg font-medium">Positions</h2>
      </div>
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            {["Symbol","Side","Qty","Avg Entry","Mkt Value","Unrealized P/L"].map(h => (
              <th key={h} className="px-4 py-2 text-left text-gray-600">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {positions?.length ? positions.map((p) => (
            <tr key={p.symbol} className="odd:bg-white even:bg-gray-50">
              <td className="px-4 py-2 font-medium">{p.symbol}</td>
              <td className="px-4 py-2 uppercase">{p.side ?? "—"}</td>
              <td className="px-4 py-2">{p.qty}</td>
              <td className="px-4 py-2">{p.avg_entry_price ? `$${p.avg_entry_price}` : "—"}</td>
              <td className="px-4 py-2">{p.market_value ? `$${p.market_value}` : "—"}</td>
              <td className="px-4 py-2">{p.unrealized_pl ? `$${p.unrealized_pl}` : "—"}</td>
            </tr>
          )) : (
            <tr><td className="px-4 py-6 text-gray-500" colSpan={6}>No positions</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
