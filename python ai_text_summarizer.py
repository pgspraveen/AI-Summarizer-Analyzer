# ----------------- IMPORT LIBRARIES -----------------
import tkinter as tk  # GUI library for creating desktop windows and widgets
from tkinter import messagebox, scrolledtext  # messagebox: pop-up dialogs | scrolledtext: text box with scrollbar
from transformers import pipeline  # Hugging Face library to load pre-trained AI models
import sqlite3  # Built-in Python library for lightweight file-based database
from datetime import datetime  # For getting current date and time as timestamps
from collections import Counter  # Counts frequency of elements in a list
import matplotlib.pyplot as plt  # For creating charts and graphs

# ----------------- LOAD AI MODEL -----------------
# Keeping original Hugging Face DistilBART model
summarizer = pipeline(
    "summarization",              # Task type: condenses long text into shorter form
    model="sshleifer/distilbart-cnn-12-6",  # Pre-trained model from Hugging Face Hub
    revision="a4f8f3e",           # Pins to a specific model version for consistency
    device=-1                     # -1 = run on CPU (use 0 for GPU)
)

# ----------------- DATABASE SETUP -----------------
conn = sqlite3.connect("summaries.db")  # Opens (or creates) the SQLite database file
cursor = conn.cursor()  # Cursor is used to execute SQL queries

cursor.execute("""
CREATE TABLE IF NOT EXISTS summary_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique auto-incrementing row ID
    input_text TEXT,                       -- Original text entered by user
    summary_text TEXT,                     -- AI-generated summary
    created_at TEXT                        -- Timestamp of when the record was saved
)
""")
conn.commit()  # Save the table creation to disk

