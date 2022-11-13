import pandas as pd

ARG1 = "normaldist"
ARG2 = "normaldist1"

meta = pd.read_csv('indices/_meta.csv', index_col = 'column')

def correlation(col1, col2):
    print('reading table')
    df = pd.read_csv('dummy_data.csv')
    print('calculating correlation')
    corr = df[col1].corr(df[col2], method = 'pearson')
    print(corr)

def aLift(cause, c_index, effect, e_index):
    total = meta.loc[effect].lower + meta.loc[effect].upper
    current = 0
    matches = 0
    matches_pos = 0

    # Read indices
    print('reading indices')
    file1 = open("indices/" + cause + "_" + c_index + ".csv", 'r')
    file2 = open("indices/" + effect + "_" + e_index + ".csv", 'r')

    # Find intersection of search spaces (linearly)
    print('finding intersection space')
    line1 = file1.readline()
    line2 = file2.readline()

    while line1 and line2:
        id1 = line1.strip().split(',')[0]
        id2 = line2.strip().split(',')[0]
        if (id1 == id2):
            line1 = file1.readline()
            line2 = file2.readline()
            matches += 1
            matches_pos += 1
        elif (id1 < id2):
            line1 = file1.readline()
            matches += 1
        else:
            line2 = file2.readline()

    file1.close()
    file2.close()

    print('calculating aLift')
    prob_total = meta.loc[effect][e_index] / total
    prob_match = matches_pos / matches
    aLift = prob_match - prob_total

    print(prob_match, prob_total, aLift, matches, matches_pos)
    print(cause + " -> " + effect + " " + str(aLift))

correlation(ARG1, ARG2)
aLift(ARG1, 'upper', ARG2, 'upper')
