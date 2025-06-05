import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Wczytaj dane
df = pd.read_csv('covid_19_clean_complete.csv', parse_dates=['Date'])

# Sidebar - wybór kraju
st.sidebar.title("Filtr")
countries = df['Country/Region'].unique()
selected_country = st.sidebar.selectbox("Wybierz kraj", sorted(countries))

# Filtruj dane
country_df = df[df['Country/Region'] == selected_country].sort_values('Date')

# Tytuł
st.title(f'Dashboard COVID-19: {selected_country}')

# Matplotlib – wykres potwierdzonych przypadków
st.subheader("🟦 Potwierdzone przypadki w czasie (Matplotlib)")
fig, ax = plt.subplots()
ax.bar(country_df['Date'], country_df['Confirmed'], color='skyblue')
ax.set_xlabel('Data')
ax.set_ylabel('Potwierdzone przypadki')
ax.set_title(f'Liczba potwierdzonych przypadków - {selected_country}')
st.pyplot(fig)

# Plotly – wykres liniowy
st.subheader("📈 Trendy - Potwierdzone, Zgony, Wyzdrowienia (Plotly)")
fig2 = px.line(
    country_df,
    x='Date',
    y=['Confirmed', 'Deaths', 'Recovered'],
    labels={'value': 'Liczba przypadków', 'variable': 'Typ'},
    title=f'Trendy COVID-19 - {selected_country}'
)
st.plotly_chart(fig2)

# Mapa przypadków
st.subheader("🗺️ Mapa aktywnych przypadków (Plotly)")
latest = df[df['Date'] == df['Date'].max()]
fig3 = px.scatter_geo(
    latest,
    lat='Lat',
    lon='Long',
    size='Active',
    color='Country/Region',
    hover_name='Province/State',
    title='Aktywne przypadki COVID-19 (najnowszy dzień)'
)
st.plotly_chart(fig3)
