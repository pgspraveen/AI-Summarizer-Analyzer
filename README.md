🧠 AI Text Summarizer & Data Analytics

This project is a Python-based application that allows users to summarize text using AI, store the results in a database, view history, and perform simple data analysis. It combines AI (NLP), SQLite database, GUI development, and data visualization in a single project.

🔹 Features

Text Summarization

Uses a pre-trained DistilBART model from HuggingFace to generate concise summaries of any input text.

Database Storage

Stores the original text, generated summary, and timestamp in a SQLite database.

Allows retrieval of previous summaries.

View History

Displays all past summaries in a scrollable window with input text, summary, and timestamp.

Data Analysis

Calculates:

Total number of summaries

Average input text length

Average summary length

Top 5 keywords in all input texts

Displays results in a popup and shows a bar chart for the top keywords.

Graphical User Interface (GUI)

Built using Tkinter for easy user interaction.

Buttons for summarization, viewing history, and analyzing data.

🔹 Technologies Used

Python 3.x

Tkinter – GUI

HuggingFace Transformers – Pre-trained NLP model

SQLite – Database for storing summaries

Matplotlib – Visualization

Collections.Counter – For keyword analysis

🔹 Installation

Clone the repository:

git clone https://github.com/yourusername/ai-text-summarizer.git
cd ai-text-summarizer


Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux


Install required packages:

pip install transformers matplotlib


Note: Tkinter usually comes pre-installed with Python.
For HuggingFace, you might need:

pip install torch

🔹 How to Run
python python_ai_text_summarizer.py


Enter any paragraph in the input box.

Click Summarize to generate a summary.

Click View History to see all past summaries.

Click Analyze Data to view analytics and top keywords.

🔹 Project Structure
ai-text-summarizer/
│
├─ python_ai_text_summarizer.py    # Main Python script
├─ summaries.db                    # SQLite database (auto-created)
├─ README.md                       # Project documentation

🔹 Learning Outcomes

Learned how to integrate AI/NLP models in Python.

Implemented database operations using SQLite.

Built a GUI application using Tkinter.

Performed data analysis and visualizations using Matplotlib.

Gained experience combining multiple technologies into a single project.

🔹 Future Improvements

Add support for multiple languages.

Include export to PDF/CSV functionality for summaries.

Allow batch text summarization.

Improve UI using frameworks like PyQt or Kivy.
