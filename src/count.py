import pickle as pk

class Count:
    def __init__(self, vocabulary, phrases, word):
        self.phrases = phrases
        self.vocabulary = vocabulary
        self.total = len(phrases)
        self.word = word

    def main(self):
        counter = self.count_word()
        np_w1_w2, p_w1_w2, p_w1, p_w2 = self.pair_counter()

        return [counter, np_w1_w2, p_w1_w2, p_w1, p_w2]

    def count_word(self):
        counter = {}
        for v in self.vocabulary:
            n = 0
            for phrase in self.phrases:
                if v in phrase:
                    n+=1
            counter[v] = n/self.total
        
        return counter
        
    def pair_counter(self):
        np_w1_w2 = {}
        p_w1_w2 = {}
        p_w1 = {}
        p_w2 = {}

        for v1 in self.vocabulary:
            if self.word != v1:
                nt_w1_w2 = 0
                t_w1_w2 = 0
                t_w1 = 0
                t_w2 = 0
                for phrase in self.phrases:
                    if self.word in phrase and v1 in phrase:
                        t_w1_w2 += 1
                    elif self.word in phrase and v1 not in phrase:
                        t_w1 += 1
                    elif self.word not in phrase and v1 in phrase:
                        t_w2 += 1
                    elif self.word not in phrase and v1 not in phrase:
                        nt_w1_w2 += 1

                np_w1_w2[(self.word, v1)] = nt_w1_w2/self.total
                p_w1_w2[(self.word, v1)] = t_w1_w2/self.total
                p_w1[(self.word, v1)] = t_w1/self.total
                p_w2[(self.word, v1)] = t_w2/self.total


        with open('corpus/p_w1_w2.pickle', 'wb') as handle1:
            pk.dump(p_w1_w2, handle1, protocol=pk.HIGHEST_PROTOCOL)

        with open('corpus/p_w1.pickle', 'wb') as handle2:
            pk.dump(p_w1, handle2, protocol=pk.HIGHEST_PROTOCOL)

        with open('corpus/p_w2.pickle', 'wb') as handle3:
            pk.dump(p_w2, handle3, protocol=pk.HIGHEST_PROTOCOL)
                    
        return [np_w1_w2, p_w1_w2, p_w1, p_w2]