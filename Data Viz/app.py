import os
print("WORKING DIRECTORY:", os.getcwd())

from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load dataset
df = pd.read_csv("cleaned_integrated_nyc_crashes.csv")

# Fix columns
df["CRASH_YEAR"] = pd.to_numeric(df["CRASH_YEAR"], errors="coerce").fillna(0).astype(int)
df["CRASH_MONTH"] = pd.to_numeric(df["CRASH_MONTH"], errors="coerce").fillna(0).astype(int)
df["BOROUGH"] = df["BOROUGH"].fillna("UNKNOWN")

# ---------------------------
# Home Page
# ---------------------------
@app.route("/")
def index():
    total = len(df)
    injuries = df[[c for c in df.columns if "INJUR" in c.upper()]].sum().sum()
    fatalities = df[[c for c in df.columns if "FATAL" in c.upper()]].sum().sum()

    return render_template("index.html",
                           total_crashes=f"{total:,}",
                           total_injuries=f"{injuries:,}",
                           total_fatalities=f"{fatalities:,}")


# ---------------------------
# Borough Page
# ---------------------------
@app.route("/boroughs")
def boroughs_page():

    borough_counts = (
        df["BOROUGH"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "BOROUGH", "BOROUGH": "COUNT"})
    )

    fig = px.bar(borough_counts, x="BOROUGH", y="COUNT",
                 title="Crashes per Borough")
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("boroughs.html", plot=graph_html)


# ---------------------------
# Injuries Page
# ---------------------------
@app.route("/injuries")
def injuries_page():

    cols = [c for c in df.columns if "INJUR" in c.upper() or "FATAL" in c.upper()]

    yearly = df.groupby("CRASH_YEAR")[cols].sum().reset_index()

    fig = px.line(yearly, x="CRASH_YEAR", y=cols,
                  markers=True,
                  title="Injuries & Fatalities by Year")

    graph_html = pio.to_html(fig, full_html=False)

    return render_template("injuries.html", plot=graph_html)


# ---------------------------
# Trends Page
# ---------------------------
@app.route("/trends")
def trends_page():

    monthly = (
        df.groupby(["CRASH_YEAR", "CRASH_MONTH"])
        .size()
        .reset_index(name="count")
    )

    monthly["Month"] = monthly["CRASH_MONTH"].apply(
        lambda x: pd.to_datetime(str(x), format='%m').strftime('%b')
    )

    fig = px.line(monthly, x="Month", y="count", color="CRASH_YEAR",
                  title="Monthly Crash Trends")
    
    fig.update_traces(mode="lines+markers")

    graph_html = pio.to_html(fig, full_html=False)

    return render_template("trends.html", plot=graph_html)


# ---------------------------
# Run Local Server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
