def correlation(col1, col2):
    print('reading table')
    df = pd.read_csv('dummy_data.csv')
    print('calculating correlation')
    corr = df[col1].corr(df[col2], method = 'pearson')
    return corr
