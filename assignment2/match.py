import numpy as np
from typing import List, Tuple

class User:
    def __init__(self, index, gender, pref, remaining):
        self.index = index
        self.gender = gender
        self.pref = pref
        self.remaining = remaining
        self.match = self

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    total = len(gender_id)

    users = []
    for u in range(total):
        pref = gender_pref[u]
        gender = gender_id[u]
        remaining = scores[u]
        new_user = User(u, gender, pref, remaining)
        users.append(new_user)

    proposers = []
    for i in range(int(total/2)):
        u = users[i]
        new_remaining = []
        for j in range(int(total/2), total):
            new_remaining.append((users[j], scores[i][j]))
        u.remaining = new_remaining
        proposers.append(u)

    receivers = []
    for i in range(int(total/2), total):
        u = users[i]
        new_remaining = []
        for j in range(int(total/2)):
            new_remaining.append((users[j], scores[i][j]))
        u.remaining = new_remaining
        receivers.append(u)

    for p in proposers:
        for r in receivers:
            if ((p.pref != "Men" and r.gender == "Male")
                    or (p.pref != "Women" and r.gender == "Female")
                    or (r.pref != "Men" and p.gender == "Male")
                    or (r.pref != "Women" and p.gender == "Female")):
                # p.remaining[r.u] = (r, 0.0)
                # r.remaining[p.u] = (p, 0.0)
                p.remaining = [(x, -1.0) if x == r else (x, y) for (x, y) in p.remaining]
                r.remaining = [(x, -1.0) if x == p else (x, y) for (x, y) in r.remaining]

    for u in users:
        # create remaining list sorted by priority with user index saved
        u.remaining.sort(key=lambda i: i[1], reverse=True)
        print(u.index)
        for x, y in u.remaining:
            print(x.index, y)
        print()

    matches = []
    while proposers != []:
        p = proposers[0]  # pick first proposer in free list
        if p.remaining != []:
            r, rscore = p.remaining.pop(0)
            # r = max(p.remaining, key=lambda x: x[1])[0]  # find max score remaining
            # p.remaining.pop(r.u)  # remove r from list
            pscore = [y for (x, y) in r.remaining if x == p]
            if r in receivers:  # if unmatched
                p.match = r
                r.match = p
                proposers.remove(p)
                receivers.remove(r)
            elif pscore > [y for (x, y) in r.remaining if x == r.match]:
                proposers.append(r.match)
                p.match = r
                r.match = p
                proposers.remove(p)

    for i in range(int(total)):
        p = users[i]
        matches.append((p, p.match))

    for x, y in matches:
        print(x.index, y.index)

    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
