# 🚀 NASA Near-Earth Object Tracker

Advanced Intelligence System for Asteroid Monitoring using Streamlit and SQLite.

## 📋 Features

- Real-time asteroid tracking dashboard
- Interactive SQL query explorer
- Advanced filtering system
- Risk analysis and analytics
- Visualization of asteroid approaches

## 🛠️ Technologies Used

- **Python 3.7**
- **Streamlit** - Web framework
- **SQLite** - Database
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/ps-learner/nasa-neo-tracker.git
cd nasa-neo-tracker
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run test_dashboard.py
```

## 📁 Project Structure
```
├── test_dashboard.py  # Main dashboard application
├── project_sql_queries.py          # SQL queries module
├── nasa_neo.db                     # SQLite database
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🎯 Usage

1. **Overview Page**: View database statistics and key metrics
2. **SQL Queries**: Execute pre-built queries and explore data
3. **Advanced Filters**: Custom filtering by velocity, size, and distance
4. **Analytics**: Advanced visualizations and risk analysis

## 📊 Database Schema

- **asteroids**: Asteroid information (name, size, hazard status)
- **close_approach**: Approach data (date, velocity, distance)

## 👨‍💻 Author

Pratyusha - https://github.com/ps-learner
