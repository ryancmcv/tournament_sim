import numpy as np
import sys 

round_list = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
advance_list = [sys.argv[5], sys.argv[6], sys.argv[7]]
edge_list = [sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11]]

print(round_list)

round_list = np.asarray(round_list, dtype=np.int32)
advance_list = np.asarray(advance_list, dtype=np.int32)
edge_list = np.asarray(edge_list, dtype=np.int32)

def sim_pod(pod_size, advance, edge, entries_remaining):
    eliminated = 0
    pod = np.random.normal(loc=100, scale=10, size=pod_size-1)
    pod = -np.sort(-pod)
    
    entry = np.random.normal(loc=100, scale=10, size=1) * (1+edge)

    if entry[0] > pod[advance-1]:
        pass
    else:
        eliminated = 1

    entries_eliminated = int(entries_remaining * ((pod_size-advance)/pod_size))
    entries_remaining = int(entries_remaining - entries_eliminated)

    return eliminated, entries_remaining, entries_eliminated, entry, pod


def need_prize(entries_remaining, entries_paid):
    if entries_remaining < entries_paid:
        needs_prize = 1
    else:
        needs_prize = 0

    return needs_prize


def get_place(entries_eliminated, entry, pod, advance):
    pods = np.random.normal(loc=100, scale=10, size=(int(( entries_eliminated / (len(pod) - advance))-1), len(pod)+1))

    beaten_by = 0

    for p in pods:
        sorted(p, reverse=True)
        p = p[advance:]
        lost_to = [i for i in p if i > entry]
        beaten_by = beaten_by + len(lost_to)

    lost_to_in_pod = [i for i in pod if i > entry]
    
    place = beaten_by + 1 + len(lost_to_in_pod)

    return place


def final_round(entries_remaining, edge):
    pod = np.random.normal(loc=100, scale=10, size=entries_remaining-1)

    entry = entry = np.random.normal(loc=100, scale=10, size=1) * (1+edge)

    beaten_by = [i for i in pod if i > entry]

    place = len(beaten_by) + 1

    return place



contest_size = 672672
entries_paid = 112112
entry_fee = 25

losers_paid_list = [0, 1, 1, 1]

contest_size = np.prod([a/b for a,b in zip(round_list,advance_list)]) * round_list[-1]

for e in range(0,150):

    r = -1
    entries_remaining = contest_size
    eliminated = 0    

    while eliminated == 0:
        r += 1

        if r < len(round_list)-1:
                eliminated, entries_remaining, entries_eliminated, entry, pod = sim_pod(round_list[r], advance_list[r], edge_list[r], entries_remaining)
        elif r == len(round_list)-1:
                eliminated = 1

    if losers_paid_list[r] == 0:
        place = contest_size
    elif r < len(round_list)-1:
        place = get_place(entries_eliminated, entry, pod, advance_list[r])
    else:
        place = final_round(round_list[r], edge_list[r])


    print(str(place) + '-' + str(r+1))
        

