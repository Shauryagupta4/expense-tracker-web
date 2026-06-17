# Personal Expense Tracker Web App

A full-featured personal finance web app built with Python and Streamlit.
Track your daily expenses, view analytics, and manage your spending — all from your browser!

**Live App:** [Click here to try it](https://share.streamlit.io)  

---

## Features

-  **Add Expense** — Add daily expenses with category, item, amount and payment method
-  **View Expenses** — View and filter all expenses by category with total amount
-  **Update Expense** — Edit any existing expense record
-  **Delete Expense** — Safely delete expenses by ID
-  **Analytics** — Bar chart, pie chart and line chart for spending insights
-  **Monthly Summary** — Month wise spending breakdown with averages
-  **Category Breakdown** — See which category you spend most on

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface and deployment |
| SQLite | Local database for storing expenses |
| Pandas | Data handling and analysis |
| Matplotlib | Charts and visualizations |

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Shauryagupta4/expense-tracker-web.git
cd expense-tracker-web
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Open your browser**
```
http://localhost:8501
```

---

## Project Structure

```
expense-tracker-web/
├── app.py              # Main Streamlit application
├── expenses.db         # SQLite database with sample data
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Pages Overview

### Add Expense
- Select category from dropdown
- Enter item name with validation
- Enter amount with minimum value check
- Select payment method (Online/Cash)
- Auto generates ID and captures today's date

### View Expenses
- Filter expenses by category
- Shows record count dynamically
- Shows total amount for filtered data

### Analytics
- Bar chart — total spending per category
- Pie chart — category breakdown percentage
- Line chart — monthly spending trend

### Monthly Summary
- Month wise total, average and count
- Highlights highest spending month

### Category Breakdown
- Category wise total, average and count
- Highlights top spending category

---

## What I Learned

- Building web apps with Streamlit using only Python
- Connecting SQLite database to a web interface
- Input validation and error handling in web apps
- Displaying Pandas DataFrames as interactive tables
- Embedding Matplotlib charts in a web browser
- Multi-page navigation using st.sidebar
- Session state management for persistent UI
- Deploying Python web apps on Streamlit Cloud

---

## About

Built by **Shaurya** — 2nd year AIML student  
This is my first web app project, converting a terminal-based Expense Tracker into a full web application.

---