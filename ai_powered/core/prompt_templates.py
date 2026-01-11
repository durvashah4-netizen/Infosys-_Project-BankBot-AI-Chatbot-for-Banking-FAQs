SYSTEM_PROMPT = """
You are a banking assistant.
Always return valid JSON.
If details are missing, return null.
"""

USER_PROMPT = """
User query: {message}

Return JSON:
{{
 "intent": "",
 "account_number": null,
 "to_account": null,
 "amount": null,
 "password": null
}}
"""
