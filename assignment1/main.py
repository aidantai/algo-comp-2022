#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # YOUR CODE HERE

    # check if preferences match
    pscore = 0
    if user1.gender in user2.preferences and user2.gender in user1.preferences:
        pscore = 1

    # check age gap
    ydiff = abs(user1.grad_year - user2.grad_year)
    yscore = 1 - 0.5*ydiff

    # match responses
    rscore = 0
    for i in range(len(user1.responses)):
        if user1.responses[i] == user2.responses[i]:
            rscore += 1
    rscore /= len(user1.responses)

    return min(0, pscore*(0.5*yscore + 0.5*rscore))


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
