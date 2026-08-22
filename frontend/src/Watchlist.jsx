import { useState, useEffect } from "react";
import { Star, X } from "lucide-react";
import api from "./api";

function Watchlist({ token }) {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  const authHeader = { headers: { Authorization: `Bearer ${token}` } };

  const load = async () => {
    try {
      const res = await api.get("/watchlist/", authHeader);
      setItems(res.data);
    } catch {
      setError("Could not load watchlist");
    }
  };

  useEffect(() => { load(); }, []);

  const remove = async (ticker) => {
    try {
      await api.delete(`/watchlist/${ticker}`, authHeader);
      load();
    } catch {
      setError("Could not remove ticker");
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Star size={16} className="text-amber-500" />
        <h3 className="font-bold text-gray-800">Watchlist</h3>
      </div>

      {error && <p className="text-xs text-rose-600 mb-2">{error}</p>}

      {items.length === 0 ? (
        <p className="text-sm text-gray-400">No tickers saved yet.</p>
      ) : (
        <ul className="space-y-2">
          {items.map((item, i) => (
            <li key={i} className="flex justify-between items-center bg-gray-50 rounded-lg px-3 py-2">
              <span className="text-sm font-semibold text-gray-700">{item.ticker}</span>
              <button onClick={() => remove(item.ticker)} className="text-gray-400 hover:text-rose-500">
                <X size={16} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Watchlist;