import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="COVID Vaccination Dashboard", layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("covid_vaccine_statewise.csv")
df = df.dropna(subset=["State"])
df["Date"] = pd.to_datetime(df["Updated On"], errors='coerce')

# Aggregations
total_dose1 = int(df["First Dose Administered"].sum())
total_dose2 = int(df["Second Dose Administered"].sum())
total_male = int(df["Male(Individuals Vaccinated)"].sum())
total_female = int(df["Female(Individuals Vaccinated)"].sum())

# --- Title
st.markdown('<div class="main-title">🇮🇳 COVID-19 Vaccination Dashboard</div>', unsafe_allow_html=True)

# --- Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-box">💉<br><b>1st Dose</b><br>{total_dose1:,}</div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-box">💉<br><b>2nd Dose</b><br>{total_dose2:,}</div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-box">👨<br><b>Males</b><br>{total_male:,}</div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-box">👩<br><b>Females</b><br>{total_female:,}</div>', unsafe_allow_html=True)

# --- Top States
st.subheader("🏆 Top 5 States by Vaccination")
dose1_top = df.groupby("State")["First Dose Administered"].sum().sort_values(ascending=False).head(5)
dose2_top = df.groupby("State")["Second Dose Administered"].sum().sort_values(ascending=False).head(5)

col1, col2 = st.columns(2)
col1.plotly_chart(px.bar(dose1_top, x=dose1_top.values, y=dose1_top.index, orientation='h', title="Top 5 - 1st Dose"))
col2.plotly_chart(px.bar(dose2_top, x=dose2_top.values, y=dose2_top.index, orientation='h', title="Top 5 - 2nd Dose"))

# --- Pie Chart
st.subheader("👥 Gender Distribution")
gender_df = pd.DataFrame({"Gender": ["Male", "Female"], "Count": [total_male, total_female]})
fig3 = px.pie(gender_df, names="Gender", values="Count", title="Gender-wise Vaccination")
st.plotly_chart(fig3, use_container_width=True)

# --- Time Series
st.subheader("📈 Vaccination Trend Over Time")
time_df = df.groupby("Date")[["First Dose Administered", "Second Dose Administered"]].sum().reset_index()
fig4 = px.line(time_df, x="Date", y=["First Dose Administered", "Second Dose Administered"], title="Dose Trend Over Time")
st.plotly_chart(fig4, use_container_width=True)

# --- Bubble Map Instead of Choropleth
st.subheader("🗺️ India State-wise Vaccination Map (1st Dose)")

# Coordinates of states
state_coords = {
    "Andhra Pradesh": [15.9129, 79.7400],
    "Arunachal Pradesh": [28.2180, 94.7278],
    "Assam": [26.2006, 92.9376],
    "Bihar": [25.0961, 85.3131],
    "Chhattisgarh": [21.2787, 81.8661],
    "Delhi": [28.7041, 77.1025],
    "Goa": [15.2993, 74.1240],
    "Gujarat": [22.2587, 71.1924],
    "Haryana": [29.0588, 76.0856],
    "Himachal Pradesh": [31.1048, 77.1734],
    "Jammu and Kashmir": [33.7782, 76.5762],
    "Jharkhand": [23.6102, 85.2799],
    "Karnataka": [15.3173, 75.7139],
    "Kerala": [10.8505, 76.2711],
    "Madhya Pradesh": [22.9734, 78.6569],
    "Maharashtra": [19.7515, 75.7139],
    "Manipur": [24.6637, 93.9063],
    "Meghalaya": [25.4670, 91.3662],
    "Mizoram": [23.1645, 92.9376],
    "Nagaland": [26.1584, 94.5624],
    "Odisha": [20.9517, 85.0985],
    "Punjab": [31.1471, 75.3412],
    "Rajasthan": [27.0238, 74.2179],
    "Sikkim": [27.5330, 88.5122],
    "Tamil Nadu": [11.1271, 78.6569],
    "Telangana": [18.1124, 79.0193],
    "Tripura": [23.9408, 91.9882],
    "Uttar Pradesh": [26.8467, 80.9462],
    "Uttarakhand": [30.0668, 79.0193],
    "West Bengal": [22.9868, 87.8550]
}

map_data = df.groupby("State")["First Dose Administered"].sum().reset_index()
map_data["Lat"] = map_data["State"].apply(lambda x: state_coords.get(x, [None, None])[0])
map_data["Lon"] = map_data["State"].apply(lambda x: state_coords.get(x, [None, None])[1])
map_data = map_data.dropna(subset=["Lat", "Lon"])

fig5 = px.scatter_mapbox(
    map_data,
    lat="Lat",
    lon="Lon",
    size="First Dose Administered",
    color="First Dose Administered",
    hover_name="State",
    color_continuous_scale="Viridis",
    zoom=4,
    height=600
)
fig5.update_layout(mapbox_style="carto-positron")
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig5, use_container_width=True)

# --- Explore Table
st.subheader("🔍 Explore State-wise Data")
selected_state = st.selectbox("Select a State", sorted(df["State"].unique()))
state_df = df[df["State"] == selected_state]
st.dataframe(state_df.tail(10))

# --- Footer
st.markdown("""<hr><div style='text-align:center;'>Made with ❤️ Latesh Patel | DSBDA Project</div>""", unsafe_allow_html=True)