import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, html, dcc, Input, Output, dash
import dash_ag_grid as dag
import plotly.express as px
# PostgreSQL 연결
engine = create_engine("postgresql://kogo:math1106@localhost:5432/mydb")
# 데이터 조회
sql = """
SELECT *
FROM vw_sales;
"""
sales = pd.read_sql(sql, engine)
# 날짜 컬럼 생성
sales["연도"] = pd.to_datetime(sales["date"]).dt.year.astype(str)
sales["분기"] = "Q" + pd.to_datetime(sales["date"]).dt.quarter.astype(str)
sales["월"] = pd.to_datetime(sales["date"]).dt.strftime("%b")

group_customer_sales = (sales.groupby("customer_name")['sales_amount']
                        .sum()
                        .reset_index()
                        .sort_values("sales_amount", ascending=False)
                        .head(20)
                        )
# print(group_year_sales)
# exit()


fig = px.bar(
    group_year_sales,
    x="sales_amount",
    y="custmer_name",
)

app = dash.Dash(__name__)
app.layout = dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run(debug=True)