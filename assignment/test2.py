def update_score(nscore, name):
    """
    func to update the scores.txt file with the 10 highest scores
    """
    # open the file, append new highscore, sort the list, only take [0:10]
    with open('scores.txt', 'r') as f:
        data = f.readlines()
        data.append(f'{name}:{str(nscore)} \n')
        
        # scores = sorted(scores, key=int, reverse=True)
        # scores = scores[0:10]

    # write the length 10 list back to the file
    with open('scores.txt', 'w') as f:
        for data in data:
            f.write(str(data))

name = 'test1'
update_score(10000, name)