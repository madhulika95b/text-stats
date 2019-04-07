#!/usr/bin/env python
"""Calculating stats on tokenized words and after removal of stop words"""

from __future__ import print_function
import io
import re
import os
import argparse
import string


class TextStatistics(object):
    """Class to tokenize and compute stats"""
    def __init__(self, filename, stopfile=None, case_sensitive=False):
        self.filename = filename
        self.stopfile = stopfile
        self.case_sensitive = case_sensitive
        self.tokenize_txt()
        self.get_unique_count()
        self.read_stop_list()
        self.get_average_len()
        self.get_char_type_count()
        self.number_of_tokens_with_stop_words_removed()
        self.letter_ratio = calc_ratio(self.letters, len(self.chars))
        self.number_ratio = calc_ratio(self.numbers, len(self.chars))
        self.punctuation_ratio = calc_ratio(self.punctuation, len(self.chars))

    def tokenize_txt(self):
        """Read the text_file and tokenize on whitespaces"""
        with io.open(self.filename, 'r', encoding='utf8') as txt_file:
            file_txt = txt_file.read()
        token_list = re.split('\\s+', file_txt.strip())
        chars = list(file_txt)
        if token_list == ['']:
            token_list = []
        self.token_list = token_list
        self.chars = chars

    def read_stop_list(self):
        """Read all stopwords into a set"""
        if self.stopfile is None:
            self.stopwords = set()
            return
        with io.open(self.stopfile, 'r', encoding='utf8') as stop_file:
            stop_words = set(line.strip() for line in stop_file)
            if not self.case_sensitive:
                stop_words = {item.lower() for item in stop_words}
        self.stopwords = stop_words

    def get_unique_count(self):
        """Get unique words from tokenized list"""
        if self.case_sensitive:
            uniquewords = set(self.token_list)
        else:
            uniquewords = set(item.lower() for item in self.token_list)
        self.test = uniquewords
        self.unique_tokens = len(uniquewords)

    def get_average_len(self):
        """Calculates avg length of words"""
        tokens_length_sum = sum(len(word) for word in self.token_list)
        average = calc_ratio(tokens_length_sum, len(self.token_list))
        self.average_len = average

    def get_char_type_count(self):
        """Determines the character type-alphabet, number or a punctuation"""
        numbers = letters = punctuation = 0
        for char in self.chars:
            if char.isalpha():
                letters = letters + 1
            elif char.isdigit():
                numbers = numbers + 1
            elif char in string.punctuation:
                punctuation = punctuation + 1
        self.letters = letters
        self.numbers = numbers
        self.punctuation = punctuation

    def number_of_tokens_with_stop_words_removed(self):
        """Returns tokens after removing stop words"""
        no_stopword_count = 0
        for word in self.token_list:
            if not self.case_sensitive:
                word = word.lower()
            word = re.sub(r'[][!?,/@#$%^<>.&(){}":;(0-9)~-]', '', word)
            if word not in self.stopwords:
                no_stopword_count = no_stopword_count + 1
        self.no_stopword_count = no_stopword_count


def calc_ratio(numer, denom):
    """Returns floating ratio of numerator and denominator"""
    try:
        return round(numer / float(denom), 3)
    except ZeroDivisionError:
        return 0.00


def arg_parser():
    """Parse the command line arguments"""
    root_path = os.path.split(os.path.realpath(os.path.dirname(__file__)))[0]
    default_text_file = os.path.join(root_path, 'data', 'text-to-process.txt')
    default_stop_file = os.path.join(root_path, 'data', 'stopwords.txt')
    parser = argparse.ArgumentParser(description='Tokenizes, removes stopwords'
                                                 ' from the text file and '
                                                 'computes some stats')
    parser.add_argument('-c', '--case-sensitive', action='store_true',
                        help='Enable case sensitivity')
    parser.add_argument('filename', nargs='?', default=default_text_file,
                        help='Name of the file to be processed')
    parser.add_argument('stopfile', nargs='?', default=default_stop_file,
                        help='Stopwords file')
    return parser.parse_args()


def print_statistics(stats):
    """Prints a series of statistics of the text file"""
    print('Number of tokens:', len(stats.token_list))
    print('Number of unique-tokens:', stats.unique_tokens)
    print('Average length of tokens:', stats.average_len)
    print('Total number of chars:', len(stats.chars))
    print('Number of total tokens with stopwords removed:', stats.no_stopword_count)
    print('Number of characters that are letters: {} \n'
          'Number of characters that are numbers: {} \n'
          'Number of characters that are punctuation: {} '
          .format(stats.letters, stats.numbers, stats.punctuation))

    print('Letters to Character ratio:', stats.letter_ratio)
    print('Numbers to Character ratio:', stats.number_ratio)
    print('Punctuation to Character ratio:', stats.punctuation_ratio)


if __name__ == '__main__':
    ARGS = arg_parser()
    stats_obj = TextStatistics(ARGS.filename, ARGS.stopfile, ARGS.case_sensitive)
    print_statistics(stats_obj)
