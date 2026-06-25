import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://kogo:123@localhost:5432/mydb')

if __name__ == "__main__":
    sales = pd.read_excel('./data/Sales.xlsx')
    details = pd.read_excel('./data/Details.xlsx', sheet_name=None)
    regions = details['지역']
    promotions = details['프로모션']
    channels = details["채널"]
    customers = details["2018년도~2022년도 주문고객"]
    products = details["제품"]
    product_categories = details["제품분류"]
    categories = details["분류"]

    # 0) 기존 테이블 정리 (참조하는 테이블부터 역순으로 삭제)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS sales CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS customers CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS products CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS product_categories CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS categories CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS regions CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS promotions CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS channels CASCADE;"))

    # 1) categories
    categories.rename(
        columns={
            "분류코드": "id",
            "분류명": "category_name"
        },
        inplace=True
    )
    categories.to_sql("categories", engine, index=False, if_exists='replace')

    # 2) product_categories
    product_categories.rename(
        columns={
            "제품분류코드": "id",
            "제품분류명": "product_category_name",
            "분류코드": "category_id"
        },
        inplace=True
    )
    product_categories.to_sql(
        "product_categories", engine, index=False, if_exists='replace'
    )

    # 3) products
    products.rename(
        columns={
            "제품코드": "id",
            "제품명": "product_name",
            "색상": "color",
            "원가": "price",
            "단가": "sale_price",
            "제품분류코드": "product_category_id"
        },
        inplace=True
    )
    products.to_sql(
        "products",
        engine,
        index=False,
        if_exists="replace",
    )

    # 4) promotions
    promotions.rename(
        columns={
            "프로모션코드": "id",
            "프로모션": "promotion_name",
            "할인율": "discount_rate"
        },
        inplace=True
    )
    promotions.to_sql(
        "promotions",
        engine,
        index=False,
        if_exists="replace",
    )

    # 5) regions
    regions.rename(
        columns={
            '지역코드': "id",
            '시도': "province",
            '구군시': 'city_district',
            '지역': 'region_name',
        },
        inplace=True
    )
    regions.to_sql(
        "regions",
        engine,
        index=False,
        if_exists="replace",
    )

    # 6) channels
    channels.rename(
        columns={
            "채널코드": "id",
            "채널명": "channel_name",
        },
        inplace=True
    )
    channels.to_sql(
        "channels",
        engine,
        index=False,
        if_exists="replace",
    )

    # 7) customers
    customers.rename(
        columns={
            '고객코드': "id",
            "지역코드": "region_id",
            "고객명": "customer_name",
            "성별": "gender",
            "생년월일": "birth_date",
        },
        inplace=True
    )
    customers.to_sql(
        "customers",
        engine,
        index=False,
        if_exists="replace",
    )

    # 8) sales
    #    참고: 지역 정보는 sales.customer_id -> customers.region_id -> regions 로
    #    이미 추적 가능하므로, sales에 region_id를 따로 두지 않고 '지역' 컬럼은 제거함

    # 8-1) 컬럼명 정리 (날짜는 값 그대로 둠, dates 테이블과 연결하지 않음)
    sales.rename(
        columns={
            "날짜": "date",
            "제품코드": "product_id",
            "고객코드": "customer_id",
            "프로모션코드": "promotion_id",
            "채널코드": "channel_id",
            "Quantity": "quantity",
        },
        inplace=True
    )

    # 8-2) UnitPrice, 지역 컬럼 제거
    #      UnitPrice -> products.sale_price 와 중복
    #      지역 -> customers.region_id (-> regions) 경로로 이미 추적 가능하므로 중복
    # sales.drop(columns=["UnitPrice", "지역"], inplace=True)

    sales.to_sql(
        "sales",
        engine,
        index=False,
        if_exists="replace",
    )

    # 9) PK / FK 제약은 한곳에 모아서 일괄 실행
    #    (테이블 생성 순서를 따라가도록 정렬: 참조 대상 -> 참조하는 쪽)
    constraints = [
        "ALTER TABLE categories ADD PRIMARY KEY (id);",

        "ALTER TABLE product_categories ADD PRIMARY KEY (id);",
        "ALTER TABLE product_categories ADD FOREIGN KEY (category_id) REFERENCES categories (id);",

        "ALTER TABLE products ADD PRIMARY KEY (id);",
        "ALTER TABLE products ADD FOREIGN KEY (product_category_id) REFERENCES product_categories (id);",

        "ALTER TABLE promotions ADD PRIMARY KEY (id);",

        "ALTER TABLE regions ADD PRIMARY KEY (id);",

        "ALTER TABLE channels ADD PRIMARY KEY (id);",

        "ALTER TABLE customers ADD PRIMARY KEY (id);",
        "ALTER TABLE customers ADD FOREIGN KEY (region_id) REFERENCES regions (id);",

        "ALTER TABLE sales ADD COLUMN id SERIAL PRIMARY KEY;",
        "ALTER TABLE sales ADD FOREIGN KEY (product_id) REFERENCES products (id);",
        "ALTER TABLE sales ADD FOREIGN KEY (customer_id) REFERENCES customers (id);",
        "ALTER TABLE sales ADD FOREIGN KEY (promotion_id) REFERENCES promotions (id);",
        "ALTER TABLE sales ADD FOREIGN KEY (channel_id) REFERENCES channels (id);",
    ]

    with engine.begin() as conn:
        for statement in constraints:
            conn.execute(text(statement))

    exit()