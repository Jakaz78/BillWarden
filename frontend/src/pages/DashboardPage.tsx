import { useState, useEffect, useCallback } from "react";
import { receiptsAPI, statsAPI } from "../api/client";
import { Receipt, Stats } from "../types";
import Navbar from "../components/Navbar";
import StatsCard from "../components/StatsCard";
import MonthlyChart from "../components/MonthlyChart";
import ReceiptUpload from "../components/ReceiptUpload";
import ReceiptList from "../components/ReceiptList";

export default function DashboardPage() {
  const [receipts, setReceipts] = useState<Receipt[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loadingReceipts, setLoadingReceipts] = useState(true);
  const [loadingStats, setLoadingStats] = useState(true);

  const fetchReceipts = useCallback(async () => {
    setLoadingReceipts(true);
    try {
      const res = await receiptsAPI.list();
      setReceipts(res.data.results);
    } catch (err) {
      console.error("Błąd pobierania paragonów:", err);
    } finally {
      setLoadingReceipts(false);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    setLoadingStats(true);
    try {
      const res = await statsAPI.get();
      setStats(res.data);
    } catch (err) {
      console.error("Błąd pobierania statystyk:", err);
    } finally {
      setLoadingStats(false);
    }
  }, []);

  const refreshAll = useCallback(() => {
    fetchReceipts();
    fetchStats();
  }, [fetchReceipts, fetchStats]);

  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  return (
    <>
      <Navbar />
      <StatsCard stats={stats} loading={loadingStats} />
      <MonthlyChart data={stats?.monthly_summary ?? []} />
      <ReceiptUpload onUploaded={refreshAll} />

      {loadingReceipts ? (
        <p className="loading-text">Ładowanie paragonów...</p>
      ) : (
        <ReceiptList receipts={receipts} onDeleted={refreshAll} />
      )}
    </>
  );
}
