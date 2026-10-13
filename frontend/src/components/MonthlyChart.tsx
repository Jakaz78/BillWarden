import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { MonthlyStat } from "../types";

interface Props {
  data: MonthlyStat[];
}

export default function MonthlyChart({ data }: Props) {
  if (data.length === 0) {
    return (
      <div className="card-box">
        <h3>📅 Wydatki według miesięcy</h3>
        <p className="empty-text">Brak danych do analizy</p>
      </div>
    );
  }

  const chartData = [...data]
    .reverse()
    .map((item) => {
      const date = new Date(item.month);
      const label = date.toLocaleDateString("pl-PL", {
        month: "short",
        year: "numeric",
      });
      const value = parseFloat(item.total);
      return {
        name: label,
        kwota: isNaN(value) ? 0 : value,
      };
    })
    .filter((item) => item.kwota > 0);

  if (chartData.length === 0) {
    return (
      <div className="card-box">
        <h3>📅 Wydatki według miesięcy</h3>
        <p className="empty-text">Brak danych do analizy</p>
      </div>
    );
  }

  return (
    <div className="card-box">
      <h3>📅 Wydatki według miesięcy</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
          <XAxis
            dataKey="name"
            tick={{ fill: "var(--text-secondary)", fontSize: 12 }}
          />
          <YAxis
            tick={{ fill: "var(--text-secondary)", fontSize: 12 }}
            tickFormatter={(v) => `${v} zł`}
          />
          <Tooltip
            formatter={(value: number) => [`${value.toFixed(2)} PLN`, "Kwota"]}
            contentStyle={{
              background: "var(--card-bg)",
              border: "1px solid var(--border-color)",
              borderRadius: "8px",
              color: "var(--text-main)",
            }}
            labelStyle={{ color: "var(--text-main)" }}
            itemStyle={{ color: "var(--accent-color)" }}
            cursor={{ fill: "var(--border-color)", opacity: 0.3 }}
          />
          <Bar dataKey="kwota" fill="var(--accent-color)" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}