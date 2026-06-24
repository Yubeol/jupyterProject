import pandas as pd




if __name__ == '__main__':
    sales = pd.read_excel('./data/Sales.xlsx')
    details = pd.read_excel('./data/Details.xlsx', sheet_name=None)
    regions = details['지역']
    promotions = details['프로모션']
    channels = details["채널"]
    customers = details["2018년도~2022년도 주문고객"]
    products = details["제품"]
    product_categories = details["제품분류"]
    categories = details["분류"]
    date = details["날짜"]

    merged_sales = pd.merge(sales, products, on='제품코드', how='left')
    merged_sales = pd.merge(merged_sales, product_categories, on='제품분류코드', how='left')
    merged_sales = pd.merge(merged_sales, categories, on='분류코드', how='left')
    merged_sales = pd.merge(merged_sales, customers, on='고객코드', how='left')
    merged_sales = pd.merge(merged_sales, regions, on='지역코드', how='left')
    merged_sales = pd.merge(merged_sales, promotions, on='프로모션코드', how='left')
    merged_sales = pd.merge(merged_sales, channels, on='채널코드', how='left')
    merged_sales = pd.merge(merged_sales, date, on='날짜', how='left')
    merged_sales = merged_sales[['날짜', '제품코드', '고객코드', '프로모션코드', '채널코드', 'Quantity', 'UnitPrice', '지역_x',
       '제품명', '색상', '원가', '단가', '제품분류코드', '제품분류명', '분류코드', '분류명', '지역코드',
       '고객명', '성별', '생년월일', '시도', '구군시', '지역_y', '프로모션', '할인율', '채널명', '날짜코드',
       '년도', '분기', '월(No)', '월(영문)']]
    merged_sales.rename(columns={"지역_x":"지역", "Quantity": "수량"}, inplace=True)

    merged_sales.to_pickle('./data/merged_sales.pkl')
    print(merged_sales.keys())
    exit()

    details = pd.read_excel('./data/Details.xlsx', sheet_name=None)

    matrix = details['제품'].values
    print(matrix)
    exit()
    products = details['제품']
    result = products.loc[products['단가']>=50000, '제품명']
    print(result)
    exit()


    sales = pd.read_excel('./data/Sales.xlsx')
    sales['판매가격'] = sales['Quantity'] * sales['UnitPrice']
    seoul_region = sales.loc[(sales['지역'] == '서울') & (sales['판매가격'] >= 100000), :]
    print(seoul_region)
    exit()
    details = pd.read_excel('./data/Details.xlsx', sheet_name=None)
    print(details.keys())
    regions = details['지역']
    print(regions)