# 🛢️ Brent Oil Change Point Analysis (1987–2022)

## 🔍 Project Summary
Brent crude oil prices have experienced dramatic shifts from 1987 to 2022 due to geopolitical, economic, and policy events. This project analyzes the Brent oil price time series to identify change points—dates where statistical behavior changes significantly—and aligns them with major global events.

We use **Bayesian Change Point Detection** via `PyMC3`, and examine **volatility clustering** in log returns to understand persistent market instability after shocks like the **Gulf War**, **2008 Financial Crisis**, **COVID-19 Pandemic**, and the **Russia-Ukraine War**.

---

## 📂 Repository Structure

```bash
brent-oil-changepoint-analysis/
├── data/
│   ├── BrentOilPrices.csv
│   └── key_events_100.csv
├── notebooks/
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Bayesian_Change_Point_Detection.ipynb
│   ├── 03_Volatility_Clustering_Analysis.ipynb
│   └── 04_Event_Impact_Assessment.ipynb
├── src/
│   ├── models.py
│   └── utils.py
├── README.md
├── requirements.txt
└── LICENSE
```

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.9+
- Recommended: use a virtual environment

```bash
python3.9 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage (Running the Notebooks)

Run the following:

```bash
jupyter lab
```

Open the notebooks in order:
1. `01_Data_Exploration.ipynb` — EDA and log return computation
2. `02_Bayesian_Change_Point_Detection.ipynb` — PyMC3 modeling
3. `03_Volatility_Clustering_Analysis.ipynb` — Rolling volatility analysis
4. `04_Event_Impact_Assessment.ipynb` — Correlation between change points and global events

---

## 📊 Features and Methodology

- **Bayesian Change Point Detection**: Probabilistic modeling using `PyMC3` to detect structural breaks
- **Volatility Clustering Analysis**: Rolling standard deviation of log returns shows periods of market instability
- **Event Correlation**: Change points compared against 100 global events (Gulf War, OPEC shifts, etc.)
- **Validation**: `ruptures` library used for offline multi-point detection

---

## 🧰 Technologies Used

- Python 3.9
- pandas, NumPy
- matplotlib, seaborn
- PyMC3, ArviZ
- ruptures
- JupyterLab

---

## 👤 Author

**Sumeyaa Sir**  
10 Academy – Birhan Energies Project

---

## 📄 License

This project is licensed under the **APACHE License** — feel free to use, modify, and distribute with credit.