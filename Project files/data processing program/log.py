import csv
import os
import pandas as pd

# split duration is [0.0, 2.3, 6.1, 32.0]

root_dictionary = './Annotations'

Participant = 'Participant'
Duration = 'Duration'
Sentiment = 'Sentiment'
Decision = 'Decision'
Private = 'Private'
Survival_item = 'Survival Item'
Sentence = 'Sentence'

UseStart = 'UseStart\n'
UseStop = 'UseStop\n'

if __name__ == '__main__':
    # print work, get useful log
    word_dict = {'pink': '', 'blue': '', 'green': '', 'orange': '', 'yellow': '',
                 'short': '', 'medium': '', 'long': '',
                 'positive': '', 'negative': '', 'nosent': '', 'posneg': '',
                 '_decision': '', 'nodecision': '',
                 'private': '', 'public': '',
                 'yesitem': '', 'noitem': ''}

    with open('codes.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            for word in word_dict.keys():
                if word in lines[i]:
                    if len(word_dict[word]) < 1:
                        word_dict[word] = ('(y=%d)' % (i + 1))
                    else:
                        word_dict[word] = word_dict[word] + (' | (y=%d)' % (i + 1))

    # for word in word_dict.keys():
    #     print(('label "%s" = ' % word) + word_dict[word] + ';')
    #     print('')
    #     print(('rewards "r_%s" \n  ' % word) + word_dict[word] + ' : 1;\nendrewards')
    #     print('')

    for word in ['private', 'public']:
        # for word in ['short', 'medium', 'long']:
        print(('rewards "r_%s_decision" \n  ' % word) + '('
              + word_dict[word] + ') & ('
              + word_dict['_decision'] + ') : 1;\nendrewards')
        print('')

    exit(0)
