# from dbtexc import dbscan
from dbtexc.dbtexc import dbtexc
import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt


def main():
    # Read dataset from file

    relevant = pd.read_csv('relevant.csv')
    # print(df.head(5))

    irrelevant = pd.read_csv('irrelevant.csv')
    # print(df.head(5))

    # Get longitude and latitude columns from relevant tweets dataset
    ll_relevant = relevant[['longitude', 'latitude']]
    ll_relevant_values = ll_relevant.values
    # print(ll_relevant_values[:5])

    # Get longitude and latitude columns from irrelevant tweets dataset
    ll_irrelevant = irrelevant[['longitude', 'latitude']]
    ll_irrelevant_values = ll_irrelevant.values
    # print(ll_irrelevant_values[:5])

    eps = 1
    N_min = 5
    N_max = 10
    clusters = dbtexc(ll_relevant_values,
                      ll_irrelevant_values, eps, N_min, N_max)


    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    markersize = 15
    ax = world.plot(figsize=(10, 6))
    colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, len(clusters)))
    print(colors)
    print(len(clusters))
    for cluster_id, cluster in enumerate(clusters):
        df = pd.DataFrame(cluster)
        geometry = [Point(p) for p in zip(df[0], df[1])]
        gdf = GeoDataFrame(df, geometry=geometry)
        gdf.plot(ax=ax, marker='o', color=colors[cluster_id], markersize=markersize)
                
    # df = pd.read_csv("dataset.csv", delimiter=',',
    #                  skiprows=0, low_memory=False)

    # geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    # gdf = GeoDataFrame(df, geometry=geometry)

    plt.show()


if __name__ == "__main__":
    main()
