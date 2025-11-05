import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="telegram_bot",
        password="",
        database=''
    )

def client_id(client_number):
   cnx = get_connection()
   query = ("SELECT id FROM clients "
            "WHERE tel_number = %s")
   cur = cnx.cursor()
   cur.execute(query, (client_number,))
   result = cur.fetchone()
   client_id = result[0]
   cur.close()
   cnx.close()
   return client_id

def client_profile(client_id):
   cnx = get_connection()
   query = ("SELECT first_name, last_name, tel_number, email FROM clients "
            "WHERE id = %s")
   cur = cnx.cursor()
   cur.execute(query, (client_id,))
   results = cur.fetchone()
   cur.close()
   cnx.close()
   return results

def orders_list(client_id):   
    cnx = get_connection()
    query = ("SELECT id, date, status FROM orders "
            "WHERE client_id = %s ")
    cur = cnx.cursor()
    cur.execute(query, (client_id,))
    results = cur.fetchall()
    cur.close()
    cnx.close()
    return results

def order_items(order_id):   
    cnx = get_connection()
    q_items = ("SELECT product_id, quantity FROM order_items "
            "WHERE order_id = %s ")
    cur = cnx.cursor()
    cur.execute(q_items, (order_id,))
    items = cur.fetchall()
    o_items = []
    for item in items:
        product_id, quantity = item
        q_product = ("SELECT name, price FROM products "
            "WHERE id = %s ")
        cur = cnx.cursor()
        cur.execute(q_product, (product_id,))
        product = cur.fetchone()
        if product:
            name, price = product
            o_items.append((name, price, quantity))
        cur.close()
    cur.close()
    cnx.close()
    return o_items

def client_by_order(order_id):
    cnx = get_connection()
    q_items = ("SELECT client_id FROM orders "
            "WHERE id = %s ")
    cur = cnx.cursor()
    cur.execute(q_items, (order_id,))
    result = cur.fetchone()
    cur.close()
    cnx.close()
    return result

def create_client(first_name, last_name, tel_number,email):
    cnx = get_connection()
    cur = cnx.cursor()
    query = """
        INSERT INTO clients (first_name, last_name, tel_number, email)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(query, (
        first_name,
        last_name if last_name else "",
        tel_number if tel_number else "",
        email if email else ""
    ))

    cnx.commit()
    cur.close()
    cnx.close()

def delete_client(client_id):
    
    cnx = get_connection()
    cur = cnx.cursor()
    query = """
        DELETE FROM clients WHERE id = %s
    """
    cur.execute(query, (client_id,))
    cnx.commit()
    cur.close()
    cnx.close()

def update_client(client_id, first_name, last_name, tel_number, email):
    cnx = get_connection()
    cur = cnx.cursor()
    query = """
        UPDATE clients
        SET first_name=%s, last_name=%s, tel_number=%s, email=%s
        WHERE id=%s
    """
    cur.execute(query, (first_name, last_name, tel_number, email, client_id))
    cnx.commit()
    cur.close()
    cnx.close()
