import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 1. 데이터 로드 (딱 1번만)
    merged_sales = pd.read_pickle('./data/merged_sales.pkl')

    # 2. 파생 컬럼 계산
    merged_sales['순이익'] = (
        merged_sales['수량'] *
        (merged_sales['단가'] * (1 - merged_sales['할인율']) - merged_sales['원가'])
    )
    merged_sales['판매금액'] = (
        merged_sales['수량'] *
        (merged_sales['단가'] * (1 - merged_sales['할인율']))
    )

    result = pd.pivot_table(
        merged_sales,
        index=["분류명", "제품분류명", "제품명"],
        columns=['년도', '분기', '월(영문)'],
        values='순이익',
        aggfunc=sum,
        fill_value=0
    )

    print(result)
    exit()

    # 3. 그룹별 집계 (딱 1번만)
    result = merged_sales.groupby(['분류명', '제품분류명', '제품명']).agg(
        총매출액=('판매금액', 'mean'),
        총순이익=('순이익', 'mean'),
        총수량=('수량', 'sum')
    ).reset_index().round(2)

    # 4. 한글 깨짐 방지
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # 5. 총매출액 기준 상위 10개 추출
    top10 = result.sort_values('총매출액', ascending=False).head(10)

    # 6. 가로 막대 그래프 (큰 값이 위로 오도록 순서 뒤집기)
    top10 = top10.iloc[::-1]   # 1위가 그래프 맨 위에 보이도록 순서 반전

    plt.figure(figsize=(10, 8))
    bars = plt.barh(top10['제품명'], top10['총매출액'], color='steelblue')

    plt.title('제품별 총매출액 TOP 10', fontsize=14)
    plt.xlabel('총매출액')
    plt.ylabel('제품명')

    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2,
                  f'{width:,.0f}', ha='left', va='center', fontsize=9)

    plt.tight_layout()
    plt.show()