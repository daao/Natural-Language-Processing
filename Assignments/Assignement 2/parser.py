from enum import Enum
import re
import random

TRAINING_FILE = 'feattemp.txt'

class Action(Enum):
    NONE = "None"
    SHIFT = "SHIFT"
    LEFT = "LEFTARC"
    RIGHT = "RIGHTARC"


class Parser:
    def __init__(self):
        self.features_training = {}
        self.sentences = {}
        self.relations = []
        self.train()

    # Function that read the training file and store the features template and the action into a dictionnary
    # The key is the feature template and the value is the action
    def train(self):
        file = open(TRAINING_FILE, 'r')
        for line in file.readlines():
            if line != "\n":
                split = line.split("\t")
                for template in split:
                    temp_split = template.split(",")
                    feat = temp_split[0].rstrip().replace(" ", "")
                    op = temp_split[1].rstrip().replace(" ", "")
                    if not feat in self.features_training.keys():
                        self.features_training[feat] = []
                    if not op in self.features_training[feat]:
                        self.features_training[feat].append(op)
        file.close()

    # Function that read the input file and store all of features for each word for each sentence
    def read_input_file(self, input_file):
        file = open(input_file, 'r')
        id = 0
        self.sentences[id] = []
        for line in file.readlines():
            if line == "\n":
                id += 1
                self.sentences[id] = []
            elif not line.startswith("#"):
                features = line.split("\t")
                self.sentences[id].append(Word(features))

    def parse(self):
        connl_file = open("output.txt", "w")
        trace_file = open("conftable.txt", "w")
        root = Word(["0", "ROOT", "ROOT", "ROOT"])

        for id, words in self.sentences.items():
            # copy the list of words of the sentence for the buffer
            word_list = words[:]

            # write the open balise xml of the trace
            self.write_open_tag_trace(trace_file, id, words)

            # Apply the shift reduce algorithm
            shift_reduce = Shift_Reduce_Algorithm([root], word_list)
            while not shift_reduce.is_final():
                features = [shift_reduce.s1().pos, shift_reduce.s2().pos, shift_reduce.b1().pos]
                action = self.oracle(features, shift_reduce)
                shift_reduce.apply(action)
                # write the trace of the current configuration in the trace file
                trace_file.write(shift_reduce.trace)

            # close the xml tag of the trace
            trace_file.write("<sentence>\n\n")

            # Write the result of the algorithm wih the ConnL U format in the output.txt
            self.write_connl_file(connl_file, id, words, shift_reduce.relations)

            # newline for the next sentence
            connl_file.write("\n")

        trace_file.close()
        connl_file.close()

    def write_open_tag_trace(self, file, id, words):
        tag = '<sentence file="assignment2" '
        tag += 'id="' + str(id) + '"'
        tag += ' text="' + self.get_sentence(words) + '">\n'
        file.write(tag)
        file.write("Step\tStack\tBuffer\tAction\tRelation Added\n")


    def write_connl_file(self, file, sentence_id, words, dep_rel):
        # header of ConnL-U file
        file.write("# sent_id = " + str(sentence_id+1) + "\n")
        file.write("# text = " + self.get_sentence(words) + "\n")

        # body of ConnL-U file
        for word in words:
            line = word.id + "\t"
            line += word.form + "\t"
            line += word.lemma + "\t"
            line += word.pos + "\t"
            line += "_\t"
            line += dep_rel[word.id] + "\t"
            line += "DEP\n"
            file.write(line)

    def get_sentence(self, words):
        sentence = ""
        for word in words:
            sentence += word.form + " "
        return sentence

    # param features : get all features of the word retrieving in the reading of the input file
    # Function that determine which action is needed to apply along the training information
    def oracle(self, features, configuration):
        s1 = features[0]
        s2 = features[1]
        b1 = features[2]

        # defined possible combination in order, if the first has multiple actions, let look in the second and over
        # until we have only 1 possible action
        combinations = [s1+s2, s2+b1, s1]
        features_actions = []
        for combination in combinations:
            if combination in self.features_training.keys():
                features_actions = self.features_training[combination]
            if len(features_actions) == 1:
                break

        action = features_actions[0]
        if action == Action.LEFT.value:
            return Action.LEFT.value
        elif action == Action.RIGHT.value:
            return Action.RIGHT.value
        elif action == Action.SHIFT.value:
            return Action.SHIFT.value
        else :
            return Action.NONE


class Shift_Reduce_Algorithm:
    def __init__(self, stack, buffer):
        self.stack = stack
        self.buffer = buffer
        self.relations = {}
        self.trace = ""
        self.step = 0

    def s1(self):
        if len(self.stack) <= 0:
            print("Error : the stack cannot be empty")
        return self.stack[-1]

    def s2(self):
        if len(self.stack) <= 1:
            return Word(["0", "NULL", "NULL", "NULL"])
        return self.stack[-2]

    def s3(self):
        if len(self.stack) <= 2:
            return Word(["0", "NULL", "NULL", "NULL"])
        return self.stack[-3]

    def b1(self):
        if len(self.buffer) <= 0:
            return Word(["0", "EMPTY", "EMPTY", "EMPTY"])
        return self.buffer[0]

    def shift(self):
        if len(self.buffer) <= 0:
            print("Err : the buffer is empty in a SHIFT operation")
            return
        word = self.buffer.pop(0)
        self.stack.append(word)
        self.trace = str(self.step) + "\t" \
                     + self.stack_to_string() + "\t" \
                     + self.buffer_to_string() \
                     + "\tSHIFT\n"
        self.step+=1

    def left_arc(self):
        if len(self.stack) <= 1:
            print("Err : the stack has not enough data for a LEFTARC operation.")
            return
        head = self.stack[-1]
        dep = self.stack[-2]
        self.stack.remove(dep)
        self.relations[dep.id] = head.id
        self.trace = str(self.step) + "\t" \
                     + self.stack_to_string() + "\t" \
                     + self.buffer_to_string() \
                     + "\tLEFTARC\t" \
                     + dep.form + "<-" + head.form +"\n"
        self.step += 1

    def right_arc(self):
        if len(self.stack) <= 1:
            print("Err : the stack has not enough data for a RIGHTARC operation.")
            return
        if (self.stack[-2].pos == "ROOT" and len(self.buffer) == 0) or (self.stack[-2].pos != "ROOT"):
            dep = self.stack.pop()
            head = self.stack[-1]
            self.relations[dep.id] = head.id
            self.trace = str(self.step) + "\t" \
                         + self.stack_to_string() + "\t" \
                         + self.buffer_to_string() \
                         + "\tRIGHTARC\t" \
                         + head.form + "->" + dep.form +"\n"
            self.step += 1

    def is_final(self):
        last = self.stack[-1]
        return last.pos == "ROOT" and len(self.buffer) == 0

    def apply(self, action):
        if action == Action.SHIFT.value:
            return self.shift()
        if action == Action.LEFT.value:
            return self.left_arc()
        if action == Action.RIGHT.value:
            return self.right_arc()

    def stack_to_string(self):
        str = "["
        for word in list(self.stack[:-1]):
            str += word.form + ", "
        str += self.stack[-1].form
        str += "]"
        return str

    def buffer_to_string(self):
        str = "["
        if len(self.buffer) > 0:
            for word in list(self.buffer[:-1]):
                str += word.form + ", "
            str += self.buffer[-1].form
        str += "]"
        return str

class Word:
    def __init__(self, features):
        self.id = features[0].rstrip()
        self.form = features[1].rstrip()
        self.lemma = features[2].rstrip()
        self.pos = features[3].rstrip()


parser = Parser()

parser.read_input_file("input.txt")

parser.parse()