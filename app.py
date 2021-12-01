from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly
import plotly.express as px
import json
import subprocess

app = Flask(__name__)

# Load preprocessed data once (outside the route for efficiency)
df = pd.read_csv("data/pernambuco_co2_clean.csv")
sectors = df['sector'].unique().tolist()
min_year = int(df['year'].min())
max_year = int(df['year'].max())


@app.cli.command("run-preprocess")
def run_preprocess():
    """Run CO2 data preprocessing"""
    try:
        # Run your preprocessing script
        subprocess.run(["python", "preprocess.py"], check=True, shell=True)
        print("✅ Preprocessing completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Preprocessing failed: {e}")
    except FileNotFoundError:
        print("❌ Error: preprocess.py not found")


@app.route("/api/emissions", methods=["GET"])
def get_emissions():
    global df  # Use the DataFrame loaded at startup

    # Get filter parameters from the request
    selected_sectors = request.args.getlist("sectors")
    start_year = int(request.args.get("start_year", default=min_year))
    end_year = int(request.args.get("end_year", default=max_year))

    # Filter data
    filtered_df = df[
        (df["sector"].isin(selected_sectors))
        & (df["year"] >= start_year)
        & (df["year"] <= end_year)
    ]

    # Create the plot
    fig = px.line(
        filtered_df,
        x="year",
        y="emissions_metric_tons",
        color="sector",
        title="Emissão de CO2 em Pernambuco por Setor",
        labels={"emissions_metric_tons": "Emissões (Tonelada Métrica)"},
    )

    # Convert plot to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graph_json)


@app.route("/")
def index():
    return render_template(
        "index.html",
        sectors=sectors,
        selected_sectors=sectors,
        min_year=min_year,
        max_year=max_year,
        start_year=min_year,
        end_year=max_year,
    )


if __name__ == "__main__":
    app.run(debug=True)
