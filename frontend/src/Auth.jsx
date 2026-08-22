import { useState } from "react";
import api from "./api";

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
    try {
      if (mode === "register") {
        await api.post("/auth/register", { email, password });
        setMode("login");
        setError("Account created. Please log in.");
        return;
      }

      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);

      const res = await api.post("/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("email", email);
      onLogin(res.data.access_token);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-md max-w-sm">
      <h3 className="font-bold text-gray-800 mb-4">
        {mode === "login" ? "Log in" : "Create account"}
      </h3>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full mb-3 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-emerald-400"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full mb-3 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-emerald-400"
      />

      {error && <p className="text-xs text-rose-600 mb-3">{error}</p>}

      <button
        onClick={handleSubmit}
        className="w-full py-2 bg-gradient-to-r from-emerald-500 to-green-500 text-white rounded-lg text-sm font-semibold mb-3"
      >
        {mode === "login" ? "Log in" : "Sign up"}
      </button>

      <p className="text-xs text-gray-400 text-center">
        {mode === "login" ? "No account?" : "Already have an account?"}{" "}
        <button
          onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}
          className="text-emerald-600 font-semibold"
        >
          {mode === "login" ? "Sign up" : "Log in"}
        </button>
      </p>
    </div>
  );
}

export default Auth;