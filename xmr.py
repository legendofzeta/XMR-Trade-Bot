import tkinter as tk
import requests
import hmac
import hashlib
import time

def show_balance():
    # Get the API key and secret key from the GUI
    api_key = api_key_entry.get()
    secret_key = secret_key_entry.get()

    # Endpoint for the balance request
    endpoint = "https://tradeogre.com/api/v1/account/balances"

    # Current timestamp for nonce
    timestamp = str(int(time.time()))

    # Create the message for the HMAC signature
    message = endpoint + timestamp

    # Calculate the HMAC signature
    signature = hmac.new(bytes(secret_key, "latin1"), msg=bytes(message, "latin1"), digestmod=hashlib.sha512).hexdigest()

    # Headers for the API request
    headers = {
        "Api-Key": api_key,
        "Sign": signature,
        "Nonce": timestamp
    }

    # Make the API request to get the balance
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        balance = response.json()

        # Get the XMR balance
        xmr_balance = balance.get("XMR", 0)

        # Update the GUI with the XMR balance
        balance_label.config(text="Your XMR balance is: " + str(xmr_balance))
    else:
        # Update the GUI with the error message
        balance_label.config(text="Error: " + response.text)

# Create the GUI window
root = tk.Tk()
root.title("TradeOgre XMR Balance")

# Create the API key label and entry
api_key_label = tk.Label(root, text="API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(root)
api_key_entry.pack()

# Create the secret key label and entry
secret_key_label = tk.Label(root, text="Secret Key:")
secret_key_label.pack()
secret_key_entry = tk.Entry(root, show="*")
secret_key_entry.pack()

# Create the show balance button
show_button = tk.Button(root, text="Show Balance", command=show_balance)
show_button.pack()

# Create the balance label
balance_label = tk.Label(root, text="")
balance_label.pack()

# Start the GUI event loop
root.mainloop()

