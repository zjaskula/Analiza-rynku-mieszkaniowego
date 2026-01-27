import sys
import time
import pandas as pd
import streamlit as st
import subprocess


st.set_page_config(
    page_title="Dashboard – oferty mieszkań",
    page_icon=":house:",
    layout="wide",
)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.markdown(
    "<h1 style='font-size: 50px; text-align: center; color: #052D73;'>Analiza ofert mieszkań na sprzedaż w Trójmieście</h1>",
    unsafe_allow_html=True)
st.markdown(" ")
st.header('Jak to działa?')
st.markdown("""Ta aplikacja pozwoli ci na szybkie podsumowanie ofert z wybranego miasta w Trójmieście i przedstawi kluczowe statystyki w postaci dashboardu. Wybierz miasto oraz ramy czasowe, i dowiedz się, czym charakteryzują 
się oferty mieszkań udostępniane w portalu [Otodom.pl](https://www.otodom.pl). Jeśli chcesz zobaczyć dane ze stycznia z 
całego Trójmiasta, wybierz :blue-background[checkbox].""")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

def base():
    st.header("Wybierz parametry")
    with st.form(key='filters'):
        show_all = st.checkbox("Pokaż dane z całego Trójmiasta (pełny miesiąc)")

        col_one, col_two = st.columns(2)
        choice = col_one.selectbox("Miasto", ["–", "Gdańsk", "Gdynia", "Sopot"])
        time_posted = col_two.selectbox(
            "Aktualność ofert", ["–", "Z ostatnich 24h", "Z ostatnich 3 dni", "Z ostatnich 7 dni"]
        )
        submitted = st.form_submit_button("🔍 Szukaj")

        if submitted and not show_all:
            if choice == "–" or time_posted == "–":
                st.warning("Musisz wybrać miasto i zakres czasu albo zaznaczyć opcję „Pokaż wszystko”.")
                return False

        if submitted and show_all:
            if choice != "–" or time_posted != "–":
                st.warning("Wybierz albo konkretne miasto i ramy czasowe, albo opcję „Pokaż wszystko”.")
                return False


    if submitted:
        st.session_state.submitted = True
        if show_all:
            st.session_state.df = pd.read_excel('data_january.xlsx')
        else:
            city = choice.lower()
            days_map = {
                "Z ostatnich 24h": "1",
                "Z ostatnich 3 dni": "3",
                "Z ostatnich 7 dni": "7"
            }
            days_since_created_str = days_map.get(time_posted, "")

            # wywołanie skryptów
            with st.spinner("Trwa pobieranie ofert..."):
                subprocess.call([sys.executable, "urls.py", city, days_since_created_str])
            with st.spinner("Trwa pobieranie szczegółów..."):
                subprocess.call([sys.executable, "webscraping.py"])
            with st.spinner("Trwa analiza danych..."):
                subprocess.call([sys.executable, "cleaning.py"])

            st.session_state.df = pd.read_excel('cleaned_data.xlsx')

    return submitted

def data():
    df = st.session_state.df
    dashboard, raw_data = st.tabs(['Dashboard', 'Dane'])

    with dashboard:
        with st.container(border=True):
            cols = st.columns(4, gap="medium")

            with cols[0]:
                st.metric(
                    "Liczba ogłoszeń",
                    f"{len(df):.0f}"
                )

            with cols[1]:
                st.metric(
                    "Mediana powierzchni",
                    f"{df['Powierzchnia'].median():.0f} m²"
                )

            with cols[2]:
                st.metric(
                    "Mediana cen",
                    f"{df['Cena'].median():.0f} zł",
                )

            with cols[3]:
                st.metric(
                    "Mediana cen za metr",
                    f"{df['Cena za metr'].median():.0f} zł/m²"
                )

        cols = st.columns(3, gap="medium")


    with raw_data:
        st.dataframe(df.style.format(thousands="", precision=0))

# wyświetlanie
base()
if st.session_state.submitted:
    data()