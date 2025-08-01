import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MySQL connection info
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Akshat@1122',
    'database': 'food_waste_data'
}

# Helper to run SQL queries
def run_query(query):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Helper to fetch data from a table
@st.cache_data
def fetch_data(table):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        return pd.read_sql(f"SELECT * FROM {table}", conn)
    except Exception as e:
        st.error(f"Error loading table {table}: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Streamlit App
st.set_page_config(page_title="Food Waste Dashboard", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Project Introduction", "Data Visualization", "SQL Queries", "Creator Info"])

# Load data
providers_df = fetch_data("providers")
receivers_df = fetch_data("receivers")
food_df = fetch_data("food_listings")
claims_df = fetch_data("claims")

# 1. Project Intro
if page == "Project Introduction":
    st.title("🍲 Food Waste Management Dashboard")
    st.image("C:/Users/ASUS/OneDrive/Desktop/AdobeStock_264542845.jpeg")
    st.subheader("About Project")
    st.write("""
        Food wastage is a significant issue, with many households and restaurants discarding surplus food while numerous people struggle 
        with food insecurity. This dashboard helps manage and analyze food donations by providers such as restaurants and grocery stores,
        and receivers like NGOs and shelters. Key features:
        - View and explore data from the food waste database
        - Visualize trends with graphs
        - Run SQL queries to gain deeper insights
        - CRUD Operations
    """)

# 2. Data Visualization
elif page == "Data Visualization":
    st.success("You are on the Data Visualization page")

    st.title("📊 Data Visualization")

    table_option = st.selectbox("Select table to explore", ["providers", "receivers", "food_listings", "claims"])

    if table_option == "providers":
        st.write(providers_df)
        st.bar_chart(providers_df["City"].value_counts())

    elif table_option == "receivers":
        st.write(receivers_df)
        st.bar_chart(receivers_df["City"].value_counts())

    elif table_option == "food_listings":
        st.write(food_df)
        st.bar_chart(food_df["Meal_Type"].value_counts())

    elif table_option == "claims":
        st.write(claims_df)
        st.bar_chart(claims_df["Status"].value_counts())

    search_term = st.text_input("Search inside table")
    if search_term:
        df_map = {
            "providers": providers_df,
            "receivers": receivers_df,
            "food_listings": food_df,
            "claims": claims_df
        }
        selected_df = df_map[table_option]
        filtered = selected_df[selected_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        st.dataframe(filtered)

    # CRUD starts here
    st.markdown("---")
    st.subheader("Perform CRUD Operations")

    crud_option = st.selectbox("Choose Operation", ["Create Table", "Read Table", "Update Table", "Delete Table"])

    if crud_option == "Create Table":
        st.markdown("Create New Table")
        new_table_name = st.text_input("Enter new table name")
        columns_def = st.text_area("Enter column definitions (e.g., id INT PRIMARY KEY, name VARCHAR(50))")

        if st.button("Create Table"):
            if new_table_name and columns_def:
                try:
                    conn = mysql.connector.connect(**db_config)
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE TABLE {new_table_name} ({columns_def})")
                    conn.commit()
                    st.success(f"✅ Table '{new_table_name}' created successfully.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                st.warning("Please enter both table name and column definitions.")

    elif crud_option == "Read Table":
        st.markdown("Read Table")
        read_table_name = st.text_input("Enter table name to read")
        if st.button("Load Table"):
            df = fetch_data(read_table_name)
            if not df.empty:
                st.dataframe(df)
            else:
                st.warning("No data found or table does not exist.")

    elif crud_option == "Update Table":
        st.markdown("Update Table Data")
        table_to_update = st.text_input("Enter table name to update")
        update_query = st.text_area("Enter SQL UPDATE statement")

        if st.button("Run Update"):
            if update_query:
                try:
                    conn = mysql.connector.connect(**db_config)
                    cursor = conn.cursor()
                    cursor.execute(update_query)
                    conn.commit()
                    st.success("✅ Update successful.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                st.warning("Enter a valid SQL UPDATE query.")

    elif crud_option == "Delete Table":
        st.markdown("Delete Table")
        del_table_name = st.text_input("Enter table name to delete")

        if st.button("Delete Table"):
            if del_table_name:
                confirm = st.checkbox("I confirm I want to delete this table (This action is irreversible)")
                if confirm:
                    try:
                        conn = mysql.connector.connect(**db_config)
                        cursor = conn.cursor()
                        cursor.execute(f"DROP TABLE {del_table_name}")
                        conn.commit()
                        st.success(f"✅ Table '{del_table_name}' deleted successfully.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
            else:
                st.warning("Please enter a table name.")

# 3. SQL Queries
elif page == "SQL Queries":
    st.title("🔢 SQL Query Explorer")

    questions = [
        ("1. How many food providers and receivers are there in each city?",
         "SELECT City, COUNT(*) AS Total_Providers FROM providers GROUP BY City"),

        ("2. Which type of food provider contributes the most food?",
        "SELECT Provider_Type AS Type, COUNT(*) AS Food_count FROM food_listings GROUP BY Provider_Type ORDER BY Food_count DESC LIMIT 1"),

        ("3. What is the contact info of food providers in a specific city?",
         "SELECT Name, Contact FROM providers WHERE City = 'New Jessica'"),

        ("4. Which receivers have claimed the most food?",
         "SELECT r.Name, SUM(f.quantity) AS total_claimed FROM claims c JOIN receivers r ON c.Reciever_ID = r.Receiver_ID JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY r.Name ORDER BY total_claimed DESC LIMIT 1"),

        ("5. What is the total quantity of food available?",
         "SELECT SUM(Quantity) AS Total_Food_Quantity FROM food_listings"),

        ("6. Which city has the highest number of food listings?",
         "SELECT Location AS City, COUNT(*) AS Listings FROM food_listings GROUP BY Location ORDER BY Listings DESC LIMIT 1"),

        ("7. What are the most commonly available food types?",
         "SELECT Food_Type, COUNT(*) AS Count FROM food_listings GROUP BY Food_Type ORDER BY Count DESC"),

        ("8. How many food claims for each food item?",
         "SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY f.Food_Name ORDER BY total_claims DESC"),

        ("9. Which provider had the highest number of successful food claims?",
         "SELECT p.Name, COUNT(c.Claim_ID) AS successful_claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN providers p ON f.Provider_ID = p.Providers_ID WHERE c.Status = 'Completed' GROUP BY p.Name ORDER BY successful_claims DESC LIMIT 1"),

        ("10. What % of food claims are completed vs. pending vs. canceled?",
         "SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage FROM claims GROUP BY Status"),

        ("11. Avg quantity of food claimed per receiver?",
         "SELECT r.Name, AVG(CAST(f.Quantity AS UNSIGNED)) AS avg_quantity_claimed FROM claims c JOIN receivers r ON c.Reciever_ID = r.Receiver_ID JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY r.Name ORDER BY avg_quantity_claimed DESC"),

        ("12. Which meal type is claimed the most?",
         "SELECT f.Meal_Type, COUNT(c.Claim_ID) AS total_claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY f.Meal_Type ORDER BY total_claims DESC"),

        ("13. Total quantity of food donated by each provider",
         "SELECT p.Name AS provider_name, SUM(CAST(f.Quantity AS UNSIGNED)) AS total_quantity_donated FROM food_listings f JOIN providers p ON f.Provider_ID = p.Providers_ID GROUP BY p.Name ORDER BY total_quantity_donated DESC"),

        ("14. Top 10 providers",
         "SELECT Name, Type, City FROM providers LIMIT 10"),

        ("15. How many meal types available?",
         "SELECT Meal_Type, COUNT(*) FROM food_listings GROUP BY Meal_Type"),

        ("16. Which city has most food receivers?",
         "SELECT City, COUNT(*) AS Total FROM receivers GROUP BY City ORDER BY Total DESC LIMIT 1"),

        ("17. Which food type has many providers?",
         "SELECT Food_Type, COUNT(DISTINCT Provider_ID) AS Provider_Count FROM food_listings GROUP BY Food_Type ORDER BY Provider_Count DESC"),

        ("18. Number of claims that are cancelled",
         "SELECT COUNT(*) AS Cancelled_Claims FROM claims WHERE Status = 'Cancelled'"),
    ]

    selected_q = st.selectbox("Choose a question", [q[0] for q in questions])
    query = dict(questions)[selected_q]
    st.code(query, language="sql")

    if st.button("Run Query"):
        result = run_query(query)
        st.dataframe(result)

# 4. Creator Info
elif page == "Creator Info":
    st.title("👨‍💼 Creator info")

    st.markdown("""
    **👤 Developed by:** Akshat Aman  
    **💼 Skills:** Python, SQL, Data Analysis, Streamlit, Pandas  
    **📧 Email:** akshataman35@gmail.com  
    **🌐 GitHub:** [AkshatAman03](https://github.com/AkshatAman03)  
    **📊 Project:** Food Waste Management System
    """)
