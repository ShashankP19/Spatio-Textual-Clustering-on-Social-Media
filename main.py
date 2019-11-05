# from dbtexc import dbscan
from dbtexc.dbtexc import dbtexc
import pandas as pd

def main():
    # Read dataset from file

    df = pd.read_csv('dataset.csv')
    # print(df.head(5))

    ll_df = df[['longitude','latitude']]
    ll_df_values = ll_df.values
    print(ll_df_values[:5])

    labels = dbtexc(ll_df_values, 2, 10)

    print(labels)
  
if __name__== "__main__":
    main()

