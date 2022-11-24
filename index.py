import os
import shutil

import pandas as pd
import numpy as np
import kmeans1d

# ordered by increasing values of clusters
# number of cluster names determines cluster count
CLUSTER_NAMES = [ 'lower', 'upper' ]

# skip indexing text columns with too many unique values
MAX_UNIQUE = 5

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
        # cluster numeric attributes
        if (df.dtypes[col] in ['int64', 'float64']):
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
        else:
            # categorize textual attributes
            column = df[col].str.lower().unique()
            values = np.sort(column)
            # skip if too many
            if len(values) > MAX_UNIQUE:
                print('Skipping index for column ' + col + ' because it has too many unique values')
                continue
            for value in values:
                formatted = value.replace(' ', '_')
                df.loc[df[col] == value].to_csv('indices/' + col + '_' + formatted + '.txt', columns = [], header = False)

    meta.to_csv('indices/_meta.csv', index_label = 'column')

    print('Finished processing')


clean_folder()
generate_indices()
