def aLift(cause, c_index, effect, e_index):
    # Read indices
    print('reading indices')
    file1 = open("indices/" + cause + "_" + c_index + ".txt", 'r')
    file2 = open("indices/" + effect + "_" + e_index + ".txt", 'r')

    # Find intersection of search spaces (linearly)
    print('finding intersection space')
    matches = 0
    matches_pos = 0
    line1 = file1.readline()
    line2 = file2.readline()
    while line1 and line2:
        if (line1 == line2):
            line1 = file1.readline()
            line2 = file2.readline()
            matches += 1
            matches_pos += 1
        elif (line1 < line2):
            line1 = file1.readline()
            matches += 1
        else:
            line2 = file2.readline()

    file1.close()
    file2.close()

    print('calculating aLift')
    total = meta.loc[effect].lower + meta.loc[effect].upper
    prob_total = meta.loc[effect][e_index] / total
    prob_match = matches_pos / matches
    aLift = prob_match - prob_total

    print(prob_match, prob_total, aLift, matches, matches_pos)
    print(cause + " -> " + effect + " " + str(aLift))
