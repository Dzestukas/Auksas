import streamlit as st
import requests


def send_telegram_message(message):

    try:
        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, json=payload)

        return response.json()

    except Exception as e:
        return {
            "error": str(e)
        }
