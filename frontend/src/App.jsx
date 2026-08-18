import { useState } from "react";
import { LayoutDashboard, LineChart, Brain, Bell, Settings, HelpCircle, Search, TrendingUp, TrendingDown, Activity, DollarSign, BarChart3 } from "lucide-react";
import api from "./api";

function App() {
  const [ticker, setTicker] = useState("");
  const [stock, setStock] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!ticker.trim()) return;
    setLoading(true);
    setError("");
    setStock(null);
    setRecommendation(null);

    const t = ticker.trim().toUpperCase();

    try {
      const [stockRes, recRes] = await Promise.all([
        api.get(`/stock/${t}`),
        api.get(`/stock/recommendation/${t}`),
      ]);
      setStock(stockRes.data);
      setRecommendation(recRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const recColors = (rec) => {
    if (!rec) return { text: "text-gray-400", bg: "from-gray-700 to-gray-600", border: "border-gray-600" };
    if (rec.includes("Buy")) return { text: "text-emerald-400", bg: "from-emerald-500 to-green-600", border: "border-emerald-500/40" };
    if (rec.includes("Sell")) return { text: "text-rose-400", bg: "from-rose-500 to-red-600", border: "border-rose-500/40" };
    return { text: "text-amber-400", bg: "from-amber-500 to-yellow-600", border: "border-amber-500/40" };
  };

  const rc = recommendation ? recColors(recommendation.recommendation) : recColors(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-950 via-navy-900 to-[#0d1421] text-gray-100 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-navy-900/80 backdrop-blur border-r border-navy-700 p-4 flex flex-col shrink-0">
        <div className="flex items-center gap-3 mb-8 px-2">
          <div className="bg-gradient-to-br from-emerald-400 to-cyan-500 p-2.5 rounded-xl shadow-lg shadow-emerald-500/20">
            <TrendingUp className="text-navy-950" size={22} strokeWidth={2.5} />
          </div>
          <div>
            <p className="font-bold text-lg leading-tight bg-gradient-to-r from-emerald-300 to-cyan-300 bg-clip-text text-transparent">AI Stock</p>
            <p className="text-xs text-gray-500 leading-tight">Analyser</p>
          </div>
        </div>

        <p className="text-xs text-gray-500 font-semibold px-2 mb-2 tracking-wider">ANALYSIS</p>
        <nav className="space-y-1 mb-6">
          <SidebarItem icon={<LayoutDashboard size={18} />} label="Market Dashboard" active />
          <SidebarItem icon={<LineChart size={18} />} label="Stock Analysis" />
          <SidebarItem icon={<Brain size={18} />} label="AI Recommendations" />
        </nav>

        <div className="mt-auto space-y-1">
          <SidebarItem icon={<Bell size={18} />} label="Alerts" />
          <SidebarItem icon={<Settings size={18} />} label="Settings" />
          <SidebarItem icon={<HelpCircle size={18} />} label="Help" />
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-6 overflow-y-auto">
        {/* Search bar */}
        <div className="relative mb-8 max-w-xl">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="Search stocks... (RELIANCE.NS, TCS.NS, INFY.NS)"
            className="w-full pl-10 pr-4 py-3 bg-navy-800/80 backdrop-blur border border-navy-700 rounded-xl text-sm focus:outline-none focus:border-emerald-500/50 focus:ring-2 focus:ring-emerald-500/20 transition-all"
          />
        </div>

        {loading && (
          <div className="flex items-center gap-2 text-cyan-400">
            <Activity className="animate-pulse" size={18} />
            <p>Analysing market data...</p>
          </div>
        )}
        {error && <p className="text-rose-400 bg-rose-500/10 border border-rose-500/30 rounded-lg px-4 py-2 max-w-xl">{error}</p>}

        {stock && recommendation && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Price + Recommendation hero card */}
            <div className={`relative overflow-hidden bg-gradient-to-br from-navy-800 to-navy-900 border ${rc.border} rounded-2xl p-6 lg:col-span-2 shadow-xl`}>
              <div className={`absolute -top-20 -right-20 w-64 h-64 bg-gradient-to-br ${rc.bg} opacity-10 rounded-full blur-3xl`}></div>

              <div className="relative flex justify-between items-start mb-6">
                <div>
                  <p className="text-gray-400 text-sm mb-1">{stock.ticker}</p>
                  <p className="text-4xl font-extrabold tracking-tight">₹{stock.current_price}</p>
                </div>
                <div className={`px-4 py-2 rounded-xl bg-gradient-to-r ${rc.bg} shadow-lg text-white font-bold text-sm flex items-center gap-2`}>
                  {recommendation.recommendation.includes("Buy") ? <TrendingUp size={16} /> : recommendation.recommendation.includes("Sell") ? <TrendingDown size={16} /> : <Activity size={16} />}
                  {recommendation.recommendation}
                </div>
              </div>

              <div className="relative grid grid-cols-3 gap-4">
                <ColorStat icon={<Activity size={16} />} label="RSI" value={stock.rsi ?? "N/A"} color="from-purple-500 to-indigo-600" />
                <ColorStat icon={<BarChart3 size={16} />} label="MACD" value={stock.macd ?? "N/A"} color="from-cyan-500 to-blue-600" />
                <ColorStat icon={<DollarSign size={16} />} label="Volume" value={stock.volume.toLocaleString()} color="from-orange-500 to-amber-600" />
              </div>
            </div>

            {/* Recommendation reasons */}
            <div className="bg-gradient-to-br from-navy-800 to-navy-900 border border-navy-700 rounded-2xl p-5 shadow-xl">
              <div className="flex items-center gap-2 mb-1">
                <div className="bg-gradient-to-br from-emerald-400 to-cyan-500 p-1.5 rounded-lg">
                  <Brain size={16} className="text-navy-950" />
                </div>
                <h3 className="font-bold">AI Analysis</h3>
              </div>
              <p className="text-xs text-gray-500 mb-4">
                Signal Score:{" "}
                <span className={`font-bold ${rc.text}`}>{recommendation.score > 0 ? `+${recommendation.score}` : recommendation.score}</span>
              </p>
              <ul className="space-y-3">
                {recommendation.reasons.map((r, i) => (
                  <li key={i} className="text-sm text-gray-300 flex gap-2.5 items-start">
                    <span className={`shrink-0 mt-1.5 w-1.5 h-1.5 rounded-full bg-gradient-to-r ${rc.bg}`}></span>
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function SidebarItem({ icon, label, active }) {
  return (
    <div
      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm cursor-pointer transition-all ${
        active
          ? "bg-gradient-to-r from-emerald-500/20 to-cyan-500/10 text-emerald-300 border border-emerald-500/20 shadow-sm"
          : "text-gray-400 hover:bg-navy-800 hover:text-gray-200"
      }`}
    >
      {icon}
      <span>{label}</span>
    </div>
  );
}

function ColorStat({ icon, label, value, color }) {
  return (
    <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-700">
      <div className={`inline-flex items-center gap-1.5 bg-gradient-to-r ${color} bg-clip-text text-transparent mb-1.5`}>
        {icon}
        <span className="text-xs font-semibold">{label}</span>
      </div>
      <p className="text-lg font-bold">{value}</p>
    </div>
  );
}

export default App;