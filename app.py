import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

def load_data():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql("SELECT * FROM Expense_tracker", conn)
    conn.close()
    return df

# sidebar navigation
st.sidebar.title("💰 Expense Tracker")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Navigate to", [
    "➕ Add Expense",
    "👁️ View Expenses",
    "✏️ Update Expense",
    "🗑️ Delete Expense",
    "📊 Analytics",
    "📅 Monthly Summary",
    "🏷️ Category Breakdown"
])

if page == "➕ Add Expense":
    st.title("➕ Add New Expense")
    st.markdown("---")

    category = st.selectbox("Select Category", ["FOOD", "CLOTHES", "VEHICLES", "ELECTRONICS"])
    item = st.text_input("Enter Item Name")
    amount = st.number_input("Enter Amount (₹)", min_value=0.0)
    payment_method = st.selectbox("Select Payment Method", ["Online", "Cash"])

    if st.button("➕ Add Expense"):
        if item.strip() == "":
            st.error("❌ Item name cannot be empty!")
        elif item.isnumeric():
            st.error("❌ Item name cannot be a number!")
        elif amount == 0:
            st.error("❌ Amount cannot be zero!")
        else:
            df = load_data()
            next_id = 1 if df.empty else int(df['ID'].max()) + 1

            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Expense_tracker (ID, Date, Category, Item, Amount, Payment_Method)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (next_id, date.today().strftime("%Y-%m-%d"), category, item, amount, payment_method))
            conn.commit()
            conn.close()

            st.success("✅ Expense added successfully!")
            st.dataframe(load_data())

elif page == "👁️ View Expenses":
    st.title("👁️ View All Expenses")
    st.markdown("---")

    df = load_data()

    filter_category = st.selectbox("Filter by Category",
        ["All", "FOOD", "CLOTHES", "VEHICLES", "ELECTRONICS"])

    if filter_category == "All":
        display_df = df
    else:
        display_df = df[df["Category"] == filter_category]

    st.write(f"Showing {len(display_df)} records")
    st.dataframe(display_df)
    st.info(f"💰 Total: ₹{display_df['Amount'].sum()}")

elif page == "✏️ Update Expense":
    st.title("✏️ Update Expense")
    st.markdown("---")

    df = load_data()

    update_id = st.number_input("Enter Expense ID to Update",
        min_value=1, step=1, key="update_id")

    if st.button("🔍 Find Expense"):
        if update_id not in df['ID'].values:
            st.error(f"❌ No expense found with ID {update_id}!")
        else:
            st.session_state['found_id'] = update_id

    if 'found_id' in st.session_state:
        row = df[df['ID'] == st.session_state['found_id']].iloc[0]

        new_category = st.selectbox("Category",
            ["FOOD", "CLOTHES", "VEHICLES", "ELECTRONICS"],
            index=["FOOD", "CLOTHES", "VEHICLES", "ELECTRONICS"].index(row['Category']))

        new_item = st.text_input("Item Name", value=row['Item'])

        new_amount = st.number_input("Amount (₹)",
            min_value=0.0, value=float(row['Amount']),
            key="update_amount")

        new_payment = st.selectbox("Payment Method",
            ["Online", "Cash"],
            index=["Online", "Cash"].index(row['Payment_Method']))

        if st.button("✅ Save Changes"):
            if new_item.strip() == "":
                st.error("❌ Item name cannot be empty!")
            elif new_item.isnumeric():
                st.error("❌ Item name cannot be a number!")
            elif new_amount == 0:
                st.error("❌ Amount cannot be zero!")
            else:
                conn = sqlite3.connect("expenses.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Expense_tracker 
                    SET Category=?, Item=?, Amount=?, Payment_Method=?
                    WHERE ID=?
                """, (new_category, new_item, new_amount, new_payment,
                      st.session_state['found_id']))
                conn.commit()
                conn.close()

                del st.session_state['found_id']

                st.success("✅ Expense updated successfully!")
                st.dataframe(load_data())

elif page == "🗑️ Delete Expense":
    st.title("🗑️ Delete Expense")
    st.markdown("---")

    df = load_data()

    delete_id = st.number_input("Enter Expense ID to Delete",
        min_value=1, step=1, key="delete_id")

    if st.button("🗑️ Delete Expense"):
        if delete_id not in df['ID'].values:
            st.error(f"❌ No expense found with ID {delete_id}!")
        else:
            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Expense_tracker WHERE ID = ?", (delete_id,))
            conn.commit()
            conn.close()

            st.success(f"✅ Expense ID {delete_id} deleted successfully!")
            st.dataframe(load_data())

elif page == "📊 Analytics":
    st.title("📊 Analytics")
    st.markdown("---")

    df = load_data()

    if df.empty:
        st.warning("⚠️ No expenses to analyse yet!")
    else:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month_name()

        category_spend = df.groupby("Category")["Amount"].sum()
        monthly_spend = df.groupby("Month")["Amount"].sum()

        # bar chart
        st.subheader("💰 Spending by Category")
        fig1, ax1 = plt.subplots()
        category_spend.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Amount (₹)")
        st.pyplot(fig1)

        # pie chart
        st.subheader("🥧 Category Breakdown")
        fig2, ax2 = plt.subplots()
        category_spend.plot(kind="pie", ax=ax2, autopct="%1.1f%%")
        ax2.set_ylabel("")
        st.pyplot(fig2)

        # line chart
        st.subheader("📈 Monthly Trend")
        fig3, ax3 = plt.subplots()
        monthly_spend.plot(kind="line", ax=ax3, marker="o")
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Amount (₹)")
        st.pyplot(fig3)

elif page == "📅 Monthly Summary":
    st.title("📅 Monthly Summary")
    st.markdown("---")

    df = load_data()

    if df.empty:
        st.warning("⚠️ No expenses yet!")
    else:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month_name()

        monthly_summary = df.groupby('Month')['Amount'].agg(['sum', 'mean', 'count'])
        monthly_summary.columns = ['Total Spent', 'Average', 'No. of Expenses']

        st.dataframe(monthly_summary)

        best_month = monthly_summary['Total Spent'].idxmax()
        st.success(f"📈 Highest spending month: {best_month}")
        st.info(f"💰 Total overall: ₹{df['Amount'].sum()}")

elif page == "🏷️ Category Breakdown":
    st.title("🏷️ Category Breakdown")
    st.markdown("---")

    df = load_data()

    if df.empty:
        st.warning("⚠️ No expenses yet!")
    else:
        category_summary = df.groupby('Category')['Amount'].agg(['sum', 'mean', 'count'])
        category_summary.columns = ['Total Spent', 'Average', 'No. of Expenses']
        category_summary = category_summary.sort_values('Total Spent', ascending=False)

        st.dataframe(category_summary)

        top_category = category_summary['Total Spent'].idxmax()
        st.error(f"🔥 You spend most on: {top_category}")
        st.info(f"💰 Total overall: ₹{df['Amount'].sum()}")