import { useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
);

function App() {
  const [city, setCity] = useState("Delhi");
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchForecast = async () => {
    try {
      setLoading(true);
      const res = await axios.get(
        `http://127.0.0.1:8000/forecast7/${city}`
      );
      setForecast(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getAQIColor = (aqi) => {
    if (aqi <= 50) return "#22c55e";
    if (aqi <= 100) return "#84cc16";
    if (aqi <= 200) return "#facc15";
    if (aqi <= 300) return "#f97316";
    if (aqi <= 400) return "#ef4444";
    return "#7f1d1d";
  };

  const getCategory = (aqi) => {
    if (aqi <= 50) return "Good";
    if (aqi <= 100) return "Moderate";
    if (aqi <= 200) return "Unhealthy for Sensitive Groups";
    if (aqi <= 300) return "Poor";
    if (aqi <= 400) return "Very Poor";
    return "Severe";
  };

  const chartData =
    forecast && {
      labels: forecast.map((f) => `Day +${f.day}`),
      datasets: [
        {
          label: "Predicted AQI",
          data: forecast.map((f) => f.prediction),
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59,130,246,0.15)",
          tension: 0.3,
          fill: true,
        },
        {
          label: "Upper Bound",
          data: forecast.map((f) => f.upper),
          borderColor: "#ef4444",
          borderDash: [6, 6],
        },
        {
          label: "Lower Bound",
          data: forecast.map((f) => f.lower),
          borderColor: "#22c55e",
          borderDash: [6, 6],
        },
      ],
    };

  return (
    <div style={styles.page}>
      {/* HEADER */}
      <div style={styles.header}>
        <h1 style={styles.title}>Air Quality Intelligence</h1>
        <p style={styles.subtitle}>
          Spatio-Temporal Forecasting • Probabilistic Uncertainty • Health Risk Modeling
        </p>

        <div style={styles.controls}>
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            style={styles.select}
          >
            <option>Delhi</option>
            <option>Mumbai</option>
            <option>Chennai</option>
            <option>Hyderabad</option>
            <option>Bangalore</option>
          </select>

          <button onClick={fetchForecast} style={styles.button}>
            {loading ? "Analyzing..." : "Get 7-Day Forecast"}
          </button>
        </div>
      </div>

      {forecast && (
        <div style={styles.dashboard}>
          {/* LEFT CARD */}
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Tomorrow Prediction</h2>

            <div
              style={{
                ...styles.bigAQI,
                color: getAQIColor(forecast[0].prediction),
              }}
            >
              {Math.round(forecast[0].prediction)}
            </div>

            <div style={styles.category}>
              {getCategory(forecast[0].prediction)}
            </div>

            <div style={styles.range}>
              {Math.round(forecast[0].lower)} –{" "}
              {Math.round(forecast[0].upper)} (90% Confidence)
            </div>
          </div>

          {/* RIGHT CARD */}
          <div style={styles.cardLarge}>
            <h2 style={styles.cardTitle}>7-Day Forecast</h2>
            <Line data={chartData} />
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    width: "100vw",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    color: "white",
    paddingBottom: "60px",
  },

  header: {
    textAlign: "center",
    paddingTop: "50px",
  },

  title: {
    fontSize: "48px",
    fontWeight: "700",
  },

  subtitle: {
    marginTop: "10px",
    opacity: 0.8,
  },

  controls: {
    marginTop: "30px",
    display: "flex",
    justifyContent: "center",
    gap: "20px",
  },

  select: {
    width: "400px",
    padding: "14px",
    borderRadius: "8px",
    border: "none",
    fontSize: "16px",
  },

  button: {
    padding: "14px 30px",
    borderRadius: "8px",
    border: "none",
    background: "#3b82f6",
    color: "white",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
  },

  dashboard: {
    marginTop: "60px",
    display: "grid",
    gridTemplateColumns: "1fr 2fr",
    gap: "40px",
    padding: "0 80px",
  },

  card: {
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(12px)",
    borderRadius: "14px",
    padding: "40px",
    textAlign: "center",
  },

  cardLarge: {
    background: "rgba(255,255,255,0.08)",
    backdropFilter: "blur(12px)",
    borderRadius: "14px",
    padding: "40px",
  },

  cardTitle: {
    marginBottom: "30px",
  },

  bigAQI: {
    fontSize: "72px",
    fontWeight: "700",
  },

  category: {
    marginTop: "10px",
    fontSize: "20px",
    opacity: 0.9,
  },

  range: {
    marginTop: "10px",
    opacity: 0.7,
  },
};

export default App;