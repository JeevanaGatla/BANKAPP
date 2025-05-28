from fastapi import FastAPI
import sqlite3


def connect_db():
    conn = sqlite3.connect("users.db")

    return conn

app = FastAPI()
connect_db()

@app.post("/user/create")
def create_bank_account(first_name: str, last_name: str, acc_no: str, ifsc: str, branch_name: str, balance: float = 0.0):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE acc_no = ?", (acc_no,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"error": "Account already exists"}

    
    cursor.execute(
        "INSERT INTO users (acc_no, ifsc, branch_name, first_name, last_name, balance) VALUES (?, ?, ?, ?, ?, ?)",
        (acc_no, ifsc, branch_name, first_name, last_name, balance)
    )
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Bank account created successfully",
        "account_id": account_id,
        "acc_no": acc_no,
        "balance": balance
    }

@app.post("/user/debit")
def debit(amt,acc_no):
    amt=float(amt)
    conn=connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE accno=?",(acc_no,))
    balance = cursor.fetchone()

    if balance[0]>=amt:
        bal=balance[0]-amt
        cursor.execute("UPDATE users SET balance=? WHERE accno=?",(bal,acc_no))
        conn.commit()
        conn.close()
        return {"current balance":bal}
    else:
        return {"message":"Insufficient balance"}
    
@app.post("/user/credit")
def credit(amt,acc_no):
    amt=float(amt)
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE accno=?",(acc_no,))
    balance=cursor.fetchone()
    curr_ba=balance[0]+amt
    cursor.execute("UPDATE users SET balance=? WHERE accno=?",(curr_ba,acc_no))
    conn.commit()
    conn.close()
    return {"current balance":curr_ba}


@app.get("/user/details")
def show_user(acc_no):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE accno=?",(acc_no,))
    data=cursor.fetchall()
    conn.close()
    return data
@app.get("/user/transfer")
def transfer(f_acc,to_acc,amt):
    
    debit(amt,f_acc)
    credit(amt,to_acc)
    return {"message":"Transfer successful"}















#if _name_ == "_main_":
 #   import uvicorn
  #  uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)