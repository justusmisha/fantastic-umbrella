import asyncio
import time
import pandas as pd
import streamlit as st

from card_parser import browser_parser
from conf import TOKEN, valid_credentials
from db_base import *
from excel_downloader import *
from links_parser import parse_links_by_query, get_name_profile
from main import main


def authenticate(username, password):
    return username in valid_credentials and valid_credentials[username] == password


async def home():
    st.title("Авито Парсер")
    queries = get_query_db()
    cities_data = pd.read_csv('cities.csv', header=None, names=['Russian', 'English'])

    for query in queries:
        if not query[2]:
            col1, col2, col3, col4 = st.columns([4, 3, 2, 2])

            with col1:
                st.write(query[1])
                pages = st.number_input('Страницы', min_value=1, step=1, value=1, format='%d', key=f"make_query_{query[1]}")
            with col2:
                selected_city_russian = st.selectbox('Выберите город:', cities_data['Russian'], key=f"select_city_{query[1]}")
                city_translation_map = dict(zip(cities_data['Russian'], cities_data['English']))
                selected_city_english = city_translation_map[selected_city_russian].replace(" ", "_").lower()
                google_sheet_name = st.selectbox('Выберите гугл документ:', get_google_sheet_names_db(), key=f"select_sheet_{query[1]}")
            with col3:
                if st.button(f"Произвести поиск", key=f"make_query_{query[0]}"):
                    start = time.time()
                    google_sheet = get_google_sheet_db(google_sheet_name)
                    google_sheet = ''.join(google_sheet)
                    parse_links_by_query(token=TOKEN, query_str=query[1], query_id=query[0], page_numbers=pages, city=selected_city_english)
                    create_new_sheet(query[1], google_sheet)
                    main(query[1], google_sheet, query_id=query[0])
                    end = time.time()
                    length = end - start
                    st.success(f"Поиск по '{query[1]}' завершен за {length:.2f} секунд!")
            with col4:
                if st.button(f"Удалить запрос", key=f"delete_{query[0]}"):
                    delete_query_from_db(query[0])
                    st.success(f"Запрос '{query[1]}' удален успешно.")

    name = st.text_input('Введите ваш запрос для парсинга или ссылку на объявление').strip()
    if st.button("Сохранить"):
        if name:
            save_query_db(name)
            st.success("Запрос Сохранен!")
        else:
            st.warning("Запрос должен быть не пустым!")


async def one_link():
    st.title("Парсер по ссылке")
    url = st.text_input('Введите ссылку на объявление').strip()
    google_sheet_name = st.selectbox('Выберите гугл документ:', get_google_sheet_names_db())

    if st.button("Произвести поиск"):
        if url:
            try:
                start = time.time()
                google_sheet = get_google_sheet_db(google_sheet_name)
                google_sheet = ''.join(google_sheet)
                create_new_sheet('Одиночный запрос', google_sheet, clear=False)
                main('Одиночный запрос', google_sheet, link=url)
                end = time.time()
                length = end - start
                st.success(f"Поиск по {url} завершен за {length:.2f} секунд!")
            except Exception as e:
                st.warning(f"Что-то пошло не так: {e}")
        else:
            st.warning("Запрос должен быть не пустым!")


async def google_sheets():
    st.title("Гугл документы")
    sheet_name = st.text_input('Введите название гугл документа').strip()

    if st.button('Создать'):
        if sheet_name:
            try:
                if sheet_name not in get_google_sheet_names_db():
                    sheet_id = create_google_sheet(sheet_name)
                    st.success(f'Гугл документ успешно создан. ID: {sheet_id}')
                    save_google_sheet_db(sheet_name, sheet_id)
                else:
                    st.warning('Документ с таким названием уже существует!')
            except Exception as e:
                st.error(f'Error: {e}')
        else:
            st.warning('Введите название!')
    a = get_google_sheet_names_db()
    if a:
        google_sheet_name = st.selectbox('Выберите чтобы перейти:', a)
        google_sheet = ''.join(get_google_sheet_db(google_sheet_name))
        google_sheet_url = f'https://docs.google.com/spreadsheets/d/{google_sheet}/edit?usp=sharing'

        if st.button("Открыть"):
            st.success(google_sheet_url)


def profile_home():
    st.title("Парсинг продавца")
    queries = get_query_db()
    link_for_parsing = st.text_input('Введите ссылку на продавца').strip()

    if st.button("Добавить продавца"):
        name = get_name_profile(browser_parser(link_for_parsing))
        save_query_db(name, url=link_for_parsing)
        change_query_bool_db(link_for_parsing)

    for query in queries:
        links = get_links_from_db(query[0])
        for link in links:
            if link[2]:
                column1, column2, column3 = st.columns([4, 2, 2])

                with column1:
                    st.write(query[1])
                    pages = st.number_input('Страницы', min_value=1, step=1, value=1, format='%d', key=f"make_query_{query[1]}")
                    google_sheet_name = st.selectbox('Выберите гугл документ:', get_google_sheet_names_db(), key=f"select_sheet_{query[1]}")
                with column2:
                    if st.button(f"Произвести поиск", key=f"make_query_{query[0]}"):
                        start = time.time()
                        print(1)
                        google_sheet = get_google_sheet_db(google_sheet_name)
                        print(2)
                        google_sheet = ''.join(google_sheet)
                        print(3)
                        parse_links_by_query(token=TOKEN, query_str=query[1], query_id=query[0], page_numbers=pages)
                        print(4)
                        create_new_sheet(query[1], google_sheet)
                        print(5)
                        main(query[1], google_sheet, query_id=query[0])
                        print(6)
                        end = time.time()
                        print(7)
                        length = end - start
                        st.success(f"Поиск по '{query[1]}' завершен за {length:.2f} секунд!")
                with column3:
                    if st.button(f"Удалить запрос", key=f"delete_{query[0]}"):
                        delete_query_from_db(query[0])
                        st.success(f"Запрос '{query[1]}' удален успешно.")


async def contacts():
    st.title("Контакты")
    st.write("Почта для контактов: yustus.misha10@gmail.com")
    st.write("Тг: [https://t.me/justusmisha](https://t.me/justusmisha)")
    st.write("GitHub: [https://github.com/justusmisha](https://github.com/justusmisha)")


async def main_page():
    nav_items = {
        "Авито Парсер": home,
        "Гугл документы": google_sheets,
        "Парсинг Продавца": profile_home,
        "Парсинг одной ссылки": one_link,
        "Контакты": contacts,
    }

    selected_item = st.sidebar.radio("Navigation", list(nav_items.keys()))
    await nav_items[selected_item]()


if __name__ == "__main__":
    st.set_page_config(page_title="Парсер", layout="wide")

    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    if not st.session_state.is_logged_in:
        username = st.sidebar.text_input("Никнейм")
        password = st.sidebar.text_input("Пароль", type="password")
        login_button = st.sidebar.button("Зайти")

        if login_button:
            if authenticate(username, password):
                st.session_state.is_logged_in = True
                st.success("Вы вошли в систему!")
            else:
                st.error("Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.")
    if st.session_state.is_logged_in:
        main_page()
        