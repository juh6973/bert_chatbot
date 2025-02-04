import tkinter as tk
from tkinter import ttk, messagebox
import requests

# API endpoint (Make sure your FastAPI backend is running)
API_URL = "http://127.0.0.1:8000/analyze/"

# Function to send API request and get sentiment analysis
def analyze_sentiment():
    text = text_entry.get("1.0", tk.END).strip()  # Get input text
    model_choice = model_var.get()  # Get selected model

    if not text:
        messagebox.showwarning("Input Error", "Please enter text for analysis.")
        return

    payload = {"text": text, "model": model_choice}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            sentiment = response_data.get("sentiment_analysis", {}).get("sentiment", "Error")
            confidence = response_data.get("sentiment_analysis", {}).get("confidence_score", "N/A")

            # Update result labels
            sentiment_label.config(text=f"Sentiment: {sentiment}")
            confidence_label.config(text=f"Confidence Score: {confidence}")
        else:
            messagebox.showerror("API Error", f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Failed to connect to API.\n{e}")

# Create the main application window
root = tk.Tk()
root.title("Sentiment Analysis UI")
root.geometry("400x350")
root.resizable(False, False)

# Heading
title_label = tk.Label(root, text="Sentiment Analysis", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Text input
text_label = tk.Label(root, text="Enter your text:")
text_label.pack()
text_entry = tk.Text(root, height=5, width=40)
text_entry.pack(pady=5)

# Model selection dropdown
model_label = tk.Label(root, text="Select Model:")
model_label.pack()
model_var = tk.StringVar(value="custom")  # Default to "custom"
model_dropdown = ttk.Combobox(root, textvariable=model_var, values=["custom", "llama"], state="readonly")
model_dropdown.pack(pady=5)

# Analyze button
analyze_button = tk.Button(root, text="Analyze Sentiment", command=analyze_sentiment, bg="blue", fg="white")
analyze_button.pack(pady=10)

# Sentiment output label
sentiment_label = tk.Label(root, text="Sentiment: ", font=("Arial", 12))
sentiment_label.pack(pady=5)

# Confidence score output label
confidence_label = tk.Label(root, text="Confidence Score: ", font=("Arial", 12))
confidence_label.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()