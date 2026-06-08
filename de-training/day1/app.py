import io
import base64
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker
from flask import Flask, render_template, request

app = Flask(__name__)

# Bar width for hourly data: 45 minutes expressed in matplotlib date units (days)
_BAR_WIDTH_DAYS = 45 / (60 * 24)


def fetch_and_plot(ticker: str):
    df = yf.download(ticker, period="5d", interval="1h", auto_adjust=True, progress=False)

    if df.empty:
        return None, None

    # Flatten MultiIndex columns produced by yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Ensure a clean DatetimeIndex (strip timezone for matplotlib compatibility)
    df.index = pd.to_datetime(df.index).tz_localize(None) if df.index.tzinfo is None \
        else pd.to_datetime(df.index).tz_convert(None)

    dates  = df.index.to_pydatetime()
    close  = df["Close"].to_numpy(dtype=float)
    volume = df["Volume"].to_numpy(dtype=float)

    # ---------- plot ----------
    fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
    fig.patch.set_facecolor("#0f172a")

    for ax in axes:
        ax.set_facecolor("#1e293b")
        ax.tick_params(colors="#94a3b8", labelsize=8)
        ax.xaxis.label.set_color("#94a3b8")
        ax.yaxis.label.set_color("#94a3b8")
        ax.title.set_color("#f1f5f9")
        for spine in ax.spines.values():
            spine.set_edgecolor("#334155")

    # Close price panel — zoom y-axis to data range so variation is visible
    price_min = close.min()
    price_max = close.max()
    padding   = (price_max - price_min) * 0.15 or price_min * 0.002

    axes[0].plot(dates, close, color="#38bdf8", linewidth=1.8, label="Close")
    axes[0].fill_between(dates, price_min - padding, close, alpha=0.15, color="#38bdf8")
    axes[0].set_ylim(price_min - padding, price_max + padding)
    axes[0].set_title(
        f"{ticker.upper()} — Last 5 Days  (1-hour intervals)",
        fontsize=13, fontweight="bold", pad=10,
    )
    axes[0].set_ylabel("Price (USD)", fontsize=10)
    axes[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, _: f"${x:,.2f}")
    )
    axes[0].legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="#f1f5f9")
    axes[0].grid(True, alpha=0.15, color="#475569")

    # Volume bar panel
    axes[1].bar(dates, volume, color="#818cf8", alpha=0.7, label="Volume", width=_BAR_WIDTH_DAYS)
    axes[1].set_ylabel("Volume", fontsize=10)
    axes[1].set_xlabel("Date / Time", fontsize=10)
    axes[1].legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="#f1f5f9")
    axes[1].grid(True, alpha=0.15, color="#475569")

    # X-axis formatting on the bottom subplot (shared with top)
    axes[1].xaxis.set_major_locator(mdates.HourLocator(interval=6))
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
    axes[1].tick_params(axis="x", rotation=30, colors="#94a3b8")

    plt.tight_layout(pad=2)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", facecolor=fig.get_facecolor(), bbox_inches="tight", dpi=130)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")

    # ---------- stats (safe scalar extraction) ----------
    open_price  = float(df["Open"].iloc[0])
    close_price = float(df["Close"].iloc[-1])
    high_price  = float(df["High"].max())
    low_price   = float(df["Low"].min())
    total_vol   = int(df["Volume"].sum())
    change      = round(close_price - open_price, 2)
    change_pct  = round((close_price - open_price) / open_price * 100, 2)

    stats = {
        "open":       round(open_price, 2),
        "close":      round(close_price, 2),
        "high":       round(high_price, 2),
        "low":        round(low_price, 2),
        "volume":     f"{total_vol:,}",
        "change":     change,
        "change_pct": change_pct,
    }
    return img_b64, stats


@app.route("/", methods=["GET", "POST"])
def index():
    chart = error = stats = ticker = None
    if request.method == "POST":
        ticker = request.form.get("ticker", "").strip().upper()
        if ticker:
            try:
                chart, stats = fetch_and_plot(ticker)
                if chart is None:
                    error = f'No data found for "{ticker}". Please check the ticker symbol.'
            except Exception as e:
                error = f"Error fetching data: {e}"
        else:
            error = "Please enter a ticker symbol."
    return render_template("index.html", chart=chart, stats=stats, ticker=ticker, error=error)


if __name__ == "__main__":
    app.run(debug=True)
