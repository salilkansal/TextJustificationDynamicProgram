#!/usr/bin/python

import sys

if len(sys.argv) > 1:
    file = open(sys.argv[1], 'r')
    source = file.read()
    file.close()
else:
    source = raw_input()

if len(sys.argv) > 2:
    M = int(sys.argv[2])
else:
    M = 80
# print source.split()
word_lengths_preprocess = []
count = 0

input_words = [""] + source.split()
print input_words
word_lengths = map(lambda x: len(x), input_words)
print 'word_lengths: ' + str(word_lengths)

for word in input_words:
    count += len(word)
    word_lengths_preprocess.append(count)

print 'word_lengths_preprocess:' + str(word_lengths_preprocess)


# This function calculates the sentence length which are from word
def __length_of_sentence(i, j):
    if i == 0:
        length_of_words = word_lengths_preprocess[j]
    else:
        length_of_words = word_lengths_preprocess[j] - word_lengths_preprocess[i - 1]

    return length_of_words + j - i


def neatness(i, j):
    sentence_length = __length_of_sentence(i, j)
    if M < sentence_length:
        return sys.maxint
    elif j == len(input_words) - 1:
        return 0
    else:
        return (M - sentence_length) ** 3


text_justification = [0]
aux = [0]
spaces = [0]

for j in range(1, len(input_words)):
    text_justification.append(sys.maxint)
    aux.append(sys.maxint)
    spaces.append(0)
    for i in range(1, j + 1):
        if text_justification[j] > text_justification[i - 1] + neatness(i, j):
            text_justification[j] = text_justification[i - 1] + neatness(i, j)
            aux[j] = i
            spaces[j] = neatness(i, j) ** (1. / 3.)

print text_justification
print aux

output = []
i = aux[len(input_words) - 1]
while i != 1:
    output.insert(0, i)
    i = aux[i - 1]

output.insert(0, i)


print output
#
# for idx, val in enumerate(output):
#     for l in range(val, output[idx + 1]):
#         print input_words[l] + " "
