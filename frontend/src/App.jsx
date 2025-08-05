import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

function App() {
  const [priceData, setPriceData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [bayesianCP, setBayesianCP] = useState([]);
  const [ruptureCP, setRuptureCP] = useState([]);
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [volatility, setVolatility] = useState(null);
  const [avgLogReturn, setAvgLogReturn] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/price-data')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load price data');
        return res.json();
      })
      .then(data => {
        console.log("✅ Price Data Loaded:", data.length);
        setPriceData(data);
        setFilteredData(data);
      })
      .catch(err => {
        console.error("❌ Error loading price data:", err);
        setError("Error loading price data.");
      });

    fetch('/api/change-points/bayesian')
      .then(res => res.json())
      .then(data => setBayesianCP(data.change_points))
      .catch(err => console.error("❌ Error loading Bayesian CPs:", err));

    fetch('/api/change-points/ruptures')
      .then(res => res.json())
      .then(data => setRuptureCP(data.change_points))
      .catch(err => console.error("❌ Error loading Rupture CPs:", err));
  }, []);

  // Filter data based on date range
  useEffect(() => {
    if (!dateRange.start || !dateRange.end) {
      setFilteredData(priceData);
      return;
    }
    const filtered = priceData.filter(p => p.Date >= dateRange.start && p.Date <= dateRange.end);
    setFilteredData(filtered);
  }, [dateRange, priceData]);

  // Compute volatility and avg log return
  useEffect(() => {
    if (filteredData.length > 1) {
      const returns = filteredData.map((d, i, arr) =>
        i === 0 ? 0 : Math.log(d.Price / arr[i - 1].Price)
      );
      const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
      const variance = returns.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / returns.length;
      setVolatility(Math.sqrt(variance).toFixed(4));
      setAvgLogReturn((mean * 100).toFixed(3));
    }
  }, [filteredData]);

  if (error) {
    return <div style={{ padding: 20, color: "red", fontSize: 20 }}>{error}</div>;
  }

  if (priceData.length === 0) {
    return (
      <div style={{ padding: 20, fontSize: 20, color: "black" }}>
        🕓 Fetching price data... <br />
        Check browser console for logs (F12)
      </div>
    );
  }

  const chartData = {
    labels: filteredData.map(p => p.Date),
    datasets: [
      {
        label: 'Brent Oil Price',
        data: filteredData.map(p => p.Price),
        fill: false,
        borderColor: 'blue',
        pointRadius: 0,
        tension: 0.3,
      },
      ...bayesianCP
        .map(cp => priceData[cp])
        .filter(d => d && d.Date >= dateRange.start && d.Date <= dateRange.end)
        .map(d => ({
          label: `Bayesian CP (${d.Date.slice(0, 10)})`,
          data: filteredData.map(p => (p.Date === d.Date ? d.Price : null)),
          borderColor: 'red',
          borderDash: [10, 5],
          pointRadius: 6,
          borderWidth: 2
        })),
      ...ruptureCP
        .map(cp => priceData[cp])
        .filter(d => d && d.Date >= dateRange.start && d.Date <= dateRange.end)
        .map(d => ({
          label: `Rupture CP (${d.Date.slice(0, 10)})`,
          data: filteredData.map(p => (p.Date === d.Date ? d.Price : null)),
          borderColor: 'orange',
          borderDash: [5, 5],
          pointRadius: 6,
          borderWidth: 2
        }))
    ]
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem', color: 'black' }}>
        📈 Brent Oil Change Point Dashboard
      </h1>

      {/* Filter Controls */}
      <div style={{ marginBottom: '1rem', fontSize: '16px' }}>
        <label>Date Range:&nbsp;</label>
        <input type="date" value={dateRange.start} onChange={e => setDateRange({ ...dateRange, start: e.target.value })} />
        &nbsp;to&nbsp;
        <input type="date" value={dateRange.end} onChange={e => setDateRange({ ...dateRange, end: e.target.value })} />
      </div>

      {/* Key Indicators */}
      <div style={{ marginBottom: '1rem', fontSize: '16px' }}>
        <strong>Volatility:</strong> {volatility} &nbsp;|&nbsp;
        <strong>Avg Log Return:</strong> {avgLogReturn}%
      </div>

      <Line data={chartData} />
    </div>
  );
}

export default App;
