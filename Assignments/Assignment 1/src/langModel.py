import re
import random as rand
import os
from decimal import *

class LanguageModel:
    def __init__(self, training_file):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz_"
        self.trigrams_count = {}
        self.trigrams_norm = {}
        self.bigram_count = {}
        self.unigram_count = {}
        self.variety = os.path.basename(training_file).split(".")[1]
        self.training_file = training_file

        file = open(training_file, "r", encoding="utf-8")
        self.text = "".join(file.readlines())
        file.close()

        self.init_matrice()
        self.text = self.clean_text(self.text) # clean the string : remove ponctuation, replace whitespace, etc...

        start = 0
        offset = start+3
        self.unigram_count[self.text[0]] += 1 # count the first letter of the text
        self.unigram_count[self.text[1]] += 1 # count the second letter of the text
        self.bigram_count[self.text[0:2]] += 1 # count the first bigram of the text

        # iterate each trigram, count the last letter of the trigram (unigram), count the last bigram of the trigram and
        # count the trigram
        while offset < len(self.text):
            trigram = self.text[start:offset]
            self.unigram_count[trigram[2]] += 1
            self.bigram_count[trigram[1:3]] += 1
            self.trigrams_count[trigram[0:2]][trigram[2]] += 1
            start += 1
            offset += 1

        self.compute_estimation() #compute estimation
        self.export_model()

    def clean_text(self, text):
        text = text.replace(" ", "__").lower()
        return re.sub("[^_a-z]", "", text)

    def export_model(self):
        file = "models/model_" + os.path.basename(self.training_file)
        out = open(file, "w")
        for first in self.alphabet:
            for second in self.alphabet:
                row = first + second + "\t\t"
                for third in self.alphabet:
                    row += '{:7.5f}'.format(self.trigrams_norm[first+second][third]) + "\t\t"
                row += "\n"
                out.write(row)
        out.close()

    def compute_estimation(self):
        for first in self.alphabet:
            for second in self.alphabet:
                bigram = first + second
                for letter in self.alphabet:
                    if self.trigrams_norm[bigram][letter] > 0:
                        self.trigrams_norm[bigram][letter] = self.trigrams_count[bigram][letter]/self.bigram_count[bigram]
                    else:
                        self.trigrams_norm[bigram][letter] = self.stupid_backoff(second, letter)

    def stupid_backoff(self, second, letter):
        alpha = 0.4
        if self.bigram_count[second+letter] > 0:
            factor = self.bigram_count[second+letter]/self.unigram_count[second]
            return factor * alpha
        else:
            factor = self.unigram_count[letter] / len(self.text)
            return factor * alpha * alpha

    def init_matrice(self):
        for i in self.alphabet:
            self.unigram_count[i] = 0
            for j in self.alphabet:
                bigram = i+j
                self.trigrams_count[bigram] = {}
                self.trigrams_norm[bigram] = {}
                self.bigram_count[bigram] = 0
                for letter in self.alphabet:
                    self.trigrams_count[bigram][letter] = 0
                    self.trigrams_norm[bigram][letter] = 0

    def generate_random_string(self, k):
        # choose a random trigram (<s>, w) according to its probability
        bigrams_starter = [bigram for bigram in self.trigrams_norm.keys() if bigram.startswith("_")]
        w = rand.choice(bigrams_starter)
        text = w

        # Choose a random trigram (w,x) according to its probability
        for i in range(k):
            letters = [letter for letter in self.trigrams_norm[w].keys()]
            rand.uniform(0, max([self.trigrams_norm[w][letter] for letter in letters]))
            while True:
                x = rand.choice(letters)
                if rand.random() < self.trigrams_norm[w][x]:
                    break
            text += x
            w = text[-2:]

        text = text.replace("__", " ").replace("_", "")
        file_name = "random_outputs/random_string_" + os.path.basename(self.training_file)
        file = open(file_name, "w")
        file.write(text)
        file.close()

    def compute_perplexity(self, text):
        text_cleaned = self.clean_text(text)
        probability = 1.0
        start = 0
        offset = start+2
        while offset < len(text_cleaned):
            bigram = text_cleaned[start:offset]
            letter = text_cleaned[offset]
            probability = Decimal(probability) * Decimal((1/(self.trigrams_norm[bigram][letter])))
            start += 1
            offset += 1
        return Decimal(probability) ** Decimal((1/len(text_cleaned)))
