from database.bank_crud import (
    create_account,
    get_account,
    list_accounts,
    transfer_money,
    check_balance
)


def handle_action(parsed: dict):
    intent = parsed.get("intent")

    # ---------------- CHECK BALANCE ----------------
    if intent == "check_balance":
        balance = check_balance(parsed["account_number"])
        if balance is None:
            return "❌ Account not found"
        return f"💰 Your balance is ₹{balance}"

    # ---------------- TRANSFER ----------------
    if intent == "transfer_money":
        return transfer_money(
            parsed["account_number"],
            parsed["to_account"],
            parsed["amount"],
            parsed["password"]
        )

    # ---------------- LIST ACCOUNTS ----------------
    if intent == "list_accounts":
        accounts = list_accounts()
        if not accounts:
            return "❌ No accounts found"

        response = "📋 Accounts:\n"
        for acc in accounts:
            response += f"• {acc[0]} ({acc[1]}) – ₹{acc[2]}\n"
        return response

    # ---------------- CREATE ACCOUNT ----------------
    if intent == "create_account":
        create_account(
            parsed["user_id"],
            parsed["account_number"],
            parsed["account_type"],
            parsed["balance"],
            parsed["password"]
        )
        return "✅ Account created successfully"

    # ---------------- ATM INFO ----------------
    if intent == "atm_details":
        return (
            "🏧 Nearby ATMs:\n"
            "1. SBI ATM – MG Road\n"
            "2. ICICI ATM – City Center\n"
            "3. HDFC ATM – Station Road"
        )

    return "🤖 Sorry, I didn’t understand your request"
