# Local-Food-Wastage-Management-System
Project Overview:
This project is a Streamlit-based web dashboard designed to manage and visualize food waste distribution across various stakeholders like food providers, receivers, and claims from a MySQL database. It aims to support a more efficient food donation ecosystem by tracking, analyzing, and visualizing food listings and claims.
This dashboard helps manage and analyze food donations by providers such as restaurants and grocery stores, and receivers like NGOs and shelters. Key features:
- View and explore data from the food waste database
- Visualize trends with graphs
- Run SQL queries to gain deeper insights
- CRUD Operations

Features:
Multi-page Streamlit App with the following pages:
- Project Introduction
- Data Visualization
- SQL Queries
- Creator Info

MySQL Database Integration:
Fetches real-time data from 4 main tables:
- providers
- receivers
- food_listings
- claims

Interactive Visualizations:
- Bar plots, pie charts, line graphs, and count plots using Matplotlib and Seaborn

Sidebar Navigation:
- Radio buttons for page selection
- Search/filtering within tables

Caching Mechanism:
- Optimized data loading using @st.cache_data 

Tech Stack:
           Tool           |            Purpose                           
 ------------------------------------------------------------ 
 🐍 Python               | Backend logic and data processing 
 🧮 MySQL                | Relational database               
 📊 Pandas               | Data manipulation                 
 📈 Seaborn & Matplotlib | Data visualizations               
 🌐 Streamlit            | Frontend web app                  
 💾 MySQL Connector      | Database connection               

Food wastage is a significant issue, with many households and restaurants discarding surplus food while numerous people struggle with food insecurity. This project aims to develop a Local Food Wastage Management System, where:
- Restaurants and individuals can list surplus food.
- NGOs or individuals in need can claim the food.
- SQL stores available food details and locations.
- A Streamlit app enables interaction, filtering, CRUD operation and visualization.

