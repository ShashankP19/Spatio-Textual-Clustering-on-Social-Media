from dbtexc.dbscan import dbscan
from dbtexc.dbtexc import dbtexc
import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import sys

eps = 0.01
N_min = 4
N_max = 8

markersize = 5
min_points = 6
algo_name = ['DBTexC', 'DBScan']

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


def main_dbscan():
    # data = pd.read_csv('dataset.csv')
    
    relevant_df = pd.read_csv('relevant.csv')
    # print(df.head(5))

    irrelevant_df = pd.read_csv('irrelevant.csv')
    # print(df.head(5))

    is_relevant = [True] * relevant_df.shape[0] + [False] * irrelevant_df.shape[0]

    data = pd.concat([relevant_df, irrelevant_df], ignore_index=True, sort =False)
    data['is_relevant'] = is_relevant
    
    data_points = data[['longitude', 'latitude']].values

    clusters, labels = dbscan(data_points, eps, min_points)

    # print(len(labels))
    # for i in range(len(labels)):
    #     print(labels[i])

    labels_rel = []
    labels_irrel = []

    for i in range(len(labels)):
        if(data['is_relevant'][i] == True):
            labels_rel.append(labels[i])
        else:
            labels_irrel.append(labels[i]) 

    num_clusters = len(clusters)
    print("Number of Clusters: ", num_clusters)

    print("Length of Relevant tweets' classes: ", len(labels_rel))
    print("Relevant tweets' classes: ", labels_rel)

    print("Length of Irrelevant tweets' classes: ", len(labels_irrel))
    print("Irrelevant tweets' classes: ", labels_irrel)

    f1_score = get_f1_score(labels_rel, labels_irrel, num_clusters)
    print("F1-score: ", f1_score)

    plot_clusters(clusters, 1)


def main_dbtexc():
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

    plot_clusters(clusters, 0)


def plot_clusters(clusters, algo):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, len(clusters)))
    ax = world.plot(figsize=(20, 12), color='#e8e4b3')
    # print(clusters)
    # print(len(clusters))

    # Restrict to Europe
    # ax = world[world.continent == 'Europe'].plot(color='white', edgecolor='black', figsize=(20, 12))
    for cluster_id, cluster in enumerate(clusters):
        df = pd.DataFrame(cluster)
        geometry = [Point(p) for p in zip(df[0], df[1])]
        gdf = GeoDataFrame(df, geometry=geometry)
        # print(gdf.head())
        gdf.plot(ax=ax, marker='o', color=mpl_colors.to_hex(
            colors[cluster_id]), markersize=markersize, label=('{} points'.format(len(cluster))))

    plt.axis('off')
    plt.legend(loc='best')
    plt.suptitle('{} Clusters on Twitter Data'.format(
        algo_name[algo]), fontsize=16)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 main.py <algo_id>')
        for id, algo in enumerate(algo_name):
            print(id, algo)
    else:
        if sys.argv[1] == '0':
            main_dbtexc()
        elif(sys.argv[1] == '1'):
            main_dbscan()
