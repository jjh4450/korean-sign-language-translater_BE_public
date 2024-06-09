# -*- coding: utf-8 -*- #인코딩 방식 설정
from jamo import h2j, j2hcj
from konlpy.tag import Okt
import re

def similar(want_word, main_list):
    """
    Find the most similar word in the list and return the corresponding dictionary.
    """
    best_match = None
    best_similarity = 0

    want_word = ''.join(only_korean(want_word))
    for entry in main_list:
        word_list = re.split(r'[, ]', entry['title'])
        for word in word_list:
            word = ''.join(only_korean(word))
            if len(word) <= len(want_word):
                similarity = max(0, len(re.findall(r'{}(?=\W|$)'.format(want_word), word)) / len(want_word))
                if similarity == 1:
                    return entry
                elif similarity > best_similarity:
                    best_similarity = similarity
                    best_match = entry

    return best_match if best_match else {"title": want_word, "url": None, "length": None}

def only_korean(text):
    """Extract only Korean characters from the given text."""
    return ' '.join(re.compile('[|ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+').findall(text)).split()

def clean(sentence):
    """Split the sentence into morphemes."""
    okt = Okt()

    circle = ['께', '으로', '으로서', '같이', '로', '게', '라고', '치고', '치고는', '에서', '으로', '로']
    number = ['이다', '다', '에게다', '야']
    big_gualho = ['이랑', '하고']

    clean_words = []
    for word in okt.pos(sentence, stem=True):
        if word[1] == "Josa":
            if word[0] in circle:
                clean_words.append(f"{word[0]}①")
            elif word[0] in number:
                clean_words.append(f"{word[0]}1")
            elif word[0] in big_gualho:
                clean_words.append(f"{word[0]}[1]")
            elif word[0] == "만":
                clean_words.append("만1①")
            elif word[0] == "에":
                clean_words.append("에[1]①")
            else:
                clean_words.append(word[0])
        elif word[1] not in ['Eomi', 'Punctuation'] and word[0] != "하다" and word[0] != "\n":
            word = re.sub("하다", "", word[0])
            clean_words.append(word)

    # print(clean_words)
    return clean_words

def jamo_bunri(word):
    """Split the word into individual jamo components."""
    result = j2hcj(h2j(word))
    return list(result)