from flask import Flask, jsonify
import pandas as pd
from src.change_point import (
    detect_single_bayesian_changepoint,
    detect_multiple_ruptures
)

app = Flask(__name__)

# Global placeholders to be filled later
bayesian_cp = []
rupture_cp = []
price_df = None
events_df = None

@app.route('/api/price-data')
def get_price():
    return price_df.to_json(orient='records', date_format='iso')

@app.route('/api/change-points/bayesian')
def get_bayesian_cp():
    return jsonify({"change_points": bayesian_cp})

@app.route('/api/change-points/ruptures')
def get_rupture_cp():
    return jsonify({"change_points": rupture_cp})

@app.route('/api/events')
def get_events():
    return events_df.to_json(orient='records', date_format='iso')


if __name__ == '__main__':
    # Load data
    price_df = pd.read_csv(
        r"C:\Users\ABC\Desktop\10Acadamy\week 10\brent-oil-changepoint-analysis\data\BrentOilPrices.csv",
        parse_dates=['Date']
    )
    events_df = pd.read_csv(
        r"C:\Users\ABC\Desktop\10Acadamy\week 10\brent-oil-changepoint-analysis\data\key_events_100.csv",
        parse_dates=['Date']
    )

    data = price_df["Price"].values
    dates = price_df["Date"].values

    # Run Bayesian change point detection
    _, bayesian_cp_idx = detect_single_bayesian_changepoint(data)
    bayesian_cp = [bayesian_cp_idx]

    # Run multiple change point detection
    rupture_cp = detect_multiple_ruptures(data, model="rbf", n_bkps=7, show_plot=False)

    # Start server
    app.run(debug=True)
