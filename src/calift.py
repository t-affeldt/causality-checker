def caLift(cause, effect, *contexts):
    counter = match(cause, effect, *contexts)
    results = [ 0 ] * len(contexts)
    for i in range(0, len(contexts)):
        total = counter['contexts'][i]
        total_ctx = meta.loc[contexts[i].split('_')[0]][contexts[i].split('_')[1]]
        pos = counter['contexts_pos'][i]
        p_match = pos / total
        p_neutral = counter['contexts_base'][i] / total_ctx
        results[i] = p_match - p_neutral
    return results
