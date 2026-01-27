import sys
import time
import pandas as pd
import streamlit as st
import subprocess
import plotly.express as px


st.set_page_config(
    page_title="Dashboard – oferty mieszkań",
    page_icon=":house:",
    layout="wide",)

st.markdown('''<style>header {visibility: hidden;}</style>''', unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 50px; text-align: center; color: #052D73;'>Analiza ofert mieszkań na sprzedaż w Trójmieście</h1>",
    unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; font-size:20px;'>Szybki przegląd ofert mieszkań w Trójmieście z kluczowymi "
    "statystykami i interaktywnymi wykresami.</p>",
    unsafe_allow_html=True)

st.markdown(
    "<hr style='border:1px solid #D3D3D3; margin:20px 0;'>",
    unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.header("Jak to działa?")
st.markdown("""Aplikacja umożliwia analizę ofert mieszkań w Trójmieście z portalu [Otodom.pl](https://www.otodom.pl), 
zarówno dla danych z całego stycznia, jak i dla ofert pozyskanych na bieżąco. 
Możesz wybrać miasto i zakres czasowy ofert i analizować bieżące oferty lub wyświetlić dane z całego Trójmiasta dla 
stycznia 2026 (zaznacz :blue-background[checkbox]).  
  
Wszystkie statystyki są prezentowane w formie interaktywnych wykresów i podsumowań, pozwalając szybko zorientować się 
w strukturze rynku mieszkań.""")

if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "mode" not in st.session_state:
    st.session_state.mode = None

st.markdown("<br>", unsafe_allow_html=True)

def base():
    st.header("Wybierz parametry")
    with st.form(key='filters'):
        show_all = st.checkbox("Pokaż dane z całego Trójmiasta (styczeń 2026)")

        col_one, col_two = st.columns(2)
        choice = col_one.selectbox("Miasto", ["–", "Gdańsk", "Gdynia", "Sopot"])
        time_posted = col_two.selectbox(
            "Aktualność ofert", ["–", "Z ostatnich 24h", "Z ostatnich 3 dni", "Z ostatnich 7 dni"]
        )
        submitted = st.form_submit_button("🔍 Szukaj")

        if submitted and not show_all:
            if choice == "–" or time_posted == "–":
                st.warning("Musisz wybrać miasto i zakres czasu albo zaznaczyć checkbox.")
                return False

        if submitted and show_all:
            if choice != "–" or time_posted != "–":
                st.warning("Wybierz albo konkretne miasto i ramy czasowe, albo zaznaczyć checkbox.")
                return False


    if submitted:
        if show_all:
            st.session_state.submitted = True
            st.session_state.df = pd.read_excel('data_january.xlsx')
            st.session_state.mode = 1
        else:
            st.session_state.mode = 2
            choice2 = choice
            if choice == 'Gdańsk':
                choice2 = 'Gdansk'
            city = choice2.lower()
            days_map = {
                "Z ostatnich 24h": "1",
                "Z ostatnich 3 dni": "3",
                "Z ostatnich 7 dni": "7"
            }
            days_since_created_str = days_map.get(time_posted, "")

            # wywołanie skryptów
            with st.spinner("Trwa pobieranie ofert..."):
                wynik = subprocess.call([sys.executable, "urls.py", city, days_since_created_str])
                if wynik != 0:
                    st.warning("Proces został przerwany. Wyszukaj ponownie.")
                    return False
            with st.spinner("Trwa pobieranie szczegółów..."):
                wynik = subprocess.call([sys.executable, "webscraping.py"])
                if wynik != 0:
                    st.warning("Proces został przerwany. Wyszukaj ponownie.")
                    return False
            with st.spinner("Trwa analiza danych..."):
                wynik = subprocess.call([sys.executable, "cleaning.py", choice])
                if wynik != 0:
                    st.warning("Proces został przerwany. Wyszukaj ponownie.")
                    return False

            st.session_state.df = pd.read_excel('cleaned_data.xlsx')
            st.session_state.submitted = True

    return submitted


def data():
    mode = st.session_state.mode
    df = st.session_state.df
    dashboard, raw_data = st.tabs(['Dashboard', 'Dane'])

    with dashboard:
        with st.container(border=True):
            cols = st.columns(4, gap="medium")

            with cols[0]:
                st.metric("Liczba ogłoszeń", f"{len(df):.0f}")

            with cols[1]:
                st.metric("Mediana powierzchni", f"{df['Powierzchnia'].median():.0f} m²")

            with cols[2]:
                st.metric("Mediana cen", f"{df['Cena'].median():.0f} zł",)

            with cols[3]:
                st.metric("Mediana cen za metr", f"{df['Cena za metr'].median():.0f} zł/m²")

        # wykres 1: histogram
        def add_metraz(df: pd.DataFrame) -> pd.DataFrame:
            bins = [0, 30, 60, 90, float("inf")]
            labels = ["<30", "30–60", "60–90", ">90"]
            df["Metraż"] = pd.cut(df["Powierzchnia"], bins=bins, labels=labels, right=True)
            return df

        def top_dzielnice(df: pd.DataFrame, n=3):
            agg = (df.groupby("Dzielnica")['Cena za metr'].median().dropna().sort_values())
            cheapest = agg.head(n)
            expensive = agg.tail(n)
            result = pd.concat([cheapest, expensive]).reset_index()
            result["Segment"] = ["Najtańsze"] * len(cheapest) + ["Najdroższe"] * len(expensive)
            return result

        df_work = df.copy()
        color_map = {
            "Sopot": "#A0DCFA",
            "Gdynia": "#0041D0",
            "Gdańsk": "#052D73"}

        with st.container(border=True):
            if mode == 1:
                miasta = sorted(df_work["Miasto"].dropna().unique())
                selected_cities = st.multiselect("Wybierz miasta do porównania", options=miasta, default=miasta)
                if not selected_cities:
                    st.warning("Musisz wybrać przynajmniej jedno miasto.")
                df_filtered = df_work[df_work["Miasto"].isin(selected_cities)]
                color_arg = "Miasto"
            else:
                miasta = df_work["Miasto"].dropna().unique()
                selected_city = st.radio("Miasto", options=miasta)
                df_filtered = df_work[df_work["Miasto"] == selected_city]
                color_arg = None

        cols = st.columns(2, gap="medium")
        with cols[0].container(border=True):
            st.subheader("Rozkład cen za m²")

            fig_hist = px.histogram(
                df_filtered,
                x="Cena za metr",
                color=color_arg,
                color_discrete_map=color_map,
                nbins=40,
                labels={"Cena za metr": "Cena za m²"})

            fig_hist.update_layout(bargap=0.05, yaxis_title="Częstość")

            st.plotly_chart(fig_hist, use_container_width=True)

        # wykres 2: mediana cen vs metraż
        with cols[1].container(border=True):
            st.subheader("Mediana ceny za m² wg metrażu")

            df_bins = add_metraz(df_filtered)

            group_cols = ["Metraż"]
            if mode == 1:
                group_cols.append("Miasto")

            df_med = (df_bins.groupby(group_cols)["Cena za metr"].median().reset_index())

            fig_med = px.bar(
                df_med,
                x="Metraż",
                y="Cena za metr",
                color="Miasto" if mode == 1 else None,
                color_discrete_map=color_map,
                barmode="group",
                labels={"Cena za metr": "Mediana ceny za m²"})
            st.plotly_chart(fig_med, use_container_width=True)

        # wykres 3: top 3 dzielnice
        with cols[0].container(border=True):
            st.subheader("Top 3 najtańsze i najdroższe dzielnice")
            unique_districts = df_filtered["Dzielnica"].dropna().unique()

            if len(unique_districts) < 6:
                st.warning("Niewystarczająca ilość informacji do wyświetlenia wykresu.")
            else:
                median_price = df_filtered["Cena za metr"].median()
                df_top = top_dzielnice(df_filtered, n=3)
                df_top["Różnica"] = df_top["Cena za metr"] - median_price

                fig_top = px.bar(
                    df_top,
                    x="Różnica",
                    y="Dzielnica",
                    color="Segment",
                    orientation="h",
                    labels={
                        "Różnica": "Odchylenie od mediany cen za m² [zł]",
                        "Dzielnica": "Dzielnica"
                    },
                    color_discrete_map={"Najtańsze": "#38663D", "Najdroższe": "#D60A26"})

                fig_top.update_layout(
                    xaxis_title="Odchylenie od mediany cen za m²",
                    shapes=[{
                        "type": "line",
                        "x0": 0,
                        "x1": 0,
                        "y0": -0.5,
                        "y1": len(df_top) - 0.5,
                        "line": {"color": "black", "width": 0.75}
                    }],
                    bargap=0.3
                )

                # wyświetlenie
                st.caption(f"W wybranych ofertach mediana cen za m² wynosi: {median_price: .0f} zł")
                st.plotly_chart(fig_top, use_container_width=True)

        # wykres 4: liczba ofert wg liczby pokoi
        with cols[1].container(border=True):
            st.subheader("Liczba ofert wg liczby pokoi")
            if mode == 1:
                rooms_count = (df_filtered.groupby(["Liczba pokoi", "Miasto"])["ID"].count().reset_index(name="Liczba ofert"))

                fig_rooms = px.bar(
                    rooms_count,
                    x="Liczba pokoi",
                    y="Liczba ofert",
                    color="Miasto",
                    color_discrete_map=color_map)
                fig_rooms.update_layout(barmode="stack")

            else:
                rooms_count = (df_filtered.groupby("Liczba pokoi")["ID"].count().reset_index(name="Liczba ofert"))

                fig_rooms = px.bar(
                    rooms_count,
                    x="Liczba pokoi",
                    y="Liczba ofert",
                    color_discrete_sequence=["#0041D0"])

            st.plotly_chart(fig_rooms, use_container_width=True)

        # wykres 5: cena wg piętra
        with cols[0].container(border=True):
            st.subheader("Cena za m² wg piętra")
            if mode == 1:
                floor_price = (df_filtered.dropna(subset=["Piętro", "Cena za metr"]).groupby(["Piętro", "Miasto"])["Cena za metr"].median().reset_index())
                fig_floor = px.bar(
                    floor_price,
                    x="Piętro",
                    y="Cena za metr",
                    color="Miasto",
                    labels={"Cena za metr": "Mediana ceny za m²"},
                    color_discrete_map=color_map
                )
                fig_floor.update_layout(barmode="group", xaxis=dict(tickmode="linear", dtick=1))
            else:
                floor_price = (
                    df_filtered.dropna(subset=["Piętro", "Cena za metr"])
                    .groupby("Piętro")["Cena za metr"]
                    .median()
                    .reset_index()
                )
                fig_floor = px.bar(
                    floor_price,
                    x="Piętro",
                    y="Cena za metr",
                    labels={"Cena za metr": "Mediana ceny za m²"},
                    color_discrete_sequence=["#0041D0"]
                )
                fig_floor.update_layout(xaxis=dict(tickmode="linear", dtick=1))

            st.plotly_chart(fig_floor, use_container_width=True)

        # wykres 6: odsetek mieszkań wg roku budowy – pie plot
        with cols[1].container(border=True):
            st.subheader("Odsetek mieszkań wg roku budowy")

            def add_rok_budowy_bin(df: pd.DataFrame) -> pd.DataFrame:
                labels = ["<1945", "1945–1970", "1971–1990", "1991–2010", ">2010"]
                df = df.copy()
                df["Rok budowy (przedziały)"] = pd.cut(
                    df["Rok budowy"],
                    bins=[0, 1945, 1970, 1990, 2010, float("inf")],
                    labels=labels
                )
                df["Rok budowy (przedziały)"] = pd.Categorical(
                    df["Rok budowy (przedziały)"],
                    categories=labels,
                    ordered=True
                )
                return df

            df_year_bins = add_rok_budowy_bin(df_filtered)
            year_counts = df_year_bins["Rok budowy (przedziały)"].value_counts().reindex(
                ["<1945", "1945–1970", "1971–1990", "1991–2010", ">2010"]).reset_index()
            year_counts.columns = ["Rok budowy", "Liczba ofert"]

            fig_year = px.pie(
                year_counts,
                names="Rok budowy",
                values="Liczba ofert",
                color_discrete_sequence= ["#A0DCFA", "#6096E0", "#1560C0", "#053A7A", "#052D73"],
                hole=0.3
            )
            fig_year.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_year, use_container_width=True)

        # wykres 7: boxplot cen mieszkań wg typu ogłoszeniodawcy
        with cols[0].container(border=True):
            st.subheader("Cena za m² wg typu ogłoszeniodawcy")

            df_filtered_box = df_filtered.dropna(subset=["Typ ogłoszeniodawcy", "Cena za metr"])
            fig_owner = px.box(
                df_filtered_box,
                x="Typ ogłoszeniodawcy",
                y="Cena za metr",
                labels={"Cena za metr": "Cena za m²"},
                color="Typ ogłoszeniodawcy",
                color_discrete_sequence=["#6096E0", "#053A7A"]
            )
            st.plotly_chart(fig_owner, use_container_width=True)

        # wykres 8: mediana ceny wg miasta i rynku
        with cols[1].container(border=True):
            st.subheader("Mediana ceny za m² wg miasta i rynku")

            df_grouped = (df_filtered.dropna(subset=["Miasto", "Rynek", "Cena za metr"]).groupby(["Miasto", "Rynek"])["Cena za metr"].mean().reset_index())

            fig_market = px.bar(
                df_grouped,
                x="Miasto",
                y="Cena za metr",
                color="Rynek",
                barmode="group",
                labels={"Cena za metr": "Mediana ceny za m²"},
                color_discrete_sequence=["#6096E0", "#053A7A"])

            st.plotly_chart(fig_market, use_container_width=True)

        # wykres 9: dodatki
        with cols[0].container(border=True):
            st.subheader("Odsetek mieszkań z wybranymi udogodnieniami")

            amenities = [
                ("Balkon", "Balkon"),
                ("Garaz/miejsce parkingowe", "Miejsce parkingowe"),
                ("Winda", "Winda"),
                ("Ogrodek", "Ogródek"),
                ("Oddzielna kuchnia", "Oddzielna kuchnia"),
                ("Piwnica/komorka", "Piwnica/komórka")]

            for i in range(0, len(amenities), 3):
                cols_amenities = st.columns(3, gap="small")
                for j, (col_name, label) in enumerate(amenities[i:i + 3]):
                    with cols_amenities[j]:
                        percent = (df_filtered[col_name] == 1).mean() * 100
                        st.metric(label=f"{label}", value=f"{percent:.0f} %")

        # wykres 10: stan wykończenia
        with cols[1].container(border=True):
            st.subheader("Stan wykończenia mieszkań")
            finish_counts = df_filtered['Stan wykończenia'].value_counts().reset_index()
            finish_counts.columns = ['Stan wykończenia', 'Liczba ofert']

            fig_finish = px.pie(
                finish_counts,
                names='Stan wykończenia',
                values='Liczba ofert',
                color_discrete_sequence= ["#A0DCFA","#0041D0","#052D73"],
                hole=0.3)
            fig_finish.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_finish, use_container_width=True)

    with raw_data:
        st.dataframe(df.style.format(thousands="", precision=0))

# wyświetlanie
base()
if st.session_state.submitted:
    data()