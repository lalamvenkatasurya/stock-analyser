import { useState } from "react";
import { LayoutDashboard, LineChart, Brain, Bell, Settings, HelpCircle, Search, TrendingUp, TrendingDown, Activity, DollarSign, BarChart3, Star, LogOut } from "lucide-react";
import api from "./api";
import Auth from "./Auth";
import Watchlist from "./Watchlist";

function App() {
  const [ticker, setTicker] = useState("");
  const [stock, setStock] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [fundamentals, setFundamentals] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [email, setEmail] = useState(localStorage.getItem("email") || "");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [watchlistMsg, setWatchlistMsg] = useState("");
  const [watchlistRefresh, setWatchlistRefresh] = useState(0);

  const authHeader = { headers: { Authorization: `Bearer ${token}` } };

  const handleSearchWithTicker = async (overrideTicker) => {
    const rawTicker = overrideTicker ?? ticker;
    if (!rawTicker.trim()) return;
    setLoading(true);
    setError("");
    setStock(null);
    setRecommendation(null);
    setFundamentals(null);
    setWatchlistMsg("");

    const t = rawTicker.trim().toUpperCase();

    try {
      const [stockRes, recRes, fundRes] = await Promise.all([
        api.get(`/stock/${t}`),
        api.get(`/stock/recommendation/${t}`),
        api.get(`/stock/fundamentals/${t}`),
      ]);
      setStock(stockRes.data);
      setRecommendation(recRes.data);
      setFundamentals(fundRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => handleSearchWithTicker();

  const addToWatchlist = async () => {
    if (!stock) return;
    try {
      await api.post(`/watchlist/${stock.ticker}`, {}, authHeader);
      setWatchlistMsg("Added to watchlist");
      setWatchlistRefresh((n) => n + 1);
    } catch (err) {
      setWatchlistMsg(err.response?.data?.detail || "Could not add to watchlist");
    }
  };

  const handleTickerChange = async (value) => {
    setTicker(value);
    if (value.trim().length < 1) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }
    try {
      const res = await api.get(`/stock/search/${value.trim()}`);
      setSuggestions(res.data);
      setShowSuggestions(true);
    } catch {
      setSuggestions([]);
    }
  };

  const selectSuggestion = (symbol) => {
    setTicker(symbol);
    setShowSuggestions(false);
    handleSearchWithTicker(symbol);
  };

  const recColors = (rec) => {
    if (!rec) return { text: "text-gray-500", bg: "from-gray-400 to-gray-500", border: "border-gray-300" };
    if (rec.includes("Buy")) return { text: "text-emerald-600", bg: "from-emerald-500 to-green-500", border: "border-emerald-300" };
    if (rec.includes("Sell")) return { text: "text-rose-600", bg: "from-rose-500 to-red-500", border: "border-rose-300" };
    return { text: "text-amber-600", bg: "from-amber-500 to-yellow-500", border: "border-amber-300" };
  };

  const rc = recommendation ? recColors(recommendation.recommendation) : recColors(null);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    setToken(null);
    setEmail("");
  };

  const initials = email ? email.slice(0, 2).toUpperCase() : "?";

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 flex">
      <aside className="w-64 bg-white border-r border-gray-200 p-4 flex flex-col shrink-0 shadow-sm">
        <div className="flex items-center gap-3 mb-8 px-2">
          <div className="bg-gradient-to-br from-emerald-400 to-cyan-500 p-2.5 rounded-xl shadow-md shadow-emerald-200">
            <TrendingUp className="text-white" size={22} strokeWidth={2.5} />
          </div>
          <div>
            <p className="font-bold text-lg leading-tight text-gray-800">AI Stock</p>
            <p className="text-xs text-gray-400 leading-tight">Analyser</p>
          </div>
        </div>

        <p className="text-xs text-gray-400 font-semibold px-2 mb-2 tracking-wider">ANALYSIS</p>
        <nav className="space-y-1 mb-6">
          <SidebarItem icon={<LayoutDashboard size={18} />} label="Market Dashboard" active={activeTab === "dashboard"} onClick={() => setActiveTab("dashboard")} />
          <SidebarItem icon={<LineChart size={18} />} label="Stock Analysis" active={activeTab === "analysis"} onClick={() => setActiveTab("analysis")} />
          <SidebarItem icon={<Brain size={18} />} label="AI Recommendations" active={activeTab === "ai"} onClick={() => setActiveTab("ai")} />
        </nav>

        <div className="mt-auto space-y-1">
          <SidebarItem icon={<Bell size={18} />} label="Alerts" />
          <SidebarItem icon={<Settings size={18} />} label="Settings" />
          <SidebarItem icon={<HelpCircle size={18} />} label="Help" />
        </div>
      </aside>

      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-3 flex justify-end items-center shadow-sm">
          {token ? (
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-700">{email}</p>
                <p className="text-xs text-gray-400">Signed in</p>
              </div>
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center text-white text-xs font-bold">
                {initials}
              </div>
              <button onClick={handleLogout} className="text-gray-400 hover:text-rose-500 ml-2" title="Log out">
                <LogOut size={18} />
              </button>
            </div>
          ) : (
            <p className="text-sm text-gray-400">Not signed in</p>
          )}
        </header>

        <main className="flex-1 p-6 overflow-y-auto relative">
          {!token ? (
            <div className="flex items-center justify-center min-h-[70vh]">
              <div className="w-full max-w-sm">
                <div className="text-center mb-6">
                  <div className="inline-flex bg-gradient-to-br from-emerald-400 to-cyan-500 p-3 rounded-2xl shadow-md shadow-emerald-200 mb-3">
                    <TrendingUp className="text-white" size={28} strokeWidth={2.5} />
                  </div>
                  <h2 className="text-xl font-bold text-gray-800">Sign in to continue</h2>
                  <p className="text-sm text-gray-400 mt-1">Access live market analysis and AI recommendations</p>
                </div>
                <Auth onLogin={(t) => { setToken(t); setEmail(localStorage.getItem("email") || ""); }} />
              </div>
            </div>
          ) : activeTab === "dashboard" ? (
            <>
              <div className="relative mb-6 max-w-xl">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                <input
                  type="text"
                  value={ticker}
                  onChange={(e) => handleTickerChange(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  onFocus={() => ticker && setShowSuggestions(true)}
                  onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
                  placeholder="Search by company name or ticker... (e.g. Tata, TCS.NS)"
                  className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl text-sm shadow-sm focus:outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 transition-all"
                />

                {showSuggestions && suggestions.length > 0 && (
                  <div className="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden">
                    {suggestions.map((s, i) => (
                      <div
                        key={i}
                        onMouseDown={() => selectSuggestion(s.symbol)}
                        className="px-4 py-2.5 hover:bg-emerald-50 cursor-pointer flex justify-between items-center"
                      >
                        <span className="text-sm font-medium text-gray-700">{s.name}</span>
                        <span className="text-xs text-gray-400">{s.symbol}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="mb-6 max-w-sm">
                <Watchlist token={token} key={watchlistRefresh} />
              </div>

              {loading && (
                <div className="flex items-center gap-2 text-cyan-600">
                  <Activity className="animate-pulse" size={18} />
                  <p>Analysing market data...</p>
                </div>
              )}
              {error && <p className="text-rose-600 bg-rose-50 border border-rose-200 rounded-lg px-4 py-2 max-w-xl">{error}</p>}

              {stock && recommendation && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                  <div className={`relative overflow-hidden bg-white border ${rc.border} rounded-2xl p-6 lg:col-span-2 shadow-md`}>
                    <div className={`absolute -top-20 -right-20 w-64 h-64 bg-gradient-to-br ${rc.bg} opacity-[0.07] rounded-full blur-3xl`}></div>

                    <div className="relative flex justify-between items-start mb-4">
                      <div>
                        <p className="text-gray-400 text-sm mb-1">{stock.ticker}</p>
                        <p className="text-4xl font-extrabold tracking-tight text-gray-900">₹{stock.current_price}</p>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        <div className={`px-4 py-2 rounded-xl bg-gradient-to-r ${rc.bg} shadow-md text-white font-bold text-sm flex items-center gap-2`}>
                          {recommendation.recommendation.includes("Buy") ? <TrendingUp size={16} /> : recommendation.recommendation.includes("Sell") ? <TrendingDown size={16} /> : <Activity size={16} />}
                          {recommendation.recommendation}
                        </div>
                        <button
                          onClick={addToWatchlist}
                          className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border border-amber-300 text-amber-600 bg-amber-50 hover:bg-amber-100 transition"
                        >
                          <Star size={13} /> Add to watchlist
                        </button>
                      </div>
                    </div>

                    {watchlistMsg && <p className="relative text-xs text-emerald-600 mb-3">{watchlistMsg}</p>}

                    <div className="relative grid grid-cols-3 gap-4">
                      <ColorStat icon={<Activity size={16} />} label="RSI" value={stock.rsi ?? "N/A"} color="from-purple-600 to-indigo-600" bg="bg-purple-50" />
                      <ColorStat icon={<BarChart3 size={16} />} label="MACD" value={stock.macd ?? "N/A"} color="from-cyan-600 to-blue-600" bg="bg-cyan-50" />
                      <ColorStat icon={<DollarSign size={16} />} label="Volume" value={stock.volume.toLocaleString()} color="from-orange-600 to-amber-600" bg="bg-orange-50" />
                    </div>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-md">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="bg-gradient-to-br from-emerald-400 to-cyan-500 p-1.5 rounded-lg">
                        <Brain size={16} className="text-white" />
                      </div>
                      <h3 className="font-bold text-gray-800">AI Analysis</h3>
                    </div>

                    <div className="flex items-center justify-between mb-4 mt-2">
                      <p className="text-xs text-gray-400">
                        Signal Score:{" "}
                        <span className={`font-bold ${rc.text}`}>{recommendation.score > 0 ? `+${recommendation.score}` : recommendation.score}</span>
                      </p>
                      <span className={`text-xs font-semibold px-2 py-1 rounded-md ${
                        recommendation.confidence_label === "High" ? "bg-emerald-50 text-emerald-600" :
                        recommendation.confidence_label === "Medium" ? "bg-amber-50 text-amber-600" :
                        "bg-gray-100 text-gray-500"
                      }`}>
                        {recommendation.confidence_label} confidence ({recommendation.confidence_pct}%)
                      </span>
                    </div>

                    <ul className="space-y-3">
                      {recommendation.reasons.map((r, i) => (
                        <li key={i} className="text-sm text-gray-600 flex gap-2.5 items-start">
                          <span className={`shrink-0 mt-1.5 w-1.5 h-1.5 rounded-full bg-gradient-to-r ${rc.bg}`}></span>
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <FundamentalsCard data={fundamentals} />
                </div>
              )}
            </>
          ) : activeTab === "analysis" ? (
            <div className="max-w-xl">
              <h2 className="text-xl font-bold text-gray-800 mb-2">Stock Analysis</h2>
              <p className="text-sm text-gray-400 mb-4">Search a ticker on the Market Dashboard tab to view detailed technical and fundamental analysis.</p>
              <button onClick={() => setActiveTab("dashboard")} className="text-sm font-semibold text-emerald-600">
                Go to Market Dashboard →
              </button>
            </div>
          ) : (
            <div className="max-w-xl">
              <h2 className="text-xl font-bold text-gray-800 mb-2">AI Recommendations</h2>
              <p className="text-sm text-gray-400 mb-4">Your AI-generated Buy/Hold/Sell calls appear here after you search a stock on the Market Dashboard.</p>
              <button onClick={() => setActiveTab("dashboard")} className="text-sm font-semibold text-emerald-600">
                Go to Market Dashboard →
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

function SidebarItem({ icon, label, active, onClick }) {
  return (
    <div
      onClick={onClick}
      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm cursor-pointer transition-all ${
        active
          ? "bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm font-medium"
          : "text-gray-500 hover:bg-gray-50 hover:text-gray-700"
      }`}
    >
      {icon}
      <span>{label}</span>
    </div>
  );
}

function ColorStat({ icon, label, value, color, bg }) {
  return (
    <div className={`${bg} rounded-xl p-3.5 border border-gray-100`}>
      <div className={`inline-flex items-center gap-1.5 bg-gradient-to-r ${color} bg-clip-text text-transparent mb-1.5`}>
        {icon}
        <span className="text-xs font-semibold">{label}</span>
      </div>
      <p className="text-lg font-bold text-gray-800">{value}</p>
    </div>
  );
}

function FundamentalsCard({ data }) {
  if (!data) return null;

  const metrics = [
    { label: "P/E Ratio", value: data.pe_ratio?.toFixed(1), color: "from-purple-600 to-indigo-600", bg: "bg-purple-50" },
    { label: "ROE", value: data.roe ? `${(data.roe * 100).toFixed(1)}%` : null, color: "from-emerald-600 to-green-600", bg: "bg-emerald-50" },
    { label: "Debt/Equity", value: data.debt_to_equity?.toFixed(1), color: "from-rose-600 to-red-600", bg: "bg-rose-50" },
    { label: "Revenue Growth", value: data.revenue_growth ? `${(data.revenue_growth * 100).toFixed(1)}%` : null, color: "from-cyan-600 to-blue-600", bg: "bg-cyan-50" },
    { label: "Current Ratio", value: data.current_ratio?.toFixed(2), color: "from-orange-600 to-amber-600", bg: "bg-orange-50" },
    { label: "Market Cap", value: data.market_cap ? `₹${(data.market_cap / 1e7).toFixed(0)} Cr` : null, color: "from-pink-600 to-fuchsia-600", bg: "bg-pink-50" },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-md lg:col-span-3">
      <h3 className="font-bold text-gray-800 mb-1">{data.company_name}</h3>
      <p className="text-xs text-gray-400 mb-4">{data.sector} · {data.industry}</p>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        {metrics.map((m, i) => (
          <div key={i} className={`${m.bg} rounded-xl p-3.5 border border-gray-100`}>
            <p className={`text-xs font-semibold mb-1.5 bg-gradient-to-r ${m.color} bg-clip-text text-transparent`}>
              {m.label}
            </p>
            <p className="text-base font-bold text-gray-800">{m.value ?? "N/A"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;