#!/usr/bin/python

"""
Programming Project
Design and Analysis of Algorithms
CS 6363

Printing Neatly
CLRS Pg 405

Dynamic Program

"""
import sys

EXTRA_SPACES_SYMBOL = ' '
DEFAULT_LINE_WIDTH = 80

# reading the input source
if len(sys.argv) > 1:
    input_file = open(sys.argv[1], 'r')
    source = input_file.read()
    input_file.close()
else:
    source = raw_input()

# if there is second argument then set the line width to that. else the max line width is default
if len(sys.argv) > 2:
    M = int(sys.argv[2])
else:
    M = DEFAULT_LINE_WIDTH
# print source.split()

word_lengths_preprocess = []
count = 0

# making the 0th index of source to be empty to be consistent with the algorithm
input_words = [""] + source.split()
word_lengths = map(lambda x: len(x), input_words)

# Pre-processing the length of words so that the sentence_length can be calculated in constant time
for word in input_words:
    count += len(word)
    word_lengths_preprocess.append(count)


# This function calculates the sentence length which are from word
def length_of_sentence(start_word_index, end_word_index):
    # if it is first word
    if start_word_index == 0:
        length_of_words = word_lengths_preprocess[end_word_index]
    else:
        length_of_words = word_lengths_preprocess[end_word_index] - word_lengths_preprocess[start_word_index - 1]

    return length_of_words + end_word_index - start_word_index


def neatness(i, j):
    sentence_length = length_of_sentence(i, j)
    if M < sentence_length:
        return sys.maxint
    elif j == len(input_words) - 1:
        return 0
    else:
        return (M - sentence_length) ** 3


text_justification = [0]
aux = [0]

for j in range(1, len(input_words)):
    text_justification.append(sys.maxint)
    aux.append(sys.maxint)
    for i in range(1, j + 1):
        if text_justification[j] > text_justification[i - 1] + neatness(i, j):
            text_justification[j] = text_justification[i - 1] + neatness(i, j)
            aux[j] = i


# This method uses aux array to print the final solution. It return it as a list of sentences
def get_solution(aux_array, n):
    if aux_array[n] == 1:
        start_lines = []
    else:
        start_lines = (get_solution(aux_array, aux_array[n] - 1))
    start = aux_array[n]
    end = n
    line = input_words[start:end + 1]
    line = put_extra_spaces(line, start, end)

    start_lines.append(line)
    return start_lines


def put_extra_spaces(line, start, end):
    extra_spaces = M - length_of_sentence(start, end)
    positions = len(line) - 1

    # No formatting for last line
    if end == len(word_lengths_preprocess) - 1:
        return line

    # If the number of spaces to add are more than the number of positions available
    if positions < extra_spaces:
        num_of_spaces_on_every_position = extra_spaces / positions
        line_output = []
        for index, word in enumerate(line):
            if index != 0:
                word_with_spaces = EXTRA_SPACES_SYMBOL * num_of_spaces_on_every_position + word
                line_output.append(word_with_spaces)
            else:
                line_output.append(word)
            return line_output
    # Else case when number of extra spaces are less than the number of positions available
    elif extra_spaces != 0:
        interval = positions / extra_spaces
        extra_positions = positions % extra_spaces

        pos = interval
        while pos <= positions:
            line[pos] = EXTRA_SPACES_SYMBOL + line[pos]
            pos += interval
            if extra_positions > 0:
                extra_positions -= 1
                pos += 1

        return line
    else:
        return line
        # distribute the spaces evenly


output = (get_solution(aux, len(input_words) - 1))
# print output

penalty = text_justification[len(word_lengths) - 1]
print penalty
print

for sentence in output:
    for idx, word in enumerate(sentence):
        if idx == len(sentence) - 1:
            print word
        else:
            print word,
