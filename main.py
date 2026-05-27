from fastapi import FastAPI
import mysql.connector
import os
from dotenv import load_dotenv

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

app = FastAPI()

def get_cursor():
    conn = get_db_connection()
    return conn, conn.cursor(dictionary = True)

# -----------------------------------
# FASTAPI APP
# -----------------------------------

app = FastAPI()

# -----------------------------------
# ADD EXPENSE
# -----------------------------------

@app.post("/expenses")
def add_expense(expense: dict):

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

    return {"message": "Expense Added Successfully"}

# -----------------------------------
# GET ALL EXPENSES
# -----------------------------------

@app.get("/expenses")
def get_expenses():

    cursor.execute("SELECT * FROM expenses ORDER BY expense_id ASC")
    return {"expenses": cursor.fetchall()}

# -----------------------------------
# UPDATE EXPENSE
# -----------------------------------

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: dict):

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

    return {"message": "Expense Updated Successfully"}

# -----------------------------------
# DELETE EXPENSE
# -----------------------------------

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    cursor.execute("DELETE FROM expenses WHERE expense_id=%s", (expense_id,))
    conn.commit()

    return {"message": "Expense Deleted Successfully"}

# -----------------------------------
# SEARCH EXPENSE (BY CATEGORY)
# -----------------------------------

@app.get("/search")
def search_expense(category: str):

    cursor.execute(
        "SELECT * FROM expenses WHERE category=%s",
        (category,)
    )

    return {"expenses": cursor.fetchall()}

# -----------------------------------
# SORT EXPENSES
# -----------------------------------

@app.get("/sort")
def sort_expenses(sort_by: str):

    if sort_by == "price_desc":
        query = "SELECT * FROM expenses ORDER BY amount DESC"

    elif sort_by == "price_asc":
        query = "SELECT * FROM expenses ORDER BY amount ASC"

    elif sort_by == "date_desc":
        query = "SELECT * FROM expenses ORDER BY expense_id DESC"

    else:
        query = "SELECT * FROM expenses ORDER BY expense_id ASC"

    cursor.execute(query)

    return {"expenses": cursor.fetchall()}