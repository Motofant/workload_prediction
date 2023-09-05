import numpy as np

class TextInfo:
    def __init__(self, user_data, compare_data) -> None:
        self.user_data = user_data

        # claculatee stuff not doable with free text
        # idea from Analysis_of_text_entry_performance_metri20161119-3688-te2saj-libre.pdf
        if compare_data:
            self.compare_data = compare_data

            # Minimum String distance
    
    def levenshtein_distance(self):
        # multiple string per task --> for loop
        output_lst = [None]*len(self.compare_data)
        for number, phrase in enumerate(self.compare_data):
            word_lst = self.user_data[number].split(" ")
            compare_lst = phrase.split(" ")
            distance_lst = [None]*len(compare_lst)
            for count, word in enumerate(compare_lst):

                user = list(word_lst[count])
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
v = TextInfo(user,compare)

e = v.levenshtein_distance()

print(e)