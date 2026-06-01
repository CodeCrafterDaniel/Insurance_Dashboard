import pandas as pd
import plotly.graph_objects as go

def create_structure_graph():
    df_structure = pd.read_excel('Статистика_по_рынку_Банк_России.xlsx', sheet_name='Структура страховых премий')

    companies = [col for col in df_structure.columns if col != 'Год']

    fig_structure = go.Figure()
    colors = ['#f81919', '#ff8000', '#ffed02', '#bce211', '#27b621', '#13c2f9', '#13d4c7']

    for idx, company in enumerate(companies):
        fig_structure.add_trace(go.Bar(
            name=company,
            x=df_structure['Год'],
            y=df_structure[company],
            text=df_structure[company],
            texttemplate='%{text:.1f}%',  # Отображение с одним знаком после запятой
            textposition='outside',  # Текст снаружи столбца
            width=0.6,  # Сужение столбцов (по умолчанию 0.8)
            marker_color = colors[idx % len(colors)]
        ))

    fig_structure.update_layout(
        title='Доля страховых компаний по годам (2017–2025)',
        barmode='stack',
        height=600,
        yaxis=dict(title='Доля (%)'),
        xaxis_title='Год',
        legend=dict(
            orientation='v',
            xanchor='left',
            yanchor='top',
        ),
    )

    return fig_structure

