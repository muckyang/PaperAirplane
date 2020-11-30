
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from konlpy.utils import pprint
from parse import load_dataframes
import pandas as pd
from pandas import Series, DataFrame
import scipy.sparse
import sqlite3

mydoclist=[]

data = load_dataframes()

stores_reviews = data["stores"].head(100000)
# indexD = stores_reviews[stores_reviews["menu"]==""].index
# droped = stores_reviews.drop(indexD)
for i, Each_row in stores_reviews.iterrows():
    mydoclist.append(Each_row['menu'])

okt = Okt()

doc_nouns_list = []
count=0
for doc in mydoclist:
    count += 1
    if count==50000:
        break
    nouns = okt.nouns(doc)
    doc_nouns = ''

    for noun in nouns:
        doc_nouns += noun + ' '
    doc_nouns_list.append(doc_nouns)

tfidf_vectorizer = TfidfVectorizer(min_df=1)
tfidf_matrix = tfidf_vectorizer.fit_transform(doc_nouns_list)

document_distances = (tfidf_matrix * tfidf_matrix.T)
# print(document_distances)
# document_distances를 sparse matrix 화 시켜서 이차원 배열에 value가 있는 값으로 전환
first = pd.DataFrame.sparse.from_spmatrix(document_distances)
# raw_data -> dataframe 컬럼을 만들어 놓음
raw_data = {'selected_store': [], 'recommended_store': [], 'similarity' : []}
# raw_data 컬럼을 넣음
recommendAuto = DataFrame(raw_data)
# print(first)

# store 전체를 비교할 것이라서 인덱스 0부터 시작하기 때문에 찾을 때에는 1씩 인덱스 올려서 찾으면 됨
for index in range(0, first[0].size):
    # 다 정제가 되었으면 이제 내림차순으로 각각 store를 행별로 정렬 관련된 상위 6개만 일단 뽑아옴(6개 추천해준다는 뜻임)
    second = first[index].sort_values(ascending=False).head(6)
    for index2 in range(0, 6):
        # if문은 print 찍어 보면 keys()랑 values 부분 이해가 갈거임
        if second.values[index2] < 0.99 and second.values[index2] > 0:
            new_row = {'selected_store':index, 'recommended_store':second.keys()[index2], 'similarity':second.values[index2]}
            recommendAuto = recommendAuto.append(new_row, ignore_index=True)

# sqlite에 넣음
# con = sqlite3.connect("/home/ubuntu/bigdata/s03p23b303/sub2/backend/db.sqlite3")
con = sqlite3.connect("../sub2/backend/db.sqlite3")
# test9는 테이블 이름
recommendAuto.to_sql('api_collabormenu', con, if_exists='append')
print("finish")