import csv
import os
import pandas as pd
import math
from src.jenks.jenks import jenks

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

    path_list = os.listdir(root_dictionary)
    path_list.sort()
    path_list = [x for x in path_list if '.csv' in x]
    durations = []
    durations_split_list = []
    for path in path_list:
        csv_path = os.path.join(root_dictionary, path)
        data = pd.read_csv(csv_path)
        for idx, index_data in data.iterrows():
            munite_str, second_str = index_data[Duration].split(':')
            seconds = int(munite_str) * 60 + float(second_str)
            durations.append(seconds)

    durations_split_list = jenks(durations, 3)

    output_dict = './sequences'
    if not os.path.exists(output_dict):
        os.makedirs(output_dict)

    sequence_file = open(os.path.join(output_dict, 'sequence.txt'), "w")

    for path in path_list:
        txt_file = open(os.path.join(output_dict, os.path.splitext(path)[0]+'.txt'), "w")
        txt_file.write(UseStart)
        sequence_file.write(UseStart)

        csv_path = os.path.join(root_dictionary, path)
        data = pd.read_csv(csv_path)

        for idx, index_data in data.iterrows():
            whole_str = ''
            participant = index_data[Participant]
            duration = index_data[Duration]
            sentiment = index_data[Sentiment]
            decision = index_data[Decision]
            private = index_data[Private]
            survival_item = index_data[Survival_item]
            sentence = index_data[Sentence]

            a, participant, b = participant.split('.')
            whole_str = whole_str + participant.lower()

            munite_str, second_str = duration.split(':')
            seconds = int(munite_str) * 60 + float(second_str)
            if seconds <= durations_split_list[1]:
                whole_str = whole_str + '_short'
            elif seconds >= durations_split_list[2]:
                whole_str = whole_str + '_long'
            else:
                whole_str = whole_str + '_medium'

            if str(sentiment) == 'nan':
                whole_str = whole_str + '_nosent'
            elif sentiment.lower() == 'positive, negative':
                whole_str = whole_str + '_posneg'
            else:
                whole_str = whole_str + '_' + sentiment.lower()

            if str(decision) == 'nan':
                whole_str = whole_str + '_nodecision'
            else:
                whole_str = whole_str + '_decision'

            if str(private) == 'nan':
                whole_str = whole_str + '_public'
            else:
                whole_str = whole_str + '_private'

            if str(survival_item) == 'nan':
                whole_str = whole_str + '_noitem'
            else:
                whole_str = whole_str + '_yesitem'

            whole_str = whole_str + '\n'
            sequence_file.write(whole_str)
            txt_file.write(whole_str)

        sequence_file.write(UseStop)
        txt_file.write(UseStop)
        txt_file.close()

    sequence_file.close()
    print('All done.')


