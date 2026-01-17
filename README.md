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


