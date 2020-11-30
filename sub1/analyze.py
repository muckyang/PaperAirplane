from parse import load_dataframes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shutil
import warnings
import nltk
from numpy import dot
from numpy.linalg import norm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds

def sort_stores_by_score(dataframes, n=20, min_reviews=30):
    """
    Req. 1-2-1 각 음식점의 평균 평점을 계산하여 높은 평점의 음식점 순으로 `n`개의 음식점을 정렬하여 리턴합니다
    Req. 1-2-2 리뷰 개수가 `min_reviews` 미만인 음식점은 제외합니다.
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    scores_group = stores_reviews.groupby(["store", "store_name"])
    review_counts = scores_group["score"].agg({"rcount":"count"})
    scores = scores_group.mean()
    scores = scores[review_counts['rcount']>min_reviews]
    return scores.sort_values(by="score", ascending=False).head(n=n).reset_index()


def get_most_reviewed_stores(dataframes, n=20):
    """
    Req. 1-2-3 가장 많은 리뷰를 받은 `n`개의 음식점을 정렬하여 리턴합니다
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )

    review_group = stores_reviews.groupby(["store", "store_name"])
    review_counts = review_group["score"].agg({"rcount":"count"})

    return review_counts.sort_values(by="rcount", ascending=False).head(n=n).reset_index()


def get_most_active_users(dataframes, n=20):
    """
    Req. 1-2-4 가장 많은 리뷰를 작성한 `n`명의 유저를 정렬하여 리턴합니다.
    """
    
    stores_reviews = dataframes["reviews"]
    review_user = stores_reviews.groupby(["user"])
    review_counts = review_user["user"].agg({"rcount":"count"})

    return review_counts.sort_values(by="rcount", ascending=False).head(n=n).reset_index()

  
def recommend_movies(df_svd_preds, user, ori_movies_df, ori_ratings_df, num_recommendations=5):
    
   
    #현재는 index로 적용이 되어있으므로 user_id - 1을 해야함.
    user_row_number = user - 1
   
    # 최종적으로 만든 pred_df에서 사용자 index에 따라 영화 데이터 정렬 -> 영화 평점이 높은 순으로 정렬 됌
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)

    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다. 
    user_data = ori_ratings_df[ori_ratings_df.user == user]
    # print(2222)
    # print(user_data)
  
    # 위에서 뽑은 user_data와 원본 영화 데이터를 합친다. 
    user_history = user_data.merge(ori_movies_df, on = 'store').sort_values(['score_x'], ascending=False)
    # print(2222)
    
    # # 원본 영화 데이터에서 사용자가 본 영화 데이터를 제외한 데이터를 추출
    recommendations = ori_movies_df[~ori_movies_df['store'].isin(user_history['store'])]
  
    # 사용자의 영화 평점이 높은 순으로 정렬된 데이터와 위 recommendations을 합친다. 
    recommendations = recommendations.merge( pd.DataFrame(sorted_user_predictions).reset_index(), on = 'store')
 
    # 컬럼 이름 바꾸고 정렬해서 return
    recommendations = recommendations.rename(columns = {user_row_number: 'Predictions'}).sort_values('Predictions', ascending = False).iloc[:num_recommendations, :]
    
    print(recommendations.groupby(['store']).mean())
    # print(232232323232323233) 
    # a = recommendations.groupby(["store"])          
    # print(a)
    return user_history, recommendations

def main():
    
    # get_recommend_movies(df_svd_preds, 511, user_reviews,df_user_store_ratings)

    warnings.filterwarnings(action='ignore')
    data = load_dataframes()
    # print(data)
    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w
        
    stores_most_scored = sort_stores_by_score(data)
    stores_mostCount_review = get_most_reviewed_stores(data)
    stores_mostCount_user = get_most_active_users(data)
    
    
    user_reviews = data["reviews"].head(10000)
    user_stores = data["stores"].head(10000)
    # ur = user_reviews[['user','store','score']]
    df_user_store_ratings = user_reviews.pivot(index='user',columns='store',values='score').fillna(0)
    # print(df_user_store_ratings.head())
    # matrix는 pivot_table 값을 numpy matrix로 만든 것 
    
    matrix = df_user_store_ratings.as_matrix()

    # user_ratings_mean은 사용자의 평균 평점 
    user_ratings_mean = np.mean(matrix, axis = 1)

    # R_user_mean : 사용자-영화에 대해 사용자 평균 평점을 뺀 것.
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)
    # print(df_user_store_ratings)
    
    pd.DataFrame(matrix_user_mean, columns = df_user_store_ratings.columns).head()
    
    U, sigma, Vt = svds(matrix_user_mean, k = 12)
    sigma = np.diag(sigma)
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = df_user_store_ratings.columns)
  
    # print(df_svd_preds)
    recommend_movies(df_svd_preds, 3019, user_reviews, user_reviews, 100)

    print("[최고 평점 음식점]")
    print(f"{separater}\n")
    for i, store in stores_most_scored.iterrows():
        print(
            "{rank}위: {store}({score}점)".format(
                rank=i + 1, store=store.store_name, score=store.score
            )
        )
    print(f"\n{separater}\n\n")

    print("[최다 리뷰 음식점]")
    print(f"{separater}\n")
    for i, store in stores_mostCount_review.iterrows():
        print(
            "{rank}위: {store}({counts}개)".format(
                rank=i + 1, store=store.store_name, counts=store.rcount
            )
        )
    print(f"\n{separater}\n\n")

    print("[최다 리뷰 작성자]")
    print(f"{separater}\n")
    for i, review in stores_mostCount_user.iterrows():
        print(
            "{rank}위: {review}({counts}개)".format(
                rank=i + 1, review=review.user, counts=review.rcount
            )
        )
    print(f"\n{separater}\n\n")



if __name__ == "__main__":
    main()
    
    