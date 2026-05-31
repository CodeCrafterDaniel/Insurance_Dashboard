import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Travel Insurance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Fake data ----------
np.random.seed(42)

countries = ['Turkey', 'Thailand', 'UAE', 'Egypt', 'Georgia', 'Russia']
insurance_types = [
    'Medical',
    'Trip Cancellation',
    'Baggage',
    'Accident'
]

n = 500

df = pd.DataFrame({
    'country': np.random.choice(countries, n),
    'insurance_type': np.random.choice(insurance_types, n),
    'price': np.random.randint(2000, 12000, n),
    'device': np.random.choice(['Mobile', 'Desktop'], n),
    'converted': np.random.choice([0, 1], n, p=[0.7, 0.3]),
    'date': pd.date_range('2025-01-01', periods=n, freq='D')
})

buyers = df[df.converted == 1]

conversion = df.converted.mean() * 100
buyers_count = len(buyers)
avg_check = buyers.price.mean()
revenue = buyers.price.sum()

# ---------- Sidebar ----------
st.sidebar.title("✈️ Insurance Dashboard")

country_filter = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries
)

device_filter = st.sidebar.multiselect(
    "Device",
    ['Mobile', 'Desktop'],
    default=['Mobile', 'Desktop']
)

filtered = df[
    df.country.isin(country_filter)
    & df.device.isin(device_filter)
    ]

buyers_filtered = filtered[filtered.converted == 1]

# ---------- Title ----------
st.title("Travel Insurance Analytics")

st.markdown(
    """
    Dashboard for travel insurance performance and funnel analysis.
    """
)

# ---------- KPI ----------
c1, c2, c3, c4 = st.columns(4)

conversion = filtered.converted.mean() * 100
buyers_count = len(buyers_filtered)
avg_check = buyers_filtered.price.mean()
revenue = buyers_filtered.price.sum()

c1.metric(
    "Conversion",
    f"{conversion:.2f}%",
    "+0.7%"
)

c2.metric(
    "Buyers",
    f"{buyers_count:,}",
    "+5%"
)

c3.metric(
    "Average Check",
    f"{avg_check:,.0f} ₽",
    "+3%"
)

c4.metric(
    "Total Revenue",
    f"{revenue:,.0f} ₽",
    "+12%"
)

st.divider()

# ---------- Funnel + Trend ----------
left, right = st.columns([1, 1])

with left:
    st.subheader("Sales Funnel")

    funnel = go.Figure(go.Funnel(
        y=[
            "Visitors",
            "Quotes",
            "Checkout",
            "Purchase"
        ],
        x=[10000, 4200, 2200, buyers_count]
    ))

    st.plotly_chart(
        funnel,
        use_container_width=True
    )

with right:
    st.subheader("Revenue Trend")

    ts = buyers_filtered.groupby(
        buyers_filtered.date.dt.month
    )['price'].sum().reset_index()

    fig = px.line(
        ts,
        x='date',
        y='price',
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs([
    "Conversion",
    "Revenue",
    "Geography"
])

with tab1:
    st.subheader("Conversion by Country")

    conv_country = filtered.groupby(
        'country'
    )['converted'].mean().reset_index()

    conv_country['converted'] *= 100

    fig = px.bar(
        conv_country,
        x='country',
        y='converted'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:
    st.subheader("Revenue by Insurance Type")

    rev = buyers_filtered.groupby(
        'insurance_type'
    )['price'].sum().reset_index()

    fig = px.pie(
        rev,
        values='price',
        names='insurance_type'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab3:
    st.subheader("Sales Geography")

    map_df = pd.DataFrame({
        'lat': [39, 15, 24, 26, 42, 55],
        'lon': [35, 101, 54, 30, 43, 37],
        'sales': np.random.randint(50, 500, 6)
    })

    st.map(map_df)

# ---------- Table ----------
st.subheader("Latest Purchases")

st.dataframe(
    buyers_filtered[
        ['country',
         'insurance_type',
         'price',
         'device']
    ].tail(10),
    use_container_width=True
)

# ---------- Insights ----------
st.subheader("Insights")

col1, col2 = st.columns(2)

with col1:
    st.error(
        """
        **Pain Point**

        Mobile conversion is lower than desktop.
        """
    )

    st.warning(
        """
        **Possible Reason**

        Checkout friction on mobile.
        """
    )

with col2:
    st.success(
        """
        **Recommendation**

        Simplify mobile checkout flow.
        """
    )

    st.info(
        """
        **Expected Effect**

        +10–15% conversion uplift.
        """
    )

# ---------- Expander ----------
with st.expander("Show raw data"):
    st.write(filtered)

# ---------- Download ----------
csv = filtered.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    "insurance_data.csv",
    "text/csv"
)