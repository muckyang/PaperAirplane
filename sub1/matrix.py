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
import numpy as np
from scipy.sparse import csr_matrix

def show_matrix(dataframes):
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    stores_user = stores_reviews.loc[:, ['store','user', 'score']]
    stores_group = stores_user.groupby(["store", "user"]).mean()
    print(stores_group)
    sdf = pd.SparseDataFrame(stores_group)
    print(sdf)
    print(sdf.head())

def main():
    warnings.filterwarnings(action='ignore')
    data = load_dataframes()
    show_matrix(data)
    show_matrix2(data)

def show_matrix2(dataframes):
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    stores_reviews = stores_reviews.loc[:,["user","category","score"]]
    print(stores_reviews)
    stores_reviews = (pd.concat( (stores_reviews.category.str.split('|', expand=True), 
                stores_reviews[['user','score']]),
            axis=1)
    .melt(id_vars=['user', 'score'], value_name='category')
    .dropna()       
    )   
    stores_reviews=stores_reviews.groupby(['user','category'],as_index = False).mean()
    stores_reviews = stores_reviews[stores_reviews.category !=""]
    # stores_reviews(stores_reviews['category'] !="")
    print(stores_reviews)
    # sdf = pd.SparseDataFrame(stores_reviews)
    # row = np.array(stores_reviews["category"])
    # col = np.array(stores_reviews["user"])
    # data = np.array(stores_reviews["score"])
    # # print(data)
    # sparse_coo = sparse.coo_matrix((data, (row,col)))

    # print(sparse_coo)

if __name__ == "__main__":
    main()