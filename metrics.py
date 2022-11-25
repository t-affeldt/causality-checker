import pandas as pd
import math

TABLENAME = "dummy_data"
ARG1 = "normaldist"
ARG2 = "normaldist1"

meta = pd.read_csv('indices/' + TABLENAME + '/_meta.csv', index_col = 'column')

def match(cause_index, effect_index, *ctx_indices):

    def next_entry(file):
        line = file.readline()
        if not line:
            return math.inf
        return int(line)

    files = {
        'cause': open('indices/' + TABLENAME + '/' + cause_index + '.txt', 'r'),
        'effect': open('indices/' + TABLENAME + '/' + effect_index + '.txt', 'r'),
        'contexts': list(map(lambda index: open('indices/' + TABLENAME + '/' + index + '.txt', 'r'), ctx_indices))
    }

    lines = {
        'cause': next_entry(files['cause']),
        'effect': -1,
        'contexts': [ -1 ] * len(ctx_indices)
    }

    # Cause F, Effect E, Context C
    counter = {
        'cause': 0, # |F|
        'effect': 0, # |F INTERSECT E|
        'contexts': [0] * len(files['contexts']), # |F INTERSECT C|
        'contexts_pos': [0] * len(files['contexts']), # |F INTERSECT E INTERSECT C|
        'contexts_base': [0] * len(files['contexts']) # |E INTERSECT C|
    }

    while lines['cause'] < math.inf and lines['effect'] < math.inf:
        # find matching (or higher) effect index

        # TODO: refactor
        for i in range(0, len(lines['contexts'])):
            while lines['contexts'][i] < lines['cause'] and lines['contexts'][i] < lines['effect']:
                lines['contexts'][i] = next_entry(files['contexts'][i])
                if lines['contexts'][i] == lines['effect'] and lines['effect'] < math.inf:
                    # found intersection of effect E and context C
                    counter['contexts_base'][i] += 1

        while lines['effect'] < lines['cause']:
            lines['effect'] = next_entry(files['effect'])

            # iterate through given contexts to match against E
            if lines['effect'] == math.inf:
                break
            # TODO: refactor
            for i in range(0, len(lines['contexts'])):
                while lines['contexts'][i] < lines['cause'] and lines['contexts'][i] < lines['effect']:
                    lines['contexts'][i] = next_entry(files['contexts'][i])
                if lines['contexts'][i] == lines['effect']:
                    # found intersection of effect E and context C
                    counter['contexts_base'][i] += 1
        if lines['cause'] == math.inf:
            continue

        # TODO: refactor
        for i in range(0, len(lines['contexts'])):
            while lines['contexts'][i] < lines['cause']:
                lines['contexts'][i] = next_entry(files['contexts'][i])
                if lines['contexts'][i] == lines['effect'] and lines['effect'] < math.inf:
                    # found intersection of effect E and context C
                    counter['contexts_base'][i] += 1

        counter['cause'] += 1
        has_effect = (lines['effect'] == lines['cause'])
        if has_effect:
            # found intersection of cause F and effect E
            counter['effect'] += 1

        # iterate through given contexts to match against F
        for i in range(0, len(lines['contexts'])):
            if lines['contexts'][i] == lines['cause']:
                # found intersection of cause F and context C
                counter['contexts'][i] += 1
                if has_effect:
                    # found intersection of all three
                    counter['contexts_pos'][i] += 1

        lines['cause'] = next_entry(files['cause'])

    files['cause'].close()
    files['effect'].close()
    map(lambda f: f.close(), files['contexts'])
    return counter


def wcaLift(cause, effect, *contexts):
    counter = match(cause, effect, *contexts)
    results = [ 0 ] * len(contexts)

    def caLift(total, pos, ctx_base, total_ctx):
        p_match = pos / total
        p_neutral = ctx_base / total_ctx
        return p_match - p_neutral

    total_effect = meta.loc[effect.split('_')[0]][effect.split('_')[1]]

    for i in range(0, len(contexts)):
        total_ctx = meta.loc[contexts[i].split('_')[0]]
        # C
        p_total = counter['contexts'][i] # |F INTERSECT C|
        p_pos = counter['contexts_pos'][i] # |F INTERSECT E INTERSECT C|
        p_ctx_base = counter['contexts_base'][i] # |E INTERSECT C|
        p_ctx_total = meta.loc[contexts[i].split('_')[0]][contexts[i].split('_')[1]] # |C|
        p_caLift = caLift(p_total, p_pos, p_ctx_base, p_ctx_total)
        p_weight = p_total / counter['cause']

        # NOT C
        total_context_entries = meta.sum(1).loc[contexts[i].split('_')[0]]
        n_total = counter['cause'] - p_total # |F| - |F INTERSECT C| = |F INTERSECT -C|
        n_pos = counter['effect'] - p_pos # |F INTERSECT E| - |F INTERSECT E INTERSECT C|
        n_ctx_base = total_effect - p_ctx_base # |E| - |E INTERSECT C|
        n_ctx_total = total_context_entries - p_ctx_total # |C UNION -C| - |C|
        n_caLift = caLift(n_total, n_pos, n_ctx_base, n_ctx_total)
        n_weight = weight = n_total / counter['cause']
        print(n_ctx_base, p_ctx_base)

        results[i] = p_weight * p_caLift + n_weight * n_caLift

    return results


#correlation(ARG1, ARG2)
#aLift(ARG1, 'upper', ARG2, 'upper')
#print(match('normaldist_lower', 'normaldist1_upper', 'pin_upper', 'numberrange1_upper'))
print(wcaLift(ARG1 + '_upper', ARG2 + '_upper', 'pin_upper', 'pin_lower'))
