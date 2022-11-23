import os
import shutil

import pandas as pd
import kmeans1d

# ordered by increasing values of clusters
# number of cluster names determines cluster count
CLUSTER_NAMES = [ 'lower', 'upper' ]

def clean_folder():
    for root, dirs, files in os.walk('./indices'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def generate_indices():
    cluster_count = len(CLUSTER_NAMES)
    print('Reading table')
    df = pd.read_csv('dummy_data.csv', index_col = False)

    meta = pd.DataFrame(dict(zip(CLUSTER_NAMES, [[]] * cluster_count)))

    for col in df.columns:
        print('processing column ' + col)
        # skip if not numeric
        if (not df.dtypes[col] in ['int64', 'float64']):
            continue
        data = df[col].to_numpy()
        clusters, centroids = kmeans1d.cluster(data, cluster_count)

        # store index in text files
        s = pd.Series(clusters)
        counter = [0] * cluster_count
        for i in range(0, cluster_count):
            selection = s[s == i]
            counter[i] = selection.size
            selection.to_csv('indices/' + col + '_' + CLUSTER_NAMES[i] +'.txt', columns = [], header = False)
        meta.loc[col] = counter

    meta.to_csv('indices/_meta.csv', index_label = 'column')

    print('Finished processing')


clean_folder()
generate_indices()