# ----------------- SAVE TO DATABASE -----------------
def save_to_db(input_text, summary_text):
    """Save original text and summary into database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: 2025-07-15 14:30:05

    cursor.execute(
        "INSERT INTO summary_history (input_text, summary_text, created_at) VALUES (?, ?, ?)",
        # '?' placeholders prevent SQL injection attacks
        (input_text, summary_text, timestamp)
    )
    conn.commit()  # Persist the new row to disk


# ----------------- SUMMARIZE FUNCTION -----------------
def summarize_text():
    """Generate summary and display it."""

    input_text = text_input.get("1.0", tk.END).strip()  # Read all text from input box
    input_text = " ".join(input_text.split())  # Normalize multiple spaces/newlines to single spaces

    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    if len(input_text.split()) < 30:  # Enforce minimum word count for meaningful summarization
        messagebox.showwarning(
            "Input Error",
            "Please enter at least 30 words."
        )
        return

    input_text = input_text[:2000]  # Truncate to 2000 chars to stay within model limits

    try:

        total_words = len(input_text.split())

        max_len = min(100, total_words // 2)   # Summary cap: half of input or 100 tokens max
        min_len = max(25, total_words // 4)    # Summary floor: quarter of input or 25 tokens min

        summary = summarizer(
            input_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False  # False = deterministic output (no randomness)
        )

        if summary and len(summary) > 0:
            summary_text = summary[0]["summary_text"]  # Extract text from pipeline result dict
        else:
            summary_text = "Unable to generate summary."

        summary_output.delete("1.0", tk.END)  # Clear previous output before inserting new one
        summary_output.insert(tk.END, summary_text)

        save_to_db(input_text, summary_text)

        messagebox.showinfo(
            "Success",
            "Summary saved successfully."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))  # Display any runtime error to the user


# ----------------- VIEW HISTORY -----------------
def view_history():

    history_window = tk.Toplevel(app)  # Opens a new child window on top of the main window
    history_window.title("Summary History")
    history_window.geometry("700x500")

    history_box = scrolledtext.ScrolledText(
        history_window,
        wrap=tk.WORD,  # Wrap lines at word boundaries
        width=80,
        height=30
    )
    history_box.pack(padx=10, pady=10)

    cursor.execute("SELECT * FROM summary_history ORDER BY id DESC")  # Newest records first
    records = cursor.fetchall()  # Returns all rows as a list of tuples

    for record in records:
        history_box.insert(tk.END, f"ID: {record[0]}\n")
        history_box.insert(tk.END, f"Input Text:\n{record[1]}\n\n")
        history_box.insert(tk.END, f"Summary:\n{record[2]}\n")
        history_box.insert(tk.END, f"Created At: {record[3]}\n")
        history_box.insert(tk.END, "-" * 80 + "\n\n")  # Visual separator between records


# ----------------- ANALYTICS -----------------
def analyze_data():

    cursor.execute("SELECT input_text, summary_text FROM summary_history")
    records = cursor.fetchall()

    if not records:
        messagebox.showwarning("No Data", "No summaries found.")
        return

    total_summaries = len(records)

    total_input_words = sum(len(r[0].split()) for r in records)   # Total words across all inputs
    total_summary_words = sum(len(r[1].split()) for r in records)  # Total words across all summaries

    avg_input_len = total_input_words / total_summaries
    avg_summary_len = total_summary_words / total_summaries

    all_words = " ".join(r[0] for r in records).lower().split()  # Combine all input texts into one word list

    stop_words = {
        'the', 'is', 'a', 'an', 'and', 'to', 'of', 'in',
        'for', 'with', 'on', 'this', 'that',
        'are', 'was', 'were', 'be', 'has', 'have'
    }  # Common words filtered out so analysis focuses on meaningful keywords

    filtered_words = [w for w in all_words if w not in stop_words]

    top_keywords = Counter(filtered_words).most_common(5)  # Top 5 most frequent meaningful words

    analysis_text = (
        f"Total Summaries: {total_summaries}\n"
        f"Average Input Length: {avg_input_len:.1f} words\n"   # :.1f = 1 decimal place
        f"Average Summary Length: {avg_summary_len:.1f} words\n"
        f"Top Keywords: {', '.join([k for k, _ in top_keywords])}"  # Extract only words, ignore counts
    )

    messagebox.showinfo("Data Analysis", analysis_text)

    if top_keywords:
        keywords, counts = zip(*top_keywords)  # Unpack list of (word, count) tuples into two separate tuples

        plt.bar(keywords, counts, color="skyblue")
        plt.title("Top Keywords in Input Text")
        plt.show()


# ----------------- GUI -----------------
app = tk.Tk()  # Creates the main application window
app.title("🧠 AI Text Summarizer & Data Analytics")
app.geometry("700x650")
app.configure(bg="#ffffff")  # White background

tk.Label(
    app,
    text="Enter text to summarize:",
    font=("Helvetica", 12),
    bg="#ffffff"
).pack(pady=10)

text_input = tk.Text(app, height=10, width=80, wrap=tk.WORD)  # Multi-line input box
text_input.pack(pady=5)

btn_frame = tk.Frame(app, bg="#ffffff")  # Invisible container to group buttons side by side
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Summarize",
          font=("Helvetica", 12),
          bg="blue", fg="white",
          command=summarize_text).grid(row=0, column=0, padx=10)  # command= binds the button click to a function

tk.Button(btn_frame, text="View History",
          font=("Helvetica", 12),
          bg="green", fg="white",
          command=view_history).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Analyze Data",
          font=("Helvetica", 12),
          bg="orange",
          command=analyze_data).grid(row=0, column=2, padx=10)

tk.Label(app, text="Summarized Output:",
         font=("Helvetica", 12),
         bg="#ffffff").pack(pady=10)

summary_output = tk.Text(
    app,
    height=8,
    width=80,
    wrap=tk.WORD,
    bg="#f0f0f0"  # Light grey to visually distinguish output area from input
)
summary_output.pack(pady=5)

app.mainloop()  # Starts the event loop — keeps the window open and listens for user interactions

