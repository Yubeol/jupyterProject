import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    merged_sales = pd.read_pickle('./data/merged_sales.pkl')
    merged_sales['순이익'] = (
            merged_sales["수량"] *
                (merged_sales['단가']*(1-merged_sales['할인율']) - merged_sales['원가'])
    )
    merged_sales['판매금액'] = (
            merged_sales["수량"] *
            (merged_sales['단가'] * (1 - merged_sales['할인율']))
    )
    result = pd.pivot_table(
        merged_sales,
        index=["분류명"],
        columns=['년도'],
        values='순이익',
        aggfunc= sum,
        fill_value=0
    )

    sns.heatmap(
        result,
        annot=True,
        fmt=".0f",
        cmap="YlGnBu",
    )
    plt.show()
    # print(result)
    exit()
    # print(merged_sales.keys())
    # exit()
    result = merged_sales.groupby(['분류명', "제품분류명", '제품명']).agg(
        총매출액 = ("판매금액", "mean"),
        총순이익 = ('순이익', 'mean'),
        총수량 = ("수량", "sum")
    ).reset_index().round(2)

    # 한글 설정
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    # 총매출액 TOP 10
    top10 = (
        result.sort_values("총매출액", ascending=False)
        .head(10)
        .sort_values("총매출액")  # 가로막대용 정렬
    )

    plt.figure(figsize=(12, 6))

    bars = plt.barh(
        top10["제품명"],
        top10["총매출액"]
    )

    plt.title("총매출액 TOP 10 제품")
    plt.xlabel("총매출액")
    plt.ylabel("제품명")

    # 값 표시
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width,
            bar.get_y() + bar.get_height() / 2,
            f"{width:,.0f}",
            va="center",
            ha="left"
        )

    plt.tight_layout()
    plt.show()