import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from graphs.profitability_graph import create_profitability_graph
from graphs.structure_graph import create_structure_graph
from graphs.volume_graph import create_volume_graph

# ---------------- PAGE ----------------
st.set_page_config(page_title="Travel Insurance Market Dashboard", layout="wide")

st.title("Travel Insurance Market Dashboard")
st.subheader("Обзор рынка")

# ---------------- DATA ----------------
all_sheets = pd.read_excel('Статистика_по_рынку_Банк_России.xlsx', sheet_name=None)

# ---------------- STREAMLIT ----------------
page = st.selectbox(
    "Выберите аналитический отчет:",
    ["Обзор страхового рынка", "Анализ страхования путешественников"]
)

if page == "Обзор страхового рынка":
    st.plotly_chart(create_volume_graph(), width='stretch')

    fig1 = create_profitability_graph()
    fig2 = create_structure_graph()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, width='stretch')
    with col2:
        st.plotly_chart(fig2, width='stretch')

    st.caption(
        "Источник: https://www.cbr.ru/analytics/insurance/overview_insurers/#a_108340"
    )

    # ============================================================
    # MARKET STRUCTURE
    # ============================================================

    # ---------- common colors ----------
    insurance_colors = {
        "Страхование жизни": "#003f5c",
        "Страхование от НС и болезней": "#2f4b7c",
        "ДМС": "#665191",
        "Автострахование (КАСКО)": "#a05195",
        "Имущество юрлиц": "#d45087",
        "Имущество граждан (ФЛ)": "#f95d6a",
        "ОСАГО": "#ff7c43",
        "Прочие виды": "#ffa600"
    }

    st.subheader("Структура страхового рынка")

    # ---------- sheets ----------
    df_premium = all_sheets['Страхования (Сумма премий)']
    df_contracts = all_sheets['Страхования (Кол-во премий)']
    df_claim_sum = all_sheets['Страхования (Сумма выплат)']
    df_claim_count = all_sheets['Страхования (Кол-во выплат)']

    # ---------- mode ----------
    mode = st.radio(
        "Режим отображения",
        ["Composition", "Dynamics"],
        horizontal=True
    )

    # ============================================================
    # COMPOSITION
    # ============================================================
    if mode == "Composition":

        year = st.selectbox(
            "Выберите год",
            sorted(df_premium["Год"].unique(), reverse=True)
        )


        def get_year_data(df):

            row = df[df["Год"] == year].iloc[0]

            labels = df.columns[1:]
            values = row[1:]

            return labels, values


        # ---------- helper ----------
        def donut_chart(
                labels,
                values,
                title,
                center_text,
                show_legend=False
        ):

            colors = [
                insurance_colors.get(
                    label,
                    None
                )
                for label in labels
            ]

            fig = go.Figure(
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.60,

                    # только проценты
                    textinfo="percent",

                    marker=dict(
                        colors=colors
                    ),

                    hovertemplate=
                    "<b>%{label}</b><br>"
                    "Доля: %{percent}<br>"
                    "Значение: %{value:,.0f}"
                    "<extra></extra>",

                    sort=False
                )
            )

            fig.update_layout(
                title=title,
                height=500,

                showlegend=show_legend,

                legend=dict(
                    orientation="h",
                    y=-0.20,
                    x=0.5,
                    xanchor="center",
                    font=dict(size=10)
                ),

                annotations=[
                    dict(
                        text=center_text,
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font_size=20
                    )
                ],

                margin=dict(
                    t=60,
                    b=100,
                    l=20,
                    r=20
                )
            )

            return fig


        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        # ---------- Premiums ----------
        # ---------- Premiums ----------
        labels, values = get_year_data(df_premium)

        with row1_col1:
            st.plotly_chart(
                donut_chart(
                    labels,
                    values,
                    "Сумма премий",
                    f"{sum(values):,.0f}<br>млн ₽",
                    show_legend=True
                ),
                width='stretch'
            )

        # ---------- Contracts ----------
        labels, values = get_year_data(df_contracts)

        with row1_col2:
            st.plotly_chart(
                donut_chart(
                    labels,
                    values,
                    "Количество договоров",
                    f"{sum(values):,.0f}<br>договоров",
                    show_legend=True
                ),
                width='stretch'
            )

        # ---------- Claim count ----------
        labels, values = get_year_data(df_claim_count)

        with row2_col1:
            st.plotly_chart(
                donut_chart(
                    labels,
                    values,
                    "Количество выплат",
                    f"{sum(values):,.0f}<br>выплат",
                    show_legend=True
                ),
                width='stretch'
            )

        # ---------- Claim sum ----------
        labels, values = get_year_data(df_claim_sum)

        with row2_col2:
            st.plotly_chart(
                donut_chart(
                    labels,
                    values,
                    "Сумма выплат",
                    f"{sum(values):,.0f}<br>млн ₽",
                    show_legend=True
                ),
                width='stretch'
            )

    # ============================================================
    # DYNAMICS
    # ============================================================
    else:

        metric_name = st.selectbox(
            "Метрика",
            [
                "Премии",
                "Договоры",
                "Кол-во выплат",
                "Сумма выплат"
            ]
        )

        metric_map = {
            "Премии": df_premium,
            "Договоры": df_contracts,
            "Кол-во выплат": df_claim_count,
            "Сумма выплат": df_claim_sum
        }

        df_dyn = metric_map[metric_name].copy()

        df_dyn = df_dyn.set_index("Год")

        # 100% shares
        df_share = (
                df_dyn
                .div(df_dyn.sum(axis=1), axis=0)
                * 100
        )

        fig = go.Figure()

        for col in df_share.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_share.index,
                    y=df_share[col],
                    stackgroup='one',
                    mode='lines',
                    name=col
                )
            )

        fig.update_layout(
            title=f"Динамика структуры рынка — {metric_name}",
            yaxis_title="Доля рынка (%)",
            height=600,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

        # ---------- Insight ----------
        latest_year = df_share.index.max()
        leader = (df_share.loc[latest_year].idxmax())

        leader_share = (df_share.loc[latest_year].max())
        st.info(
            f"""
            📊 **Инсайт**

            В {latest_year} году крупнейшую долю по метрике
            **{metric_name}**
            занимает
            **{leader}**
            — {leader_share:.1f}% рынка.
            """
        )

    st.caption(
        "Источник: https://www.cbr.ru/statistics/insurance/ssd_stat/#a_130716file"
    )


else:
    SBER = {"primary": "#21A038", "secondary": "#37C871", "accent": "#7EE8A6", "light": "#CFF5DD", "mint": "#EAFBF0",
            "dark": "#0E7A29", "gray": "#7A7A7A", "bg": "#F7FAF8"}
    # ============================================================
    # TAB 2 — SBER PRODUCT DASHBOARD
    # ============================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Сумма сборов",
            "1.25 млрд ₽",
            "+14%"
        )

    with c2:
        st.metric(
            "Покупатели",
            "620 тыс.",
            "+9%"
        )

    with c3:
        st.metric(
            "Средний чек",
            "2 020 ₽",
            "+4%"
        )

    with c4:
        st.metric(
            "Конверсия",
            "3.8%",
            "+0.6 п.п."
        )

    st.divider()

    # --------------------------------------------------------
    # FUNNEL + INSIGHTS
    # --------------------------------------------------------

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Customer Funnel")

        stages = [
            "Visitors",
            "Quotes",
            "Checkout",
            "Purchase"
        ]

        values = [
            10000,
            4200,
            2200,
            1000
        ]

        funnel = go.Figure(
            go.Funnel(
                y=stages,
                x=values,

                textinfo=
                "value+percent initial+percent previous",

                textposition="inside",

                marker=dict(
                    color=[
                        SBER["light"],
                        "#A6E7BF",
                        SBER["secondary"],
                        SBER["primary"]
                    ],

                    line=dict(
                        color="white",
                        width=2
                    )
                ),

                connector=dict(
                    line=dict(
                        color="#E0E0E0",
                        width=1
                    )
                )
            )
        )

        funnel.update_layout(
            height=360,
            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
            ),
            showlegend=False,
            template="plotly_white"
        )

        st.plotly_chart(
            funnel,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    with right:
        st.subheader("Funnel Insights")
        ctr_quotes = (values[1] / values[0]) * 100
        checkout_conversion = (values[3] / values[2]) * 100
        total_conversion = (values[3] / values[0]) * 100

        st.metric(
            "Visitors → Quotes",
            f"{ctr_quotes:.1f}%"
        )

        st.metric(
            "Checkout → Purchase",
            f"{checkout_conversion:.1f}%"
        )

        st.metric(
            "Total Conversion",
            f"{total_conversion:.1f}%"
        )

        st.info(
            """
Основная потеря пользователей
происходит между этапами
**Quotes → Checkout**.

Это потенциальная зона
для улучшения UX и оффера.
"""
        )

    st.divider()

    # --------------------------------------------------------
    # BUYERS + REVENUE
    # --------------------------------------------------------

    st.subheader(
        "Product Dynamics"
    )

    left, right = st.columns(2)

    # ---------------- Buyers ----------------

    with left:
        buyers_df = pd.DataFrame({
            "Month": [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug"
            ],
            "Buyers": [
                35, 42, 48, 52,
                61, 70, 84, 92
            ]
        })

        fig_buyers = go.Figure()

        fig_buyers.add_trace(
            go.Scatter(
                x=buyers_df["Month"],
                y=buyers_df["Buyers"],

                mode="lines+markers",

                line=dict(
                    color=SBER["primary"],
                    width=4
                ),

                marker=dict(
                    size=8
                ),

                fill="tozeroy"
            )
        )

        fig_buyers.update_layout(
            title="Покупатели в динамике",
            height=350,
            hovermode="x unified",
            yaxis_title="тыс. покупателей"
        )

        st.plotly_chart(
            fig_buyers,
            width="stretch"
        )

    # ---------------- Revenue ----------------

    with right:
        revenue_df = pd.DataFrame({
            "Month": [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug"
            ],
            "Revenue": [
                55, 62, 68, 75,
                90, 105, 120, 140
            ]
        })

        fig_rev = go.Figure()

        fig_rev.add_trace(
            go.Bar(
                x=revenue_df["Month"],
                y=revenue_df["Revenue"],

                marker_color=
                SBER["secondary"]
            )
        )

        fig_rev.update_layout(
            title="Сборы в динамике",
            height=350,
            yaxis_title="млн ₽"
        )

        st.plotly_chart(
            fig_rev,
            width="stretch"
        )

    st.divider()

    # --------------------------------------------------------
    # SBER VS COMPETITORS
    # --------------------------------------------------------

    st.subheader(
        "Сбер vs конкуренты"
    )

    companies = [
        "Сбер",
        "Альфа",
        "Т-Банк",
        "Ингосстрах",
        "РЕСО"
    ]

    buyers = [
        620,
        520,
        390,
        310,
        280
    ]

    fig_comp = go.Figure()

    fig_comp.add_trace(
        go.Bar(
            x=buyers,
            y=companies,

            orientation="h",

            text=buyers,
            textposition="outside",

            marker=dict(
                color=[
                    SBER["primary"],
                    "#C9C9C9",
                    "#C9C9C9",
                    "#C9C9C9",
                    "#C9C9C9"
                ]
            ),

            hovertemplate=
            "<b>%{y}</b><br>"
            "Покупатели: %{x} тыс."
            "<extra></extra>"
        )
    )

    fig_comp.update_layout(
        title=
        "Количество покупателей Travel Insurance",
        height=420,
        showlegend=False,
        xaxis_title="тыс. покупателей"
    )

    fig_comp.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig_comp,
        width="stretch"
    )

    st.caption(
        "Mockup competitor benchmark"
    )
