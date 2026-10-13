import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h1>🧾 BillWarden</h1>
      </div>
      <div className="navbar-right">
        {user && (
          <>
            <span className="user-badge">👤 {user.username}</span>
            <button className="btn-logout" onClick={handleLogout}>
              Wyloguj
            </button>
          </>
        )}
        <button className="btn-theme" onClick={toggleTheme}>
          {theme === "dark" ? "☀️ Tryb Jasny" : "🌙 Tryb Ciemny"}
        </button>
      </div>
    </nav>
  );
}
