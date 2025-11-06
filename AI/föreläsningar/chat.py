from collections import Counter
import random


text = ('Your final challenge\n'
        'Let your bitch go through your phone\n'
        'Hell nah yo ass tweaking jigsaw')
text = text.replace('\n', ' ')


counter = Counter(text[i:i+3] for i in range(len(text)-3))


class ThreeGram:
    def __init__(self):
        self.counts = {}

    def train(self, text):
        for i in range(len(text) - 3):
            ngram = text[i:i+3]
            next_char = text[i+3]
            if ngram not in self.counts:
                self.counts[ngram] = Counter()
            self.counts[ngram][next_char] += 1
    def next_token_probability(self, ngram):
        #Compute the probability distribution of next token
        if ngram not in self.counts:
            return None
        next_chars = self.counts[ngram]
        total = next_chars.total()
        next_char_prob = {char: count/total for char, count in next_chars.items()}
        return next_char_prob
    def generate_next_char(self, context):
        context_window = context[-3:]
        if context_window not in self.counts:
            return None
        counter = self.counts[context_window]
        chars, weights = list(counter.keys()), list(counter.values())
        sample = random.sample(chars, 1, counts=weights)
        return(sample[0])
lm = ThreeGram()
lm.train(text)
print(lm.generate_next_char('ur '))