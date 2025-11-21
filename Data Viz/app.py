from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
import os

app = Flask(__name__)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
df = pd.read_csv("cleaned_integrated_nyc_crashes.csv")

df["BOROUGH"] = df["BOROUGH"].fillna("UNKNOWN")
df["CRASH_YEAR"] = pd.to_datetime(df["CRASH DATE"], errors="coerce").dt.year
df["CRASH_MONTH"] = pd.to_datetime(df["CRASH DATE"], errors="coerce").dt.month_name()

month_order = ["January","February","March","April","May","June","July","August",
               "September","October","November","December"]

# ------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------
@app.route("/")
def index():
    total_crashes = len(df)

    total_injuries = df[[c for c in df.columns if "INJUR" in c.upper()]].sum().sum()

    fatal_cols = [c for c in df.columns if "KILLED" in c.upper()]
    total_fatal = df[fatal_cols].sum().sum()

    return render_template("index.html",
                           total_crashes=f"{total_crashes:,}",
                           total_injuries=f"{total_injuries:,}",
                           total_fatal=f"{total_fatal:,}")


# ------------------------------------------------------------
# REPORT GENERATOR PAGE (DROPDOWNS + SEARCH)
# ------------------------------------------------------------
@app.route("/report")
def report_page():
    years = sorted(df["CRASH_YEAR"].dropna().unique())
    vehicle_types = sorted(df["VEHICLE TYPE CODE 1"].dropna().unique())
    factors = sorted(df["CONTRIBUTING FACTOR VEHICLE 1"].dropna().unique())
    injury_cols = [c for c in df.columns if "INJUR" in c.upper() or "KILLED" in c.upper()]

    return render_template("report.html",
                           years=years,
                           vehicles=vehicle_types,
                           factors=factors,
                           injuries=injury_cols)


# ------------------------------------------------------------
# FILTER ENDPOINT — ALL CHARTS UPDATE TOGETHER
# ------------------------------------------------------------
@app.route("/filter")
def filter_data():

    borough = request.args.get("borough", "")
    year = request.args.get("year", "")
    vehicle = request.args.get("vehicle", "")
    factor = request.args.get("factor", "")
    injury = request.args.get("injury", "")
    search = request.args.get("search", "").lower()

    dff = df.copy()

    if borough != "":
        dff = dff[dff["BOROUGH"] == borough]

    if year != "":
        dff = dff[dff["CRASH_YEAR"] == int(year)]

    if vehicle != "":
        dff = dff[dff["VEHICLE TYPE CODE 1"].str.contains(vehicle, na=False)]

    if factor != "":
        dff = dff[dff["CONTRIBUTING FACTOR VEHICLE 1"].str.contains(factor, na=False)]

    if injury != "":
        dff = dff[dff[injury] > 0]

    # SEARCH MODE
    if search:
        if "brooklyn" in search:
            dff = dff[dff["BOROUGH"] == "BROOKLYN"]
        if "queens" in search:
            dff = dff[dff["BOROUGH"] == "QUEENS"]
        if "bronx" in search:
            dff = dff[dff["BOROUGH"] == "BRONX"]
        if "manhattan" in search:
            dff = dff[dff["BOROUGH"] == "MANHATTAN"]

        # Detect Year
        for y in range(2010, 2030):
            if str(y) in search:
                dff = dff[dff["CRASH_YEAR"] == y]

        if "pedestrian" in search:
            dff = dff[dff["NUMBER OF PEDESTRIANS INJURED"] > 0]

    # -----------------------------------------------
    # Borough Chart
    # -----------------------------------------------
    b = dff["BOROUGH"].value_counts().reset_index()
    b.columns = ["BOROUGH", "COUNT"]
    fig_b = px.bar(b, x="BOROUGH", y="COUNT", title="Crashes by Borough", color="BOROUGH")
    plot_borough = fig_b.to_html(full_html=False)

    # -----------------------------------------------
    # Monthly Trend Chart
    # -----------------------------------------------
    dff2 = dff.copy()
    dff2["CRASH_MONTH"] = pd.Categorical(dff2["CRASH_MONTH"], categories=month_order, ordered=True)

    m = dff2.groupby("CRASH_MONTH").size().reset_index(name="Count")

    fig_m = px.line(m, x="CRASH_MONTH", y="Count", markers=True, title="Monthly Trends")
    plot_trend = fig_m.to_html(full_html=False)

    # -----------------------------------------------
    # Injuries Pie
    # -----------------------------------------------
    injury_columns = [c for c in df.columns if "INJUR" in c.upper() or "KILLED" in c.upper()]
    inj = dff[injury_columns].sum().reset_index()
    inj.columns = ["Type", "Count"]

    fig_i = px.pie(inj, names="Type", values="Count", title="Injury Breakdown")
    plot_injury = fig_i.to_html(full_html=False)

    # -----------------------------------------------
    # Heatmap
    # -----------------------------------------------
    df_map = dff.dropna(subset=["LATITUDE", "LONGITUDE"])
    map_obj = folium.Map(location=[40.7128, -74.006], zoom_start=11, tiles="CartoDB Positron")

    if not df_map.empty:
        HeatMap(df_map[["LATITUDE", "LONGITUDE"]].values.tolist(), radius=7).add_to(map_obj)

    map_path = "static/map.html"
    map_obj.save(map_path)

    return render_template("filtered.html",
                           borough_plot=plot_borough,
                           trend_plot=plot_trend,
                           injury_plot=plot_injury,
                           map_path=map_path)


# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
