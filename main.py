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
st.subheader("🟦 Potwierdzone przypadki w czasie ")
fig, ax = plt.subplots()
ax.bar(country_df['Date'], country_df['Confirmed'], color='skyblue')
ax.set_xlabel('Data')
ax.set_ylabel('Potwierdzone przypadki')
ax.set_title(f'Liczba potwierdzonych przypadków - {selected_country}')
st.pyplot(fig)

# Plotly – wykres liniowy
st.subheader("Trendy - Potwierdzone, Zgony, Wyzdrowienia ")
fig2 = px.line(
    country_df,
    x='Date',
    y=['Confirmed', 'Deaths', 'Recovered'],
    labels={'value': 'Liczba przypadków', 'variable': 'Typ'},
    title=f'Trendy COVID-19 - {selected_country}'
)
st.plotly_chart(fig2)

# Mapa przypadków
st.subheader("🗺Mapa aktywnych przypadków ")
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

# Donut chart – rozkład przypadków w ostatnim dniu dla danego kraju
st.subheader("Rozkład przypadków COVID-19 (ostatni dzień, donut)")

latest_country = country_df[country_df['Date'] == country_df['Date'].max()]
if not latest_country.empty:
    values = latest_country[['Active', 'Deaths', 'Recovered']].values[0]
    labels = ['Aktywne', 'Zgony', 'Wyzdrowienia']

    fig4 = px.pie(
        names=labels,
        values=values,
        title=f'Struktura przypadków COVID-19 ({selected_country}) - {country_df["Date"].max().date()}',
        hole=0.4  # tworzy donut
    )
    st.plotly_chart(fig4)
else:
    st.info("Brak danych z ostatniego dnia dla tego kraju.")

# Top 10 krajów z największą liczbą aktywnych przypadków
st.subheader("Top 10 krajów z największą liczbą aktywnych przypadków (ostatni dzień)")

top10 = (
    df[df['Date'] == df['Date'].max()]
    .groupby('Country/Region')['Active']
    .sum()
    .nlargest(10)
    .reset_index()
)

fig5 = px.bar(
    top10,
    x='Country/Region',
    y='Active',
    title='Top 10 krajów z największą liczbą aktywnych przypadków',
    color='Active',
    color_continuous_scale='Reds'
)
st.plotly_chart(fig5)

