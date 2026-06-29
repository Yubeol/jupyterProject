import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, html
import dash_ag_grid as dag

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

# Pivot
pivot_sale = pd.pivot_table(
    sales,
    index="product_name",
    columns=["연도", "분기", "월"],
    values="sales_amount",
    aggfunc="sum",
    fill_value=0
).reset_index()

# -------------------------------
# 컬럼명을 문자열로 변경
# -------------------------------
rename_dict = {}

new_columns = []

for col in pivot_sale.columns:
    if isinstance(col, tuple):
        # 첫 번째 컬럼
        if col[0] == "product_name":
            new_columns.append("product_name")
        else:
            new_columns.append(f"{col[0]}|{col[1]}|{col[2]}")
    else:
        new_columns.append(col)

pivot_sale.columns = new_columns

# -------------------------------
# 계층형 컬럼 생성
# -------------------------------
columnDefs = [
    {
        "headerName": "제품명",
        "field": "product_name",
        "pinned": "left",
        "width": 180
    }
]

years = {}

for field in pivot_sale.columns[1:]:

    year, quarter, month = field.split("|")

    years.setdefault(year, {})
    years[year].setdefault(quarter, [])

    years[year][quarter].append({
        "headerName": month,
        "field": field,
        "width": 90,
        "type": "numericColumn"
    })

# 연도 → 분기 → 월
for year in sorted(years.keys()):

    q_children = []

    for quarter in sorted(years[year].keys()):

        q_children.append({
            "headerName": quarter,
            "children": years[year][quarter]
        })

    columnDefs.append({
        "headerName": year,
        "children": q_children
    })

# -------------------------------
# Dash
# -------------------------------
app = Dash(__name__)

app.layout = html.Div(
    [
        dag.AgGrid(
            id="pivot-grid",
            rowData=pivot_sale.to_dict("records"),
            columnDefs=columnDefs,

            defaultColDef={
                "sortable": True,
                "filter": True,
                "resizable": True,
                "editable": False
            },

            dashGridOptions={
                "animateRows": True
            },

            style={
                "height": "700px",
                "width": "100%"
            }
        )
    ],
    style={"padding": "20px"}
)

if __name__ == "__main__":
    app.run(debug=True)