from src.langModel import LanguageModel

training_set = ["../training_set/training.AU", "../training_set/training.GB", "../training_set/training.US"]
test = "../test_set/test"

lang_models = []

for training in training_set:
    lm = LanguageModel(training)
    lm.generate_random_string(300, True)
    lang_models.append(lm)

file = open(test, "r", encoding="utf-8")
perplexity = {}
i = 0
for line in file.readlines():
    perplexity[str(i)] = {}
    for lang_model in lang_models:
        perplexity[str(i)][lang_model.variety] = lang_model.compute_perplexity(line)
        print("Perplexity of " + lang_model.variety + " = " + str(perplexity[str(i)][lang_model.variety]))

    best = min(perplexity[str(i)].keys(), key=(lambda k:perplexity[str(i)][k]))
    print("Best language model is " + best)
    i += 1

file.close()
