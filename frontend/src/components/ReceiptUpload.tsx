import { useState, useRef, DragEvent, ChangeEvent } from "react";
import { receiptsAPI } from "../api/client";

interface Props {
  onUploaded: () => void;
}

export default function ReceiptUpload({ onUploaded }: Props) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    const validTypes = ["image/jpeg", "image/png", "image/bmp", "image/webp"];
    if (!validTypes.includes(file.type)) {
      setError("Nieobsługiwany format. Dozwolone: JPG, PNG, BMP, WEBP.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("Plik jest za duży! Maksymalny rozmiar to 10 MB.");
      return;
    }

    setError(null);
    setPreview(URL.createObjectURL(file));
    setUploading(true);

    try {
      await receiptsAPI.upload(file);
      onUploaded();
      setPreview(null);
    } catch (err: any) {
      const detail = err.response?.data?.receipt_image?.[0];
      setError(detail || "Błąd podczas wgrywania paragonu.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const onDragOver = (e: DragEvent) => {
    e.preventDefault();
    setDragging(true);
  };

  const onDragLeave = (e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
  };

  const onDrop = (e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div className="card-box">
      <h3>📤 Dodaj nowy paragon</h3>

      {error && <p className="error-text">{error}</p>}

      <div
        className={`drop-zone ${dragging ? "drop-zone--active" : ""}`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        {uploading ? (
          <>
            <div className="drop-zone-icon">⏳</div>
            <p>Analizuję paragon...</p>
          </>
        ) : preview ? (
          <img
            src={preview}
            alt="Podgląd"
            style={{ maxHeight: 160, borderRadius: 8 }}
          />
        ) : (
          <>
            <div className="drop-zone-icon">📸</div>
            <p>Przeciągnij zdjęcie paragonu tutaj</p>
            <p className="drop-zone-hint">lub kliknij, aby wybrać plik (JPG, PNG, max 10 MB)</p>
          </>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/bmp,image/webp"
        onChange={onChange}
        style={{ display: "none" }}
      />
    </div>
  );
}