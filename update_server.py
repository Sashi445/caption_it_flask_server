import requests
import os


def send_update_to_nodejs(update_data):
    webhook_url = os.getenv('webhook_url')
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, json=update_data, headers=headers)

        if response.status_code == 200:
            print("Update sent successfully.")
        else:
            print(f"Failed to send update. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error sending update: {str(e)}")
