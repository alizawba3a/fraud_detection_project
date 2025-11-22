# Data-Visualization
👥 Team Members
Name	Contribution
Ahmed Elsegeny	Built the full Flask website using VS Code
Ali	Built the full Flask website using VS Code
Saeed	Worked on the Google Colab notebook for data cleaning & preprocessing
Marwan	Worked on the Google Colab notebook for data cleaning & preprocessing
All Members	Participated equally in planning, design, testing & report preparation
📌 Project Overview

This project analyzes Motor Vehicle Collision Data in New York City and provides:

🟦 Interactive charts and graphs

🌍 Borough-based crash summaries

🩺 Injury & fatality statistics

🔍 Search and filter features

🗺 Geographic visualization (heatmaps & accident locations)

📄 Auto-generated PDF/HTML reports

🌐 Fully deployed live website (PythonAnywhere)

The system is implemented using:

Python 3

Flask

Pandas

Plotly Express

Folium

HTML / CSS / JS

💾 Dataset

The dataset used is:

Motor Vehicle Collisions — NYC
cleaned_integrated_nyc_crashes.csv


Preprocessing steps (done in Google Colab by Saeed & Marwan):

Cleaning null values

Standardizing column names

Fixing date/time formats

Integrating crash + injury + borough data

Exporting final cleaned CSV

💻 Website Features
1. Home Dashboard

Total crashes

Total injuries

Total fatalities

2. Borough Analysis Page

Borough-wise crash counts

Year filter

Injury type comparisons

3. Trend Analysis Page

Crashes over time

Vehicle type patterns

Contributing factors

4. Search & Filtering

Users can type natural queries such as:

“Brooklyn 2022 pedestrian crashes”

And the system displays filtered results instantly.

5. Report Generator

A single button instantly generates a dynamic report page with updated charts based on filters.

6. Deployment

The final system is deployed online using:

PythonAnywhere

WSGI configuration

Production-ready folder structure

📂 Project Structure
/dataviz
 ├── app.py
 ├── cleaned_integrated_nyc_crashes.csv
 ├── templates/
 ├── static/
 ├── requirements.txt
 ├── wsgi.py

🚀 How to Run Locally

Install requirements:

pip install -r requirements.txt


Run Flask app:

python app.py


Open in browser:

http://127.0.0.1:5000/

🌐 Deployment (PythonAnywhere)

Uploaded ZIP via dashboard

Unzipped into /home/username/

Installed requirements

Created wsgi.py

Configured static & template directories

Reloaded web app to publish

📘 Final Notes

The project was developed collaboratively and all team members worked equally.

VS Code implementation by Ahmed & Ali.

Colab notebook and preprocessing by Saeed & Marwan.

Entire team participated in debugging, testing, and final report.
