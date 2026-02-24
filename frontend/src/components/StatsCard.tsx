import { Stats } from "../types";

interface Props {
  stats: Stats | null;
  loading: boolean;
}

export default function StatsCard({ stats, loading }: Props) {
  if (loading) {
    return (
      <div className="total-summary">
        <h2>Łącznie wydano</h2>
        <div className="total-amount">...</div>
      </div>
    );
  }

  const total = stats
    ? parseFloat(stats.total_expenses).toFixed(2).replace(".", ",")
    : "0,00";

  const count = stats?.receipt_count ?? 0;

  return (
    <div className="total-summary">
      <h2>Łącznie wydano</h2>
      <div className="total-amount">{total} PLN</div>
      <p className="receipt-count">
        {count === 0
          ? "Brak paragonów"
          : count === 1
          ? "1 paragon"
          : `${count} paragonów`}
      </p>
    </div>
  );
}