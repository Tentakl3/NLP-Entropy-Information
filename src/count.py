from itertools import combinations
import pandas as pd
import pickle as pk

class Count:
    def __init__(self, vocabulary, phrases):
        self.phrases = phrases
        self.vocabulary = vocabulary
        self.total = len(phrases)

    def main(self):
        #counter = self.count_word()
        #self.h()
        pair_counts = self.pair_counter()

    def count_word(self):
        counter = {}
        for v in self.vocabulary:
            n = 0
            for phrase in self.phrases:
                if v in phrase:
                    n+=1
            counter[v] = n
        
        return counter
        
    def pair_counter(self):
        pair_counts = {}

        vocabulary_pairs = list(combinations(self.vocabulary, 2))

        for v1, v2 in vocabulary_pairs:
            pair_counts[(v1, v2)] = 0
            for phrase in self.phrases:
                if v1 in phrase and v2 in phrase:
                    pair_counts[(v1, v2)] += 1

        with open('corpus/pair_count.pickle', 'wb') as handle:
            pk.dump(pair_counts, handle, protocol=pk.HIGHEST_PROTOCOL)
                    
        return pair_counts
    
    def h(self):
        with open('corpus/counter_matrix.pickle', 'rb') as handle:
            counter_matrix = pk.load(handle)
        
        for element in counter_matrix["útil"]:
            if element != 0:
                print(element)