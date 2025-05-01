import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="ESG Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/company_esg_financial_dataset.csv")
    df.fillna(method='ffill', inplace=True)
    return df

# Load the data
df = load_data()

st.title("🌍 ESG Performance Dashboard")
st.write("Analyze ESG and financial performance of global companies.")

# Sidebar filters
regions = df['Region'].unique()
industries = df['Industry'].unique()
years = sorted(df['Year'].unique())

region_filter = st.sidebar.multiselect("Select Region(s)", regions, default=regions)
industry_filter = st.sidebar.multiselect("Select Industry(s)", industries, default=industries)
year_filter = st.sidebar.slider("Select Year Range", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=(2015, 2021))

# Filtered Data
filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Industry'].isin(industry_filter)) &
    (df['Year'] >= year_filter[0]) &
    (df['Year'] <= year_filter[1])
]

# Summary Metrics
st.markdown("### 📈 Key ESG Metrics Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Avg ESG Score", f"{filtered_df['ESG_Overall'].mean():.1f}")
col2.metric("Carbon Emissions", f"{filtered_df['CarbonEmissions'].sum()/1e6:.2f}M Tons")
col3.metric("Market Cap", f"${filtered_df['MarketCap'].sum()/1e9:.2f}B")

# Show filtered table
st.subheader("Filtered ESG Data")
st.dataframe(filtered_df)

# ESG Score vs Revenue
st.subheader("💡 ESG Score vs Revenue")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered_df, x='ESG_Overall', y='Revenue', hue='Region', ax=ax1)
st.pyplot(fig1)

# ESG Score Trends
st.subheader("📈 ESG Score Trends Over Time")
fig2, ax2 = plt.subplots()
sns.lineplot(data=filtered_df, x='Year', y='ESG_Overall', hue='Region', ci=None, ax=ax2)
st.pyplot(fig2)

# ESG Score by Industry
st.subheader("🏭 ESG Score by Industry")
industry_avg = filtered_df.groupby("Industry")["ESG_Overall"].mean().sort_values(ascending=False)
st.bar_chart(industry_avg)

# ESG Distribution by Region
st.subheader("📍 ESG Distribution by Region")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x='Region', y='ESG_Overall')
st.pyplot(fig3)

# ESG Correlation Heatmap
st.subheader("🔍 ESG Correlation Matrix")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(filtered_df[[
    'ESG_Environmental', 'ESG_Social', 'ESG_Governance',
    'CarbonEmissions', 'WaterUsage', 'EnergyConsumption']].corr(),
    annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

# Download Filtered Data
st.download_button(
    label="📅 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_esg_data.csv',
    mime='text/csv'
)

# Insights Section
st.subheader("🧐 Insights & Recommendations")
st.markdown("""
- ✨ **Tech companies in North America** have high governance scores but lag in carbon neutrality.
- ⚡ **Energy sector in APAC** shows weak board diversity and high emissions.
- 🔹 Recommend improved renewable energy targets and board diversity policies.
""")
