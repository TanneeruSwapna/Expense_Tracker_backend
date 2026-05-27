from fastapi import FastAPI
import mysql.connector
import os
from dotenv import load_dotenv

# -----------------------------------
# LOAD ENV FILE
# -----------------------------------
load_dotenv()

# -----------------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
        ssl_disabled=False
    )

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Backend is running" }

# -----------------------------------
# ADD EXPENSE
# -----------------------------------
@app.post("/expenses")
def add_expense(expense: dict):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    INSERT INTO expenses(title, amount, category)
    VALUES(%s, %s, %s)
    """

    values = (
        expense["title"],
        expense["amount"],
        expense["category"]
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Expense Added Successfully"}


# -----------------------------------
# GET ALL EXPENSES
# -----------------------------------
@app.get("/expenses")
def get_expenses():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expenses ORDER BY expense_id ASC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"expenses": data}


# -----------------------------------
# UPDATE EXPENSE
# -----------------------------------
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: dict):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    UPDATE expenses
    SET title=%s, amount=%s, category=%s
    WHERE expense_id=%s
    """

    values = (
        expense["title"],
        expense["amount"],
        expense["category"],
        expense_id
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Expense Updated Successfully"}


# -----------------------------------
# DELETE EXPENSE
# -----------------------------------
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE expense_id=%s",
        (expense_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Expense Deleted Successfully"}


# -----------------------------------
# SEARCH EXPENSE
# -----------------------------------
@app.get("/search")
def search_expense(category: str):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM expenses WHERE category=%s",
        (category,)
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"expenses": data}


# -----------------------------------
# SORT EXPENSES
# -----------------------------------
@app.get("/sort")
def sort_expenses(sort_by: str):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if sort_by == "price_desc":
        query = "SELECT * FROM expenses ORDER BY amount DESC"

    elif sort_by == "price_asc":
        query = "SELECT * FROM expenses ORDER BY amount ASC"

    elif sort_by == "date_desc":
        query = "SELECT * FROM expenses ORDER BY expense_id DESC"

    else:
        query = "SELECT * FROM expenses ORDER BY expense_id ASC"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"expenses": data}