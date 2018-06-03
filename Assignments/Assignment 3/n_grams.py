class Bigram:
    def __init__(self):
        self.bigram_count = {}
        self.unigram_count = {}
        self.bigram_norm = {}
        self.build()

    # Read the training file from https://www.ngrams.info/download_coca.asp
    # Save all bigrams and their frequencies
    # Compute the estimation (with 1-add smoothing)
    def build(self):
        f = open("w2_.txt", "r")
        for line in f.readlines():
            tuple = line.split()
            value = tuple[0]
            key = tuple[1] + "_" + tuple[2]
            self.bigram_count[key] = int(value)
            if not tuple[2] in self.unigram_count:
                self.unigram_count[tuple[2]] = 0
            self.unigram_count[tuple[2]] += 1
        self.compute_estimation()

    # Compute the estimation and normalize the probability of the bigram
    # Apply the 1-add smoothing
    def compute_estimation(self):
        for key, freq in self.bigram_count.items():
            w2 = key.split("_")[1]
            self.bigram_norm[key] = (freq + 1)/(self.unigram_count[w2] + len(self.unigram_count))

    # Compute the perxplexity of a sentence
    def compute_perplexity(self, sentence):
        prob = 1.0 # initialize the probability
        start = 1
        splitted = sentence.split() # split the sentence into array of word
        N = len(splitted) # get the number of words
        while start < N:
            key = splitted[start-1] + "_" + splitted[start]
            # If the bigram exist
            if key in self.bigram_norm:
                prob *= (1/self.bigram_norm[key])
            # if the bigram doesn't exist, compute the estimation with 1-add smoothing
            else:
                # Compute the estimation with 1-add smoothing
                unigram = self.unigram_count[splitted[start]] if start in self.unigram_count else 0
                denom = 1/(unigram + len(self.unigram_count))
                prob *= 1/denom
            start += 1

        return prob ** (1/N)