import { useState, FormEvent } from "react";
import { useAuth } from "../context/AuthContext";
import { Link, Navigate } from "react-router-dom";

export default function RegisterPage() {
  const { user, register } = useAuth();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== password2) {
      setError("Hasła muszą być identyczne.");
      return;
    }

    if (password.length < 8) {
      setError("Hasło musi mieć co najmniej 8 znaków.");
      return;
    }

    setLoading(true);

    try {
      await register(username, email, password, password2);
    } catch (err: any) {
      const data = err.response?.data;
      if (data) {
        // Zbierz wszystkie błędy walidacji
        const messages = Object.values(data)
          .flat()
          .join(" ");
        setError(messages || "Błąd rejestracji.");
      } else {
        setError("Błąd połączenia z serwerem.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="card-box">
        <h2>🧾 Zarejestruj się</h2>

        {error && <p className="error-text">{error}</p>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Nazwa użytkownika</label>
            <input
              id="username"
              type="text"
              className="form-control"
              placeholder="jan_kowalski"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="form-control"
              placeholder="jan@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Hasło</label>
            <input
              id="password"
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <span className="helptext">Minimum 8 znaków</span>
          </div>

          <div className="form-group">
            <label htmlFor="password2">Powtórz hasło</label>
            <input
              id="password2"
              type="password"
              className="form-control"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Rejestracja..." : "Zarejestruj się"}
          </button>
        </form>

        <div className="auth-link">
          Masz już konto? <Link to="/login">Zaloguj się</Link>
        </div>
      </div>
    </div>
  );
}