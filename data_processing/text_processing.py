import numpy as np
import pandas as pd
import statistics
import json
class TextInfo:
    
    def __init__(self, user_data, compare_data, mode) -> None:
        self.user_data = user_data
        self.mode = mode
        # claculatee stuff not doable with free text
        # idea from Analysis_of_text_entry_performance_metri20161119-3688-te2saj-libre.pdf
        self.compare_data = compare_data
        print(self.user_data)
        print(self.compare_data)
        self.levenshtein = self.levenshtein_distance() if self.compare_data else [[0]]

        self.levenshtein_sum_phrase = [sum(x)for x in self.levenshtein]
        self.levenshtein_avg_total = statistics.mean(self.levenshtein_sum_phrase)
        self.levenshtein_sum_total = sum(self.levenshtein_sum_phrase)
        self.words_sum = sum(self.word_count())
        self.chars_space, self.chars_nospace = self.char_count()    
        self.chars_space_sum = sum(self.chars_space)
        self.chars_nospace_sum = sum(self.chars_nospace)

    def levenshtein_distance(self):
        # multiple string per task --> for loop
        output_lst = [None]*len(self.compare_data)
        for number, phrase in enumerate(self.compare_data):
            word_lst = self.user_data[number].split(" ")
            compare_lst = phrase.split(" ")
            distance_lst = [None]*len(compare_lst)
            for count, word in enumerate(compare_lst):
                if len(word)==0:
                    continue
                user = list(word_lst[min(count, len(word_lst)-1)]) # to avoid more words
                compare = list(word)
                user_len = len(user)
                compare_len = len(compare)
                x = np.zeros(shape=(user_len+1, compare_len+1))
                x[0][range(compare_len+1)] = range(compare_len+1)
                x[:,0][range(user_len+1)] = range(user_len+1)

                for i in range(1,compare_len+1):
                    for j in range(1,user_len+1):
                        sub_cost = 0
                        if user[j-1] != compare[i-1]:
                            sub_cost = 1

                        x[j,i] = min(x[j-1,i]+1,x[j,i-1]+1,x[j-1,i-1]+sub_cost)
                distance_lst[count] = x[user_len,compare_len]

                # word doesnt exist
                #distance_lst[number] = len(compare)
            output_lst[number] = distance_lst

        return output_lst
    
    def word_count(self):
        if self.compare_data:
            output = [0]*len(self.user_data)
            # compare data exists --> mulitple phrases
            for count,text in enumerate(self.user_data):
                text = text.replace("\n"," ")
                output[count] = len(text.split(" ")) 

            return output
        else:
            self.user_data = self.user_data.replace("\n"," ")
            return [len(self.user_data.split(" "))]
    
    def char_count(self):
        if self.compare_data:
            char_with_space = [0]*len(self.user_data)
            char_without_space = [0]*len(self.user_data)
            # compare data exists --> mulitple phrases
            for count,text in enumerate(self.user_data):
                text = text.replace("\n"," ")
                char_with_space[count]=len(text)
                char_without_space[count]=len(text.replace(" ",""))

            return char_with_space, char_without_space
        else:
            self.user_data = self.user_data.replace("\n"," ")
            return [len(self.user_data)],[len(self.user_data.replace(" ",""))] 
    
    def output_dict(self):
        return{
            #self.mode+"levenshtein":self.levenshtein,
            #self.mode+"levenshtein_sum_phrase":self.levenshtein_sum_phrase,
            self.mode+"levenshtein_sum_total":self.levenshtein_sum_total,
            self.mode+"levenshtein_avg_total":self.levenshtein_avg_total,
            self.mode+"word_sum":self.words_sum,
            #self.mode+"chars_space":self.chars_space, 
            #self.mode+"chars_nospace":self.chars_nospace,  
            self.mode+"chars_space_sum":self.chars_space_sum,
            self.mode+"chars_nospace_sum":self.chars_nospace_sum,
        }

if __name__ == '__main__':
    if True:
        #with open("./logging/Sensor_test_1_easy_phrases.csv", mode='r') as file:
        #    compare = file.read().splitlines()
        compare = pd.read_csv("./logging/Sensor_test_1_easy_phrases.csv",header=None)[0].tolist()
        user_df = pd.read_csv("./logging/Sensor_test_1_phrase_user_entered.csv", index_col=[0],header=None)
        user = user_df[1].tolist()
        print(user)
        print(compare)
    else:
        with open("./logging/Sensor_test_1_writing__user_entered.txt", mode='r') as file:
            user = file.read()
        compare = None
        print(user)
    '''
    user = [
        "dolfins heap high out of the waer",
        "do not say anything" ,
        "the union will go on strike",
        "we want grocery shooting",
        "interactions between men and woman",
    ]

    compare = [
        "dolphins leap high out of the water",
        "do not say anything",
        "the union will go on strike",
        "we went grocery shopping",
        "interactions between men and women",
    ]
    '''
    v = TextInfo(user_data=user, compare_data=compare)

    x = v.word_count()
    print(f"Anzahl Worte: {x} --> {v.words_sum}")
    w_s,wo_s = v.char_count()
    print(f"Anzahl chars(mit space): {w_s} --> {v.chars_space_sum}")
    print(f"Anzahl chars(ohne space): {wo_s} --> {v.chars_nospace_sum}")

    print(json.dumps(v.output_dict(), indent=2))