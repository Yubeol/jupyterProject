from unittest import result

import pandas as pd

if __name__ == "__main__":
    sales = pd.read_pickle("./data/merged_sales.pkl")

    new_sales = sales.loc[:9, ['고객명', '제품명', "판매금액"]]
    new_sales.drop(3, axis=0, inplace=True)
    new_sales.reset_index(drop=True, inplace=True)
    print(new_sales)
    exit()

    # print(sales['고객명'])
    customers = ['이민수', '최은주', '강소미', '성시연']
    extracted_customers = sales.loc[sales['고객명'].isin(customers), ['고객명', '수량', '판매금액', '순이익']]
    result = extracted_customers.groupby('고객명').agg(
        총매출액 = ("판매금액", "sum"),
        총순수익=("순이익", "mean"),
        총거래건수=("판매금액", "count")
    ).reset_index().round(2)
    print(result)
    # now = pd.Timestamp.now()
    # print(now)
    exit()

    product_count = sales.value_counts('제품명').reset_index()
    print(product_count)
    exit()

    product_total_count = pd.crosstab(
        sales['분류명'], sales['년도']
    )
    print(product_total_count)

    birthday = pd.to_datetime(sales["생년월일"]).dt.year
    today = pd.to_datetime(sales['날짜']).dt.year
    sales["나이"] = today - birthday
    sales['연령대'] = pd.cut(
        sales['나이'],
        bins=[0, 20, 30, 40, 50, 60, 200],
        labels=["10대", "20대", "30대", "40대", "50대", "60대이상"],
        include_lowest=True,
        right=False
    )
    ages_group = sales.groupby("연령대")["판매금액"].mean().reset_index().round(2)
    print(ages_group)
    exit()

    sales.loc[(sales["나이"] >= 0) & (sales["나이"] < 20), "연령대"] = "10대"
    sales.loc[(sales["나이"] >= 20) & (sales["나이"] < 30), "연령대"] = "20대"
    sales.loc[(sales["나이"] >= 30) & (sales["나이"] < 40), "연령대"] = "30대"
    sales.loc[(sales["나이"] >= 40) & (sales["나이"] < 50), "연령대"] = "40대"
    sales.loc[(sales["나이"] >= 50) & (sales["나이"] < 60), "연령대"] = "50대"
    sales.loc[sales["나이"] >= 60, "연령대"] = "60대이상"
    print(sales["연령대"])
    # sales.info()
    # print(sales.shape)
    # exit()
    # print(sales.describe())
