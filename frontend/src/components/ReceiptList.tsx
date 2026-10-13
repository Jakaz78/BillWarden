import { useState } from "react";
import { Receipt } from "../types";
import { receiptsAPI } from "../api/client";

interface Props {
  receipts: Receipt[];
  onDeleted: () => void;
}

export default function ReceiptList({ receipts, onDeleted }: Props) {
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleDelete = async (id: number, shopName: string | null) => {
    const name = shopName || "nieznany sklep";
    if (!confirm(`Usunąć paragon ze sklepu ${name}?`)) return;

    setDeletingId(id);
    try {
      await receiptsAPI.delete(id);
      onDeleted();
    } catch (err) {
      console.error("Błąd usuwania:", err);
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return "---";
    const d = new Date(dateStr);
    return d.toLocaleDateString("pl-PL", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const formatAmount = (amount: string | null) => {
    if (!amount) return "0.00";
    return parseFloat(amount).toFixed(2);
  };

  if (receipts.length === 0) {
    return (
      <div className="empty-state">
        <p>Jeszcze nic tu nie ma. Dodaj pierwszy paragon powyżej! 👆</p>
      </div>
    );
  }

  return (
    <>
      <h2>Historia Wydatków</h2>

      {receipts.map((receipt) => (
        <div key={receipt.id} className="receipt-card">
          {receipt.receipt_image_url ? (
            <img
              src={receipt.receipt_image_url}
              alt="Paragon"
              className="receipt-thumb"
              onClick={() => setPreviewUrl(receipt.receipt_image_url)}
            />
          ) : (
            <div className="receipt-placeholder">🧾</div>
          )}

          <div className="receipt-info">
            <h3>{receipt.shop_name || "Nieznany Sklep"}</h3>
            <p>Data: {formatDate(receipt.transaction_date)}</p>
            <p className="price">{formatAmount(receipt.transaction_total_amount)} PLN</p>
          </div>

          <div className="delete-section">
            <button
              className="delete-btn"
              disabled={deletingId === receipt.id}
              onClick={() => handleDelete(receipt.id, receipt.shop_name)}
              title="Usuń paragon"
            >
              {deletingId === receipt.id ? "..." : "✕"}
            </button>
          </div>
        </div>
      ))}

      {/* Modal podglądu zdjęcia */}
      {previewUrl && (
        <div className="preview-overlay" onClick={() => setPreviewUrl(null)}>
          <div className="preview-content" onClick={(e) => e.stopPropagation()}>
            <button className="preview-close" onClick={() => setPreviewUrl(null)}>
              ✕
            </button>
            <img src={previewUrl} alt="Podgląd paragonu" />
          </div>
        </div>
      )}
    </>
  );
}