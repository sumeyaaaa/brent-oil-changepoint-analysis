# Brent Oil Change Point Analysis (1987–2022)

Brent crude oil prices have undergone dramatic swings over the past three and a half decades, driven by geopolitical events, macroeconomic cycles, policy shifts, and unexpected crises. This repository explores those dynamics by detecting and visualising change points—dates where the statistical behaviour of the price time series changes markedly—and then aligning those change points with major world events. The work combines probabilistic modelling, classic time‑series methods, and an interactive dashboard to allow stakeholders to both reproduce the analysis and explore the results.

This project was completed for the 10 Academy Week 10 challenge in collaboration with Birhan Energies. It aims to deliver actionable intelligence for analysts, investors, and policymakers in the energy sector, empowering them to understand why the oil market changes and to anticipate future shifts.

## 📂 Repository Structure

The codebase is divided into logical pieces for data ingestion, modelling, visualisation, and documentation. The high‑level layout looks like this:

brent-oil-changepoint-analysis/
├── backend/ # Flask backend serving data and analysis results via a REST API
│ ├── app.py # Main Flask application exposing /api endpoints
│ └── ... # Model invocation, configuration and other backend helpers
├── data/ # Input datasets
│ ├── BrentOilPrices.csv # Daily Brent spot prices (1987–2022)
│ └── key_events_100.csv # Key political/economic events with dates and types
├── frontend/ # React dashboard built with Vite
│ ├── src/ # Front‑end source code
│ │ ├── App.jsx # Main React component rendering charts and filters
│ │ └── main.jsx # Entry point mounting the React app
│ ├── index.html # HTML entry file for Vite
│ ├── package.json # Front‑end dependencies and scripts
│ └── vite.config.js # Development server and proxy configuration
├── notebooks/ # Jupyter notebooks for exploratory analysis and modelling
│ ├── task‑1/ # Data loading, cleaning and descriptive statistics
│ │ └── Load_Eda.ipynb # Exploratory data analysis and log return computation
│ └── task‑2/ # Modelling notebooks
│ └── modeling.ipynb # Bayesian change point modelling and validation
├── src/ # Python modules used by the notebooks and backend
│ ├── change_point.py # Bayesian change point detection (PyMC3) and Ruptures models
│ ├── data_load.py # Utilities to load and preprocess the CSV data
│ └── events_table_preparing.py # Scripts to prepare the events dataset
├── requirements.txt # Python dependencies for backend and notebooks
├── LICENSE # Open‑source license
└── README.md # Project overview and instructions (this file)

sql_more

Copy

## 🔍 Project Summary

The objective is to identify and interpret structural breaks in the Brent oil price series and relate them to historically significant events. We:

- Detect change points using a Bayesian model implemented with PyMC3. The model treats the date of a structural break (e.g., a change in mean price) as an unknown parameter and infers it via Markov Chain Monte Carlo sampling. A complementary approach using the ruptures library finds multiple breakpoints offline.
- Compute log returns and volatility to investigate volatility clustering—periods where price variability remains high following a shock.
- Compile a timeline of 100 key events (wars, OPEC announcements, financial crises, pandemics, and sanctions) and match them against detected change points.
- Build an interactive dashboard so users can explore the price series, change points, events, and key indicators in one place. The dashboard allows filtering by date range and computes average log return and volatility for the selected period, highlighting how specific events correspond to spikes or drops in price.

Our analysis reveals that many identified change points coincide with notable events: the Gulf War (1990), the Asian Financial Crisis (1997), the 2008 Global Financial Crisis, the COVID‑19 pandemic, and the Russia–Ukraine war. Visualising these relationships helps explain market behaviour and provides context for forecasting and risk management.

## ⚙️ Installation and Setup

### 1. Python Backend Setup

1. Create a virtual environment (recommended):

    ```
    python -m venv .venv
    # On Mac/Linux:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    ```

2. Install backend dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Run the Flask server:

    ```
    python backend/app.py
    ```

    - API runs at: http://localhost:5000/
    - Endpoints:
        - `/api/price-data` — daily price series (JSON)
        - `/api/change-points/bayesian` — Bayesian change point index
        - `/api/change-points/ruptures` — ruptures change point indices
        - `/api/events` — list of key events

---

### 2. JavaScript Frontend (React)

1. Install Node and npm (if needed):  
   [Node.js official download](https://nodejs.org/en/download/)

2. Install frontend dependencies:

    ```
    cd frontend
    npm install
    ```

3. Start the React development server:

    ```
    npm run dev
    ```

    - Dashboard: http://localhost:5173/

4. Build for production (optional):

    ```
    npm run build
    ```

---

### 3. Jupyter Notebooks

- Data loading and EDA:  
  `notebooks/task-1/Load_Eda.ipynb`

- Bayesian change point modeling:  
  `notebooks/task-2/modeling.ipynb`

    ```
    jupyter lab
    ```

---

### 4. Features and Methodology

- Bayesian Change Point Detection (PyMC3)
- Multiple Change Point Detection (`ruptures`)
- Volatility and Returns (log returns, rolling std)
- Event Correlation (100+ events, color-coded dashboard)
- Interactive Dashboard (React + Flask API)

---

### 5. Technologies Used

- Python (3.8+): pandas, NumPy, Matplotlib
- PyMC3: Bayesian inference
- ruptures: change point detection
- Flask: backend API
- React & Vite: frontend
- Chart.js (via react-chartjs-2): charting
- Jupyter Notebook/Lab: exploration & analysis

---

### 6. Author

Sumeyaa Sir  
10 Academy – Birhan Energies Project

---

### 7. License

MIT License

