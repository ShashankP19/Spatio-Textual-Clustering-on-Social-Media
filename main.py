# from dbtexc import dbscan
from dbtexc.dbtexc import dbtexc
import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors

def get_f1_score(labels_rel, labels_irrel, num_clusters):
    
    # True Positive (TP): Number of POI-relevant points in clusters
    TP = len(labels_rel) - labels_rel.count(0)  
    
    # False Positive (FP): Number of POI-irrelevant points in clusters
    FP = len(labels_irrel) - labels_irrel.count(0)  

    # False Negative (FN): Number of POI-relevant points not in any cluster
    FN = labels_rel.count(0)
    
    # Precision: TP / (TP + FP)
    precision = TP / (TP + FP)

    # Recall: 
    recall = TP / (TP + FN)

    f1_score = 2 * (precision * recall) / (precision + recall)

    return f1_score



def main():
    # Read dataset from file

    relevant = pd.read_csv('HP_relevant.csv')
    # print(df.head(5))

    irrelevant = pd.read_csv('HP_irrelevant.csv')
    # print(df.head(5))

    # Get longitude and latitude columns from relevant tweets dataset
    ll_relevant = relevant[['longitude', 'latitude']]
    ll_relevant_values = ll_relevant.values
    # print(ll_relevant_values[:5])

    # Get longitude and latitude columns from irrelevant tweets dataset
    ll_irrelevant = irrelevant[['longitude', 'latitude']]
    ll_irrelevant_values = ll_irrelevant.values
    # print(ll_irrelevant_values[:5])

    # eps = 0.0001
    # N_min = 3
    # N_max = 5

    eps = 0.001
    N_min = 3
    N_max = 5
    clusters, labels_rel, labels_irrel = dbtexc(ll_relevant_values,
                      ll_irrelevant_values, eps, N_min, N_max)

    num_clusters = len(clusters)
    print("Number of Clusters: ", num_clusters)

    print("Length of Relevant tweets' classes: ", len(labels_rel))
    print("Relevant tweets' classes: ", labels_rel)

    print("Length of Irrelevant tweets' classes: ", len(labels_irrel))
    print("Irrelevant tweets' classes: ", labels_irrel)

    f1_score = get_f1_score(labels_rel, labels_irrel, num_clusters)
    print("F1-score: ", f1_score)

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    markersize = 2
    colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, len(clusters)))
    ax = world.plot(figsize=(20, 12), color='#e8e4b3')

    for cluster_id, cluster in enumerate(clusters):
        df = pd.DataFrame(cluster)
        geometry = [Point(p) for p in zip(df[0], df[1])]
        gdf = GeoDataFrame(df, geometry=geometry)
        gdf.plot(ax=ax, marker='o', color=mpl_colors.to_hex(
            colors[cluster_id]), markersize=markersize, label=('{} points'.format(len(cluster))))
    
    plt.axis('off')
    plt.legend(loc='best')
    plt.suptitle('DBTexC Clusters on Twitter Data', fontsize=16)
    plt.show()


if __name__ == "__main__":
    main()
