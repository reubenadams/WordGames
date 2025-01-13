from itertools import product
from collections import defaultdict
from random import shuffle, choice


alphabet = "abcdefghijklmnopqrstuvwxyz"


class Corpus:
    def __init__(self, path, min_length):

        with open(path, "r") as f:
            word_list = f.readlines()
        
        word_list = [word.strip() for word in word_list]
        word_list = [word for word in word_list if len(word) >= min_length]

        self.word_list = word_list
        self.min_word_length = min(len(word) for word in word_list)
        self.max_word_length = max(len(word) for word in word_list)

        self.start_end_length_lists = defaultdict(list)
        for start_char, end_char, length in product(alphabet, alphabet, range(self.min_word_length, self.max_word_length + 1)):
            for word in word_list:
                if word[0] == start_char and word[-1] == end_char and len(word) == length:
                    self.start_end_length_lists[(start_char, end_char, length)].append(word)

        self.start_max_length_lists = defaultdict(list)
        for start_char, max_length in product(alphabet, range(self.min_word_length, self.max_word_length + 1)):
            for word in word_list:
                if word[0] == start_char and len(word) <= max_length:
                    self.start_max_length_lists[(start_char, max_length)].append(word)

    def start_end_length_list(self, start_char, end_char, length, shuffled=True):
        L = list(self.start_end_length_lists[(start_char, end_char, length)])
        if shuffled:
            shuffle(L)
        return L
    
    def start_max_length_list(self, start_char, max_length, shuffled=True):
        max_length = min(max_length, self.max_word_length)
        L = list(self.start_max_length_lists[(start_char, max_length)])
        if shuffled:
            shuffle(L)
        return L
    
    def random_word(self):
        return choice(self.word_list)


class TreeNode:

    def __init__(self, word_list, total_snake_length, corpus):

        self.word_list = word_list
        self.total_snake_length = total_snake_length
        self.corpus = corpus

        self.current_snake_length = sum([len(word) for word in word_list]) - (len(word_list) - 1)
        self.snake_complete = total_snake_length == self.current_snake_length - 1
        self.remaining_length = total_snake_length - self.current_snake_length
        self.completion_length = self.remaining_length + 2
        self.max_non_completion_length = self.completion_length - (corpus.min_word_length - 1)

        self._completing_words = None
        self._non_completing_words = None
        self._children = None

    @property
    def completing_words(self):
        if self._completing_words is None:
            start_char = self.word_list[-1][-1]
            end_char = self.word_list[0][0]
            self._completing_words = self.corpus.start_end_length_list(start_char, end_char, self.completion_length)
        return self._completing_words

    @property
    def non_completing_words(self):
        if self._non_completing_words is None:
            start_char = self.word_list[-1][-1]
            self._non_completing_words = self.corpus.start_max_length_list(start_char, self.max_non_completion_length)
        return self._non_completing_words
    
    @property
    def children(self):
        child_words = [word for word in self.completing_words + self.non_completing_words if word not in self.word_list]
        if self._children is None:
            self._children = [TreeNode(self.word_list + [word], self.total_snake_length, self.corpus) for word in child_words]
        return self._children


    def depth_first_search(self):
        if self.snake_complete:
            return self.word_list
        for child in self.children:
            result = child.depth_first_search()
            if result:
                return result


corpus = Corpus("word_lists/words_english_2k.txt", 3)


def get_snake(snake_length):
    snake = None
    while snake is None:
        first_word = corpus.random_word()
        root = TreeNode(word_list=[first_word], total_snake_length=snake_length, corpus=corpus)
        snake = root.depth_first_search()
    return snake
