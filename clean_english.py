with open("word_lists/words_2k_most_common_contemp_fiction_wiki.txt", "rb") as f:
    words = f.read().decode("utf-8").split("\n")
    words = [word[3:-3] for word in words]
    words = [word.lower() for word in words if '\'' not in word and ' ' not in word]


with open("word_lists/words_english_2k.txt", "w") as f:
    f.write("\n".join(words))
