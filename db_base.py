import psycopg2

from psycopg2 import sql


def connect_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )


def save_links_db(url, query_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        insert_query = sql.SQL("INSERT INTO public.links (url, query_id) VALUES (%s, %s)")
        cursor.execute(insert_query, (url, query_id))
        conn.commit()
        print("URL saved successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while saving URL:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def get_links_from_db(query_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        select_query = "SELECT * FROM public.links WHERE (query_id) = (%s)"
        cursor.execute(select_query, (query_id,))
        links = cursor.fetchall()
        return links
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while retrieving links:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def save_query_db(query_name, url=None):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        if url:
            insert_query = sql.SQL("INSERT INTO public.queries (query, url) VALUES (%s, %s)")
            cursor.execute(insert_query, (query_name, url,))
        else:
            insert_query = sql.SQL("INSERT INTO public.queries (query) VALUES (%s)")
            cursor.execute(insert_query, (query_name,))
        conn.commit()
        print("Query saved successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while saving URL:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def change_query_bool_db(query_url):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        update_query = sql.SQL("UPDATE public.queries SET is_shop = %s WHERE url = %s")
        cursor.execute(update_query, (True, query_url))
        conn.commit()
        print("Query updated successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while updating query:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def get_query_db():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        select_query = "SELECT * FROM public.queries"
        cursor.execute(select_query)
        links = cursor.fetchall()
        return links
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while retrieving query:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def delete_query_from_db(id):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        delete_query = "DELETE FROM public.queries WHERE id = %s"
        cursor.execute(delete_query, (id,))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while deleting query:", error)
        if conn is not None:
            conn.rollback()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def save_google_sheet_db(sheet_name, sheet_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        insert_query = sql.SQL("INSERT INTO public.google_sheets (sheet_id, sheet_name) VALUES (%s, %s)")
        cursor.execute(insert_query, (sheet_id, sheet_name,))
        conn.commit()
        print("Query saved successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while saving URL:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def get_google_sheet_names_db():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        select_query = "SELECT sheet_name FROM public.google_sheets"
        cursor.execute(select_query)
        sheets = cursor.fetchall()
        return [sheet[0] for sheet in sheets]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while retrieving query:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def get_google_sheet_db(sheet_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        select_query = "SELECT sheet_id FROM public.google_sheets WHERE sheet_name = %s"
        cursor.execute(select_query, (sheet_name,))
        sheets = cursor.fetchall()
        return [sheet[0] for sheet in sheets]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while retrieving query:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
