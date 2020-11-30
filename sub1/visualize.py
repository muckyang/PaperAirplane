import itertools
from collections import Counter
from parse import load_dataframes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
import warnings
import datetime


def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

    sns.set_palette(sns.color_palette("Spectral"))
    plt.rc("xtick", labelsize=6)


def show_store_categories_graph(dataframes, n=100):
    """
    Tutorial: 전체 음식점의 상위 `n`개 카테고리 분포를 그래프로 나타냅니다.
    """

    stores = dataframes["stores"]

    # 모든 카테고리를 1차원 리스트에 저장합니다
    categories = stores.category.apply(lambda c: c.split("|"))
    categories = itertools.chain.from_iterable(categories)

    # 카테고리가 없는 경우 / 상위 카테고리를 추출합니다
    categories = filter(lambda c: c != "", categories)
    categories_count = Counter(list(categories))
    
    best_categories = categories_count.most_common(n=n)
    df = pd.DataFrame(best_categories, columns=["category", "count"]).sort_values(
        by=["count"], ascending=False
    )

    # 그래프로 나타냅니다
    chart = sns.barplot(x="category", y="count", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점 카테고리 분포")
    plt.show()

def show_store_review_distribution_graph(dataframes):
    """
    Req. 1-3-1 전체 음식점의 리뷰 개수 분포를 그래프로 나타냅니다. 
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )

    # 모든 음식점을 1차원 리스트에 저장합니다
    stores = stores_reviews.store_name.apply(lambda c: c.split(" "))
    stores = itertools.chain.from_iterable(stores)
    
    # 음식점의 개수 추출합니다
    stores = filter(lambda c: c != "", stores)
    stores_count = Counter(list(stores))
    # print(stores_count)

    best_stores = stores_count.most_common()
    df = pd.DataFrame(best_stores, columns=["store_num", "count"]).sort_values(
        by=["count"], ascending=False
    )

    count_group = df.groupby(by=["count"], as_index=False).count()
    print(count_group)

    # 그래프로 나타냅니다
    chart = sns.scatterplot( x="count",y="store_num", data=count_group)
    chart.set_xticklabels([-30,0,100,200,300,400,500,600])
    plt.title("음식점 리뷰 개수 분포")
    plt.xlabel('리뷰 수')
    plt.ylabel('음식점 수')
    plt.axis([-30,600,-900,7000])
    plt.show()

def show_store_average_ratings_graph(dataframes, n=100):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    # x축 음식점, y축 평균평점

    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )

    scores_group = stores_reviews.groupby(["store", "store_name"])
    review_counts = scores_group["score"].agg({"rcount":"count"})
    scores = scores_group.mean()

    # print(scores)

    df = scores.head(n=n).reset_index()
    
    # 그래프로 나타냅니다
    chart =sns.barplot(x="store_name", y="score", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점별 평균 평점")
    plt.xlabel('음식점')
    plt.ylabel('평균평점')
    plt.ylim(0,6)
    plt.show()

def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    stores_reviews = dataframes["reviews"]

    # 모든 리뷰의 유저를 1차원 리스트에 저장합니다
    users = stores_reviews.user

    # 유저가 없는 경우 / 상위 유저를 추출합니다
    users_review_count = Counter(list(users))

    users_review_count = users_review_count.most_common()
    df = pd.DataFrame(users_review_count, columns=["user", "num"]).sort_values(
        by=["num"], ascending=False
    )

    count_group = df.groupby(by=["num"], as_index=False).count()


    # 그래프로 나타냅니다
    chart = sns.pointplot(x="num", y="user", data=count_group)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("유저별 리뷰 개수 분포")
    chart.set_xlabel('reviewCount')
    chart.set_ylabel('userCount')
    plt.show()

def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    reviews = dataframes["reviews"]
    genders_ages = reviews.filter(["gender","born_year"])
    # print(genders_ages)

    # born_year는 기본 자료형이 Object라서 int형으로 바꾸어주어야 연령대 계산 가능
    genders_ages[["born_year"]] = genders_ages[["born_year"]].apply(pd.to_numeric)
    genders_ages["age"] = (datetime.datetime.now().year - genders_ages["born_year"]+1) // 10 * 10
    # 10대부터 70대까지 자료를 보여줌
    genders_ages = genders_ages[genders_ages['age'] > 0]
    genders_ages = genders_ages[genders_ages['age'] < 80]
    # print(genders_ages)
    # print(genders_ages.dtypes)
    # print("--------------------")
    # 정제중 누락된 데이터가 있는지 확인
    # print(genders_ages.isna().sum())
    # print("--------------------")
    # print(genders_ages)

    # 정제 후 겹치는 데이터 없앤 후 카운드해서 가져옴
    genders_ages = genders_ages.groupby(["gender", "age"], as_index=False).count()
    # print(genders_ages)
    # born_year에 카운팅된 수가 들어갔기 때문에 컬럼명 알아볼 수 있게 조정
    genders_ages = genders_ages.rename(columns={'born_year': 'counting'})
    # print(genders_ages)
    # 데이터를 피보팅함
    genders_ages = genders_ages.pivot("age", "gender", "counting")
    # print(genders_ages)

    # 인덱스 이름 바까주고
    index_after = {}
    for i in list(genders_ages.index):
        index_after[i] = "%d대" % i
    # print(index_after)

    genders_ages.rename(index=index_after, inplace=True)
    # print(genders_ages)

    # 데이터 시각화
    genders_ages.plot.bar(rot=0)
    plt.title('성별과 연령대별 분포')
    plt.grid()
    plt.xlabel('연령대')
    plt.ylabel('명')

    plt.show()

def show_stores_distribution_graph(dataframes):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """
    stores = dataframes["stores"]

    map_osm = folium.Map(location=[36.086621, 128.084844], zoom_start=7)
    for i in stores.index:
        if i == 500 : break
        # 행 우선 접근 방식으로 값 추출하기
        lat = stores.loc[i, 'latitude']
        lng = stores.loc[i, 'longitude']
        store_name = stores.loc[i, 'store_name']

        # 추출한 정보를 지도에 표시
        marker = folium.Marker([lat,lng], popup=store_name)
        marker.add_to(map_osm)

    map_osm.save('test.html')
    map_osm

def main():
    warnings.filterwarnings(action='ignore')
    set_config() 
    data = load_dataframes()
    show_store_categories_graph(data) #0번째
    show_store_review_distribution_graph(data) #1번째 - 음식점별 리뷰 개수 분포
    show_store_average_ratings_graph(data) #2번째 - 음식점별 평균 평점
    show_user_review_distribution_graph(data) #3번째 - 전체 유저별 리뷰 개수 분포
    show_user_age_gender_distribution_graph(data) #4번째 - 연령, 성별 기준 리뷰 분포
    show_stores_distribution_graph(data) #5번째 - 음식점 위치 분포


if __name__ == "__main__":
    main()
