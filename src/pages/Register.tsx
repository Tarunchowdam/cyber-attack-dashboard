import { useState } from "react";
import { authApi } from "../api/authApi";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function submit(e: any) {
    e.preventDefault();
    setError("");
    setMsg("");
    setLoading(true);

    if (!email.trim() || !password.trim()) {
      setError("Please fill all fields");
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long");
      setLoading(false);
      return;
    }

    try {
      const response = await authApi.register({ email, password });

      if (response.success) {
        setMsg("Registration successful!");
        setTimeout(() => navigate("/login"), 1500);
      } else {
        setError(response.message || "Registration failed");
      }
    } catch (err) {
      setError("Registration failed. Please try again.");
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submit}>
        <div style={{ textAlign: "center", marginBottom: 8 }}>
          <div className="logo" style={{
                          margin: '0 auto',
                          fontSize: 72,
                          color: "#00f2ff",
                          textShadow: "0 0 30px #00f2ff, 0 0 60px #00f2ff, 0 0 100px #00f2ff"
                          }}>🛡️</div>
        </div>

        <h2>Create Account</h2>
        <p>Register to access the security dashboard</p>

        {msg && <p style={{ color: "#4caf50", fontSize: 13 }}>{msg}</p>}
        {error && <p style={{ color: "tomato", fontSize: 13 }}>{error}</p>}

        <label style={{ fontWeight: 700, fontSize: 13, color: "#9fbfd0" }}>Email</label>
        <div style={{ marginTop: 8 }}>
          <input
            placeholder="user@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
          />
        </div>

        <label
          style={{
            marginTop: 12,
            display: "block",
            fontWeight: 700,
            fontSize: 13,
            color: "#9fbfd0",
          }}
        >
          Password
        </label>
        <div style={{ marginTop: 8 }}>
          <input
            placeholder="*********"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
          />
        </div>

        <button className="login-btn" type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>

        <p
          style={{ marginTop: 12, fontSize: 12, cursor: "pointer", color: "#9fbfd0", textAlign:"center" }}
          onClick={() => navigate("/login")}
        >
          Already have an account? Sign In
        </p>
      </form>
    </div>
  );
}