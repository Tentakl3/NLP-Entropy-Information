from math import log

class Entropy:
    def __init__(self, counter,np_w1_w2, p_w1_w2, p_w1, p_w2, vocabulary, word):
        self.vocabulary = vocabulary
        self.counter = counter
        self.np_w1_w2 = np_w1_w2
        self.p_w1_w2 = p_w1_w2
        self.p_w1 = p_w1
        self.p_w2 = p_w2
        self.word = word
    
    def main(self):
        self.h()
        self.information()

    def h(self):
        h_dict = {}
        for v in self.vocabulary:
            if self.word != v:
                if self.p_w2[(self.word, v)] != 0 and self.p_w1_w2[(self.word, v)] != 0 and self.p_w1[(self.word, v)] != 0:
                    h_value = (-1)*((self.np_w1_w2[(self.word, v)] * log(self.np_w1_w2[(self.word, v)] / (1 - self.p_w2[(self.word, v)])) \
                                            + self.p_w1[(self.word, v)] * log(self.p_w1[(self.word, v)]/ (1 - self.p_w2[(self.word, v)]))) \
                                            + (self.p_w2[(self.word, v)] * log(self.p_w2[(self.word, v)]/ self.p_w2[(self.word, v)]) \
                                            + self.p_w1_w2[(self.word, v)] * log(self.p_w1_w2[(self.word, v)]/ self.p_w2[(self.word, v)])))
                else:
                    h_value = 10000

                h_dict[v] = h_value

        sorted_h_dict = dict(sorted(h_dict.items(), key=lambda item: item[1]))

        with open(f"corpus/h_{self.word}.txt", 'w', encoding="utf-8") as f:  
            for key, value in sorted_h_dict.items():
                f.write(f"H({self.word} | {key}) = {value}\n")

    def information(self):
        i_dict = {}
        for v in self.vocabulary:
            if self.word != v:
                if self.p_w1_w2[(self.word, v)] != 0 and self.p_w1[(self.word, v)] != 0 and self.p_w2[(self.word, v)] != 0:
                    i_value = self.np_w1_w2[(self.word, v)] * log(self.np_w1_w2[(self.word, v)] /((1 - self.counter[self.word]) * (1 - self.counter[v]))) \
                        + self.p_w1[(self.word, v)] * log(self.p_w1[(self.word, v)] / (self.counter[self.word] * (1 - self.counter[v]))) \
                        + self.p_w2[(self.word, v)] * log(self.p_w2[(self.word, v)] / ((1 - self.counter[self.word]) * self.counter[v])) \
                        + self.p_w1_w2[(self.word, v)] * log(self.p_w1_w2[(self.word, v)]/(self.counter[self.word] * self.counter[v]))
                else:
                    i_value = 1000
                
                i_dict[v] = i_value

        sorted_i_dict = dict(sorted(i_dict.items(), key=lambda item: item[1]))

        with open(f"corpus/i_{self.word}.txt", 'w', encoding="utf-8") as f:  
            for key, value in sorted_i_dict.items():
                f.write(f"I({self.word} ; {key}) = {value}\n")