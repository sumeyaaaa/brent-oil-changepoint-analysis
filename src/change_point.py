import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import ruptures as rpt
import aesara.tensor as at

def detect_single_bayesian_changepoint(data, n_samples=3000):
    """Single change point detection using PyMC v4 (Aesara backend)."""
    n = len(data)
    idx = np.arange(n)  # use NumPy array, not Aesara

    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)

        mu_1 = pm.Normal('mu_1', mu=0, sigma=1)
        mu_2 = pm.Normal('mu_2', mu=0, sigma=1)

        sigma_1 = pm.HalfNormal('sigma_1', sigma=1)
        sigma_2 = pm.HalfNormal('sigma_2', sigma=1)

        # Use pm.math.switch instead of aesara.tensor.switch
        mu = pm.math.switch(idx < tau, mu_1, mu_2)
        sigma = pm.math.switch(idx < tau, sigma_1, sigma_2)

        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=data)

        trace = pm.sample(n_samples, tune=1000, cores=2, progressbar=True)

    change_idx = int(np.mean(trace.posterior['tau'].values))
    return trace, change_idx




def plot_bayesian_changepoint(data, change_idx, x=None, title="Detected Bayesian Change Point", ylabel="Value"):
    if x is None:
        x = np.arange(len(data))
    plt.figure(figsize=(15, 5))
    plt.plot(x, data, label="Series")
    plt.axvline(x[change_idx], color='red', linestyle='--', label="Bayesian Change Point")
    plt.title(title)
    plt.xlabel("Date" if hasattr(x[0], "year") else "Index")
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def print_bayesian_summary(trace, change_idx, x=None):
    mu1 = float(trace.posterior['mu_1'].mean().values)
    mu2 = float(trace.posterior['mu_2'].mean().values)
    sigma1 = float(trace.posterior['sigma_1'].mean().values)
    sigma2 = float(trace.posterior['sigma_2'].mean().values)

    print("Bayesian change point at index:", change_idx)
    if x is not None:
        print("Change date:", x[change_idx])
    print(f"Mean before: {mu1:.4f}, after: {mu2:.4f}")
    print(f"Std before: {sigma1:.4f}, after: {sigma2:.4f}")

    az.plot_trace(trace, var_names=['tau', 'mu_1', 'mu_2', 'sigma_1', 'sigma_2'])
    plt.show()

def detect_multiple_ruptures(data, model="l2", n_bkps=5, pen=None, show_plot=True, x=None, title="Ruptures Detected Change Points", ylabel="Value"):
    algo = rpt.Pelt(model=model) if pen is not None else rpt.KernelCPD(kernel="rbf")
    data_ = data.reshape(-1, 1) if data.ndim == 1 else data

    if pen is not None:
        bkps = algo.fit(data_).predict(pen=pen)
    else:
        algo = rpt.Binseg(model=model).fit(data_)
        bkps = algo.predict(n_bkps=n_bkps)

    if show_plot:
        rpt.display(data, bkps, figsize=(15, 5))
        plt.title(title)
        plt.xlabel("Date" if (x is not None and hasattr(x[0], "year")) else "Index")
        plt.ylabel(ylabel)
        plt.show()

    return bkps[:-1]

def link_change_points_to_events(bkps, dates, events_df, window_days=30):
    links = []
    event_dates = pd.to_datetime(events_df['Date'])
    for idx in bkps:
        cp_date = pd.to_datetime(dates[idx])
        diffs = (event_dates - cp_date).abs().dt.days
        within_window = diffs <= window_days
        if within_window.any():
            nearest_idx = diffs[within_window].idxmin()
            event = events_df.loc[nearest_idx]
            links.append((idx, cp_date, event['Event'], event['Date'], diffs[nearest_idx]))
        else:
            links.append((idx, cp_date, None, None, None))
    return links

def annotate_event_links(ax, links, y_pos, color='red'):
    for idx, cp_date, event, event_date, days_diff in links:
        if event is not None:
            ax.annotate(f"{event} ({event_date.date()})", xy=(cp_date, y_pos), xycoords=('data', 'data'),
                        xytext=(0, 15), textcoords='offset points', arrowprops=dict(arrowstyle="->", color=color),
                        fontsize=8, rotation=90, color=color)
