import pandas as pd
from plotly.offline import plot
import plotly.express as px


def plot_hist(df: pd.DataFrame, col: str) -> px.histogram:

    fig = px.histogram(
        df, col, template="plotly_dark", barmode="overlay", color=col
    )

    # Установка прозрачного фона
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )
    fig.update_traces(marker=dict(line=dict(color="rgba(0,0,0,0)", width=0.5)))
    return fig


def plot_time_series(df: pd.DataFrame, value_col: str) -> px.line:
    date_col = "Дата"
    df[date_col] = pd.to_datetime(
        df[date_col]
    )  # Convert the date column to datetime
    df["Date"] = df[date_col].dt.date  # Extract the date from the datetime

    fig = px.line(
        df.groupby("Date").size().reset_index(name="Count"),
        x="Date",
        y="Count",
        template="plotly_dark",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)"
    )
    fig.update_traces(
        marker=dict(line=dict(color="rgba(0, 0, 0, 0)", width=0.5))
    )
    return fig
