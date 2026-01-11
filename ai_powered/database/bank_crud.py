from database.db import get_conn
import random
from database.security import hash_password


# ---------------- USER ----------------
def create_user(username, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hash_password(password))
    )

    conn.commit()
    conn.close()



def get_user(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE username=?",
        (username,)
    )

    user = cur.fetchone()
    conn.close()
    return user


# ---------------- ACCOUNT ----------------
def create_account(user_id, acc_no, acc_type, balance, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO accounts VALUES (?, ?, ?, ?, ?)
    """, (acc_no, user_id, acc_type, balance, password))

    card_no = "4000" + str(random.randint(100000000000, 999999999999))
    cur.execute("""
        INSERT INTO cards VALUES (NULL, ?, ?, 'ACTIVE')
    """, (acc_no, card_no))

    conn.commit()
    conn.close()

def check_balance(acc_no):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
    res = cur.fetchone()
    conn.close()
    return res[0] if res else None

def card_details(acc_no):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT card_number, status FROM cards WHERE account_number=?", (acc_no,))
    res = cur.fetchall()
    conn.close()
    return res

def transfer_money(sender, receiver, amount, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT balance, password FROM accounts WHERE account_number=?", (sender,))
    sender_data = cur.fetchone()

    if not sender_data:
        return "❌ Sender account not found"
    if sender_data[1] != password:
        return "❌ Wrong password"
    if sender_data[0] < amount:
        return "❌ Insufficient balance"

    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (receiver,))
    if not cur.fetchone():
        return "❌ Receiver account not found"

    cur.execute("UPDATE accounts SET balance = balance - ? WHERE account_number=?",
                (amount, sender))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE account_number=?",
                (amount, receiver))

    cur.execute("""
        INSERT INTO transactions VALUES (NULL, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (sender, receiver, amount))

    conn.commit()
    conn.close()
    return "✅ Transaction Successful"
