import pandas as pd
import plotly.graph_objects as go

def create_profitability_graph():
    df_profitability = pd.read_excel('Статистика_по_рынку_Банк_России.xlsx', sheet_name='Рентабельность')

    fig_profitability = go.Figure()

    fig_profitability.add_trace(
        go.Bar(
            x=df_profitability["Год"],
            y=df_profitability["ROE"],
            name="ROE",
            text=df_profitability["ROE"],
            textposition="outside",
            texttemplate="%{text}%",
            marker_color="#ff0000"
        )
    )

    fig_profitability.add_trace(
        go.Bar(
            x=df_profitability["Год"],
            y=df_profitability["ROA"],
            name="ROA",
            text=df_profitability["ROA"],
            textposition="outside",
            texttemplate="%{text}%",
            marker_color="#ff9f80"
        )
    )

    # Layout
    fig_profitability.update_layout(
        title="Рентабельность страхового рынка",
        barmode="group",
        height=600,

        yaxis=dict(
            title="Проценты, %"
        ),

    legend=dict(
        orientation="h",
        y=1.1
        )
    )

    return fig_profitability