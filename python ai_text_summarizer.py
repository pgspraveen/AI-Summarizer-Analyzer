# ----------------- IMPORT LIBRARIES -----------------
import tkinter as tk  # GUI library
from tkinter import messagebox, scrolledtext  # Popups and scrollable text boxes
from transformers import pipeline  # HuggingFace AI model
import sqlite3  # SQLite database
from datetime import datetime  # For timestamps
from collections import Counter  # For counting top keywords
import matplotlib.pyplot as plt  # For visualization

# ----------------- LOAD AI MODEL -----------------
# Using pre-trained DistilBART summarization model from HuggingFace
summarizer = pipeline(
    "summarization",  # Task: summarization
    model="sshleifer/distilbart-cnn-12-6",  # Pre-trained model
    revision="a4f8f3e",  # Specific model version
    device=-1  # Use CPU (-1), set 0 if you have GPU
)

# ----------------- DATABASE SETUP -----------------
# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("summaries.db")
cursor = conn.cursor()  # Cursor object to execute SQL commands

# Create a table for storing input + summary
# id -> unique ID
# input_text -> original paragraph
# summary_text -> AI-generated summary
# created_at -> timestamp of saving
cursor.execute("""
CREATE TABLE IF NOT EXISTS summary_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT,
    summary_text TEXT,
    created_at TEXT
)
""")
conn.commit()  # Save changes to database

# ----------------- FUNCTION TO SAVE DATA -----------------
def save_to_db(input_text, summary_text):
    """Save input text, summary, and timestamp to database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    cursor.execute(
        "INSERT INTO summary_history (input_text, summary_text, created_at) VALUES (?, ?, ?)",
        (input_text, summary_text, timestamp)  # Values to insert
    )
    conn.commit()  # Commit changes

# ----------------- FUNCTION TO SUMMARIZE TEXT -----------------
def summarize_text():
    """Take user input, summarize using AI, display and save."""
    input_text = text_input.get("1.0", tk.END).strip()  # Get text from input box

    if not input_text:  # Check if input is empty
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    try:
        # Generate summary using AI model
        summary = summarizer(input_text, max_length=50, min_length=25, do_sample=False)
        summary_text = summary[0]['summary_text']  # Extract summary

        # Show summary in output box
        summary_output.delete("1.0", tk.END)  # Clear previous summary
        summary_output.insert(tk.END, summary_text)  # Insert new summary

        # Save input and summary to database
        save_to_db(input_text, summary_text)

        messagebox.showinfo("Success", "Summary saved to database!")  # Notify user

    except Exception as e:
        messagebox.showerror("Error", str(e))  # Show error popup

# ----------------- FUNCTION TO VIEW HISTORY -----------------
def view_history():
    """Open a new window to display all past summaries."""
    history_window = tk.Toplevel(app)  # Create a new window
    history_window.title("Summary History")
    history_window.geometry("700x500")

    # Scrollable text box for history
    history_box = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, width=80, height=30)
    history_box.pack(padx=10, pady=10)

    # Fetch all records from database, newest first
    cursor.execute("SELECT * FROM summary_history ORDER BY id DESC")
    records = cursor.fetchall()

    # Insert records into history box
    for record in records:
        history_box.insert(tk.END, f"ID: {record[0]}\n")  # Record ID
        history_box.insert(tk.END, f"Input Text:\n{record[1]}\n\n")  # Original text
        history_box.insert(tk.END, f"Summary:\n{record[2]}\n")  # Summary
        history_box.insert(tk.END, f"Created At: {record[3]}\n")  # Timestamp
        history_box.insert(tk.END, "-"*80 + "\n\n")  # Separator

# ----------------- FUNCTION TO ANALYZE DATA -----------------
def analyze_data():
    """Analyze all summaries: word counts, averages, top keywords, charts."""
    cursor.execute("SELECT input_text, summary_text FROM summary_history")
    records = cursor.fetchall()

    if not records:  # If database is empty
        messagebox.showwarning("No Data", "No summaries found to analyze.")
        return

    # Total summaries
    total_summaries = len(records)

    # Count words in input and summary
    total_input_words = sum(len(r[0].split()) for r in records)
    total_summary_words = sum(len(r[1].split()) for r in records)

    # Calculate averages
    avg_input_len = total_input_words / total_summaries
    avg_summary_len = total_summary_words / total_summaries

    # Extract top keywords from all input texts
    all_words = " ".join(r[0] for r in records).lower().split()
    stop_words = {'the','is','a','an','and','to','of','in','for','with','on','this','that'}  # Common words to ignore
    filtered_words = [w for w in all_words if w not in stop_words]  # Remove stop words
    top_keywords = Counter(filtered_words).most_common(5)  # Top 5 words

    # Prepare analysis text
    analysis_text = (
        f"Total Summaries: {total_summaries}\n"
        f"Average Input Length: {avg_input_len:.1f} words\n"
        f"Average Summary Length: {avg_summary_len:.1f} words\n"
        f"Top Keywords: {', '.join([k for k,_ in top_keywords])}"
    )
    messagebox.showinfo("Data Analysis", analysis_text)  # Show popup

    # Plot top keywords chart
    if top_keywords:
        keywords, counts = zip(*top_keywords)  # Split keywords and counts
        plt.bar(keywords, counts, color='skyblue')  # Create bar chart
        plt.title("Top Keywords in Input Text")  # Chart title
        plt.show()  # Display chart

# ----------------- GUI SETUP -----------------
app = tk.Tk()  # Create main window
app.title("🧠 AI Text Summarizer & Data Analytics")
app.geometry("700x650")  # Window size
app.configure(bg="#ffffff")  # Background color

# Input label and box
tk.Label(app, text="Enter text to summarize:", font=("Helvetica", 12), bg="#ffffff").pack(pady=10)
text_input = tk.Text(app, height=10, width=80, wrap=tk.WORD)
text_input.pack(pady=5)

# Buttons frame
btn_frame = tk.Frame(app, bg="#ffffff")
btn_frame.pack(pady=10)

# Buttons
tk.Button(btn_frame, text="Summarize", font=("Helvetica", 12), bg="blue", fg="white",
          command=summarize_text).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="View History", font=("Helvetica", 12), bg="green", fg="white",
          command=view_history).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Analyze Data", font=("Helvetica", 12), bg="orange", fg="white",
          command=analyze_data).grid(row=0, column=2, padx=10)

# Output label and box
tk.Label(app, text="Summarized Output:", font=("Helvetica", 12), bg="#ffffff").pack(pady=10)
summary_output = tk.Text(app, height=8, width=80, wrap=tk.WORD, bg="#f0f0f0")
summary_output.pack(pady=5)

# Run the GUI
app.mainloop()  # Start Tkinter event loop

