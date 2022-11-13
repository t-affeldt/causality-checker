import pandas as pd
import kmeans1d

print('Reading table')
df = pd.read_csv('dummy_data.csv')

meta = pd.DataFrame({
    'lower': [],
    'upper': []
})

for col in df.columns:
    print('processing column ' + col)
    # skip if not numeric
    if (not df.dtypes[col] in ['int64', 'float64']):
        continue
    # split on median
    divider = df[col].median()

    lower = df[col][df[col] < divider]
    lower.to_csv(path_or_buf = "./indices/" + col + "_lower.csv", header = False)
    lower_count = lower.shape[0]

    upper = df[col][df[col] >= divider]
    upper.to_csv(path_or_buf = "./indices/" + col + "_upper.csv", header = False)
    upper_count = upper.shape[0]

    meta.loc[col] = [ lower_count, upper_count ]

meta.to_csv(path_or_buf = "./indices/_meta.csv", index_label = 'column')

print('Finished processing')
