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
    col1, col2 = st.columns([2, 1])

    with col1:
        df_volume = pd.read_excel('Статистика_по_рынку_Банк_России.xlsx', sheet_name='Объем')
        st.plotly_chart(create_volume_graph(df_volume), width='stretch')

    with col2:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.metric(
                    f"Сумма премий за {df_volume.iloc[-1]['Дата']}",
                    f"{df_volume.iloc[-1]['Премии (за квартал)'] / 1000:.2f} млрд ₽",
                    f"{df_volume.iloc[-1]['Темп прироста премий, г/г (правая шкала)']:.2f}% г/г"
                )

        with c2:
            with st.container(border=True):
                st.metric(
                    f"Сумма выплат за  {df_volume.iloc[-1]['Дата']}",
                    f"{df_volume.iloc[-1]['Выплаты (за квартал)'] / 1000:.2f} млрд ₽",
                    f"{df_volume.iloc[-1]['Темп прироста выплат г/г (правая шкала)']:.2f}% г/г"
                )

        st.info(
            """
            **Анализ**

            * За анализируемый период **квартальные сборы рынка выросли почти в 3 раза** (с 400 до 1300 млрд руб.). **Исторический максимум** сборов зафиксирован в IV кв. 2024 года, что обусловлено традиционным для конца года закрытием крупных корпоративных контрактов и предновогодней активностью в авто- и розничном кредитовании.
            * **В IV кв. 2024 года зафиксирован критический скачок объема выплат**, при котором темп их прироста г/г взлетел до абсолютного максимума (около 300%).
            * К концу 2025 года **динамика прироста премий и выплат ушла в зону минимальных или отрицательных значений** (в IV кв. 2025 г. темп выплат г/г стал отрицательным), несмотря на то, что абсолютные объемы сборов остаются высокими.
            """,
            icon='📊'
        )

    fig1 = create_profitability_graph()
    fig2 = create_structure_graph()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, width='stretch')
        st.info(
            """
            **Инсайт**

            Страховой сектор демонстрирует стабильно высокую рентабельность капитала (**ROE** не опускалась ниже 20%).
            """,
            icon='💡'
        )
    with col2:
        st.plotly_chart(fig2, width='stretch')
        st.info(
            """
            **Инсайт**

            **Кредитные организации** сохраняют статус ключевого канала продаж, контролируя более половины страхового рынка (54.3% в 2024 г. и 52.0% в 2025 г.).
            """,
            icon='💡'
        )

    st.caption(
        "Источник: https://www.cbr.ru/analytics/insurance/overview_insurers/#a_108340"
    )

    st.divider()

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
        ["Срез", "Динамика"],
        horizontal=True
    )

    # ============================================================
    # COMPOSITION
    # ============================================================
    if mode == "Срез":

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
        def donut_chart(labels, values, title, center_text, show_legend=False):

            colors = [insurance_colors.get(label, None) for label in labels]

            fig = go.Figure(
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.60,

                    textinfo="percent",

                    marker=dict(colors=colors),

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

                margin=dict(t=60, b=100, l=20, r=20)
            )

            return fig


        col1, col2 = st.columns([2, 1])

        with col1:
            row1_col1, row1_col2 = st.columns(2)
            row2_col1, row2_col2 = st.columns(2)

            # ---------- Premiums ----------
            labels, values = get_year_data(df_premium)

            with row1_col1:
                st.plotly_chart(
                    donut_chart(labels, values, "Сумма премий", f"{sum(values):,.0f}<br>млн ₽", show_legend=True),
                    width='stretch'
                )

            # ---------- Contracts ----------
            labels, values = get_year_data(df_contracts)

            with row1_col2:
                st.plotly_chart(
                    donut_chart(labels, values, "Количество договоров", f"{sum(values):,.0f}<br>договоров",
                                show_legend=True),
                    width='stretch'
                )

            # ---------- Claim count ----------
            labels, values = get_year_data(df_claim_count)

            with row2_col1:
                st.plotly_chart(
                    donut_chart(labels, values, "Количество выплат", f"{sum(values):,.0f}<br>выплат", show_legend=True),
                    width='stretch'
                )

            # ---------- Claim sum ----------
            labels, values = get_year_data(df_claim_sum)

            with row2_col2:
                st.plotly_chart(
                    donut_chart(labels, values, "Сумма выплат", f"{sum(values):,.0f}<br>млн ₽", show_legend=True),
                    width='stretch'
                )

        with col2:
            st.subheader(f'Инсайты ({year} Год)')

            # =========================
            # Расчет инсайтов
            # =========================

            premium_row = df_premium[df_premium["Год"] == year].iloc[0]
            contracts_row = df_contracts[df_contracts["Год"] == year].iloc[0]
            claim_count_row = df_claim_count[df_claim_count["Год"] == year].iloc[0]
            claim_sum_row = df_claim_sum[df_claim_sum["Год"] == year].iloc[0]

            # Убираем колонку Год
            premium_data = premium_row.drop("Год")
            contracts_data = contracts_row.drop("Год")
            claim_count_data = claim_count_row.drop("Год")
            claim_sum_data = claim_sum_row.drop("Год")

            # =========================
            # Инсайт 1
            # Сумма премий vs договоры
            # =========================

            largest_premium_segment = premium_data.idxmax()
            premium_share = (premium_data[largest_premium_segment] / premium_data.sum() * 100)
            contracts_share = (contracts_data[largest_premium_segment] / contracts_data.sum() * 100)

            # =========================
            # Инсайт 2
            # Количество выплат
            # =========================

            largest_claim_count_segment = claim_count_data.idxmax()
            claim_count_share = (claim_count_data[largest_claim_count_segment] / claim_count_data.sum() * 100)

            # =========================
            # Инсайт 3
            # Количество выплат vs сумма выплат
            # =========================
            largest_claim_sum_segment = claim_sum_data.idxmax()
            claim_sum_share = (claim_sum_data[largest_claim_sum_segment] / claim_sum_data.sum() * 100)
            claim_frequency_share = (claim_count_data[largest_claim_sum_segment] / claim_count_data.sum() * 100)

            st.info(
                f"""
                **Инсайт (Сумма премий vs Количество договоров)**

                **В {year} году** ключевым драйвером рыночных сборов выступает сегмент
                **{largest_premium_segment}**,
                который генерирует **{premium_share:.1f}% совокупной выручки**,
                занимая при этом всего **{contracts_share:.1f}% от общего количества заключенных договоров**.

                Это подчеркивает высокую концентрацию капитала в данном виде страхования
                и его определяющее влияние на маржинальность всего сектора.
                """,
                icon="💡"
            )

            st.info(
                f"""
                **Инсайт (Количество выплат)**

                Основная операционная нагрузка по урегулированию убытков **в {year} году**
                сосредоточена в сегменте **{largest_claim_count_segment}**,
                на который приходится **{claim_count_share:.1f}% всех страховых случаев на рынке**.

                Столь высокая частота выплат требует от участников рынка максимальной
                автоматизации сервисов и цифровизации клиентского пути.
                """,
                icon="💡"
            )

            st.info(
                f"""
                **Инсайт (Количество выплат vs Сумма выплат)**

                Наибольшие финансовые риски для емкости рынка **в {year} году**
                представляет сегмент **{largest_claim_sum_segment}**.

                Обладая сравнительно низкой частотой страховых случаев
                **({claim_frequency_share:.1f}% от общего количества выплат)**,
                данный вид аккумулирует **{claim_sum_share:.1f}% всех денежных выплат на рынке**.

                Это указывает на высокую среднюю стоимость одного убытка и критическую
                важность перестраховочной защиты в данном направлении.
                """,
                icon="💡"
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

        df_share = (df_dyn.div(df_dyn.sum(axis=1), axis=0) * 100)
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

        st.plotly_chart(fig, width='stretch')

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
