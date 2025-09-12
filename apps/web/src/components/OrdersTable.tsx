type Order = {
  symbol: string;
  qty: string;
  side: ("buy" | "sell");
  type: ("market" | "limit" | "stop" | "stop_limit" | "trailing_stop");
  time_in_force: ("day" | "gtc" | "opg" | "cls" | "ioc" | "fok");
  limit_price?: number;
  stop_price?: number;
  client_order_id?: string;
  extended_hours?: boolean;
};

function populateType(order: Order) {
    const { type, limit_price, stop_price } = order;
    if (type === "limit" && limit_price !== undefined) return String(type + " @ $" + limit_price);
    if (type === "stop" && stop_price !== undefined) return String(type + " @ $" + stop_price);
    return type;
}

export default function OrdersTable({ orders }: { orders: Order[] }) {
  return (
    <div className="theme-container">
      <div className="px-4 py-3 border-b">
        <h2 className="text-lg font-medium">Recent Orders</h2>
      </div>
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            {["Asset","Order Type","Side","Qty"].map(h => (
              <th key={h} className="px-4 py-2 text-left text-gray-600">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {orders?.length ? orders.map((o) => (
            <tr key={o.client_order_id} className="odd:bg-white even:bg-gray-50">
              <td className="px-4 py-2 font-medium">{o.symbol}</td>
              <td className="px-4 py-2 uppercase">{o.type ? populateType(o) : "—"}</td>
              <td className="px-4 py-2">{o.side}</td>
              <td className="px-4 py-2">{o.qty}</td>
            </tr>
          )) : (
            <tr><td className="px-4 py-6 text-gray-500" colSpan={6}>No positions</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
