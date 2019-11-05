# from dbtexc import dbscan
from dbtexc.dbtexc import dbtexc
import pandas as pd

def main():
    # Read dataset from file

    relevant = pd.read_csv('relevant.csv')
    # print(df.head(5))

    irrelevant = pd.read_csv('irrelevant.csv')
    # print(df.head(5))

    # Get longitude and latitude columns from relevant tweets dataset
    ll_relevant = relevant[['longitude','latitude']]
    ll_relevant_values = ll_relevant.values
    print(ll_relevant_values[:5])

    # Get longitude and latitude columns from irrelevant tweets dataset
    ll_irrelevant = irrelevant[['longitude','latitude']]
    ll_irrelevant_values = ll_irrelevant.values
    print(ll_irrelevant_values[:5])

    eps = 1
    N_min = 5
    N_max = 10
    labels = dbtexc(ll_relevant_values, ll_irrelevant_values, eps, N_min, N_max)

    print(labels)
  
if __name__== "__main__":
    main()

