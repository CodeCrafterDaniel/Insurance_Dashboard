import pandas as pd
import plotly.graph_objects as go

def create_volume_graph(df_volume):

    df_volume["Премии (за квартал)"] = df_volume["Премии (за квартал)"] / 1000
    df_volume["Выплаты (за квартал)"] = df_volume["Выплаты (за квартал)"] / 1000

    fig_volume = go.Figure()

    # Левая ось — млрд руб
    fig_volume.add_trace(
        go.Bar(
            x=df_volume["Дата"],
            y=df_volume["Премии (за квартал)"],
            name="Премии (за квартал) (млн. руб.)"
        )
    )

    fig_volume.add_trace(
        go.Bar(
            x=df_volume["Дата"],
            y=df_volume["Выплаты (за квартал)"],
            name="Выплаты (за квартал) (млн. руб.)"
        )
    )

    # Правая ось — %
    fig_volume.add_trace(
        go.Scatter(
            x=df_volume["Дата"],
            y=df_volume["Темп прироста премий, г/г (правая шкала)"],
            name="Темп прироста премий, г/г %",
            mode="lines+markers",
            yaxis="y2"
        )
    )

    fig_volume.add_trace(
        go.Scatter(
            x=df_volume["Дата"],
            y=df_volume["Темп прироста выплат г/г (правая шкала)"],
            name="Темп прироста выплат г/г %",
            mode="lines+markers",
            yaxis="y2"
        )
    )

    # Layout
    fig_volume.update_layout(
        title="Динамика премий и выплат всего страхового сектора",
        barmode="group",
        height=600,

        yaxis=dict(
            title="Млрд. руб."
        ),

        yaxis2=dict(
            title="Прирост %",
            overlaying="y",
            side="right",
            showgrid=False
        ),

        legend=dict(
            orientation="h",
            y=1.1
        )
    )

    return fig_volume