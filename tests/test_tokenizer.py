#!/usr/bin/env python
"""To run test cases on tokenizer.py"""
import os
import pytest
from tokens import tokenizer

ROOT_PATH = os.path.split(os.path.realpath(os.path.dirname(__file__)))[0]
FILENAME = os.path.join(ROOT_PATH, 'data', 'sample.txt')
STOPFILE = os.path.join(ROOT_PATH, 'data', 'sample_Stopwords.txt')


@pytest.mark.parametrize('test_input, expected_tokenlist, expected_chars',
                         [
                             ('character_data_file.txt', ['Text', 'mining'],
                              ['T', 'e', 'x', 't', ' ', 'm', 'i', 'n', 'i', 'n', 'g']),

                             ('empty.txt', [], [])
                         ])
def test_file_read(test_input, expected_tokenlist, expected_chars):
    """Test file reading and tokenizing"""
    filename = os.path.join(ROOT_PATH, 'data', test_input)
    stats = tokenizer.TextStatistics(filename, STOPFILE, False)
    assert stats.token_list == expected_tokenlist
    assert stats.chars == expected_chars


def test_read_file_not_exist():
    """Test file reading and tokenizing for Non existing files"""
    with pytest.raises(IOError):
        tokenizer.TextStatistics('dummy.txt', STOPFILE, False)


@pytest.mark.parametrize('test_input, test_input_case, expected_output',
                         [
                             ('sample_Stopwords.txt', False, {'also', 'to', 'as',
                                                              'is', 'it'}),
                             ('sample_Stopwords.txt', True, {'also', 'to', 'as',
                                                             'is', 'It'}),
                             ('sample_stop_with_duplicates.txt', True,
                              {'has', 'it', 'to', 'also', 'as', 'Was', 'is', 'Is'}),
                             ('sample_stop_with_duplicates.txt', False,
                              {'also', 'to', 'as', 'is', 'it', 'has', 'was'})
                         ])
def test_read_stop_list(test_input, test_input_case, expected_output):
    """Test reading stopwords file"""
    stopfile = os.path.join(ROOT_PATH, 'data', test_input)
    stats = tokenizer.TextStatistics(FILENAME, stopfile, test_input_case)
    assert stats.stopwords == expected_output


def test_read_None_stopfile():
    """Test for the stop file=None"""
    stats = tokenizer.TextStatistics(FILENAME, None, False)
    assert stats.stopwords == set()


def test_stopwords_file_not_exist():
    """Test reading Non existing files"""
    with pytest.raises(IOError):
        stats = tokenizer.TextStatistics(FILENAME, 'dummy.txt', False)
        stats.read_stop_list()


@pytest.mark.parametrize('test_input_tokens, test_input_case, expected_output',
                         [
                             (['This', 'list', 'has', 'duplicate', 'data', 'I',
                               'call', 'it', 'duplicate', 'List'],
                              True, 9),
                             (['This', 'list', 'has', 'duplicate', 'data', 'I',
                               'call', 'it', 'duplicate', 'List'], False, 8),
                             (['This', 'List', 'checks', 'case', 'elements',
                               'of', 'this', 'list'], True, 8),
                             (['This', 'has', 'no', 'Has', 'duplicates'], False, 4),
                             ([], False, 0)
                         ])
def test_get_unique_count(test_input_tokens, test_input_case, expected_output):
    """Test to get unique words in the text file"""
    stats = tokenizer.TextStatistics(FILENAME, STOPFILE, test_input_case)
    stats.token_list = test_input_tokens
    stats.get_unique_count()
    assert stats.unique_tokens == expected_output


@pytest.mark.parametrize('test_input, expected_output',
                         [
                             (['This', 'list', 'has', 'duplicate', 'data', 'I',
                               'call', 'it', 'duplicate', 'list'],
                              4.40),
                             (['This', 'has', 'no', 'duplicates'], 4.75),
                             ([''], 0.00),
                             ([], 0.00)
                         ])
def test_average_len(test_input, expected_output):
    """Test to compute average length of words in the text file"""
    stats = tokenizer.TextStatistics(FILENAME, None, False)
    stats.token_list = test_input
    stats.get_average_len()
    assert stats.average_len == expected_output


@pytest.mark.parametrize('test_input, letters, numbers, punctuation',
                         [
                             (['T', '0', '(', '&', '4', '!'], 1, 2, 3),
                             (['m', 'a', 'd', 'h', 'u', '%'], 5, 0, 1),
                             (['*', '!', '76', 'S', '&'], 1, 1, 3),
                             ([], 0, 0, 0)
                         ])
def test_char_type_count(test_input, letters, numbers, punctuation):
    """Test to get type of each character"""
    stats = tokenizer.TextStatistics(FILENAME, STOPFILE, False)
    stats.chars = test_input
    stats.get_char_type_count()
    assert stats.letters == letters
    assert stats.numbers == numbers
    assert stats.punctuation == punctuation


@pytest.mark.parametrize('input_tokens, input_stop_words, input_case, '
                         'tokens_with_stopwords_removed',
                         [
                             (['This', 'list', 'has?', 'duplicate', 'data',
                               'this!', 'it!?', 'duplicate', 'List'],
                              ['is', 'has', 'it', 'i', 'this', 'list'],
                              False, 3),
                             (['This', 'list', 'has?', 'duplicate', 'data',
                               'this!', 'it!?', 'duplicate', 'List'],
                              ['is', 'has', 'it', 'i', 'this', 'list'],
                              True, 5),
                             (['This', 'list', 'Has', 'It'], ['it', 'has'],
                              False, 2),
                             (['This', 'list', 'not', 'contain', 'stopping',
                               'data', 'list'], ['is', 'has', 'it', 'i'],
                              True, 7),
                             (['This', 'list', 'not', 'contain', 'stopping'],
                              ['is', 'has', 'it', 'i'], False, 5),
                             ([], ['is', 'has', 'it', 'i', 'this'],
                              True, 0)
                         ])
def test_remove_stop_words(input_tokens, input_stop_words, input_case,
                           tokens_with_stopwords_removed):
    """Test the removal of stop words from text file functionality"""
    stats = tokenizer.TextStatistics(FILENAME, STOPFILE, input_case)
    stats.token_list = input_tokens
    stats.stopwords = input_stop_words
    stats.number_of_tokens_with_stop_words_removed()
    assert stats.no_stopword_count == tokens_with_stopwords_removed


@pytest.mark.parametrize('numerator, denominator, output',
                         [
                             (4, 2, 2.00),
                             (6, 3, 2.00),
                             (4, 0, 0.00)
                         ])
def test_calc_ratio(numerator, denominator, output):
    """Test the ratio calculation"""
    assert tokenizer.calc_ratio(numerator, denominator) == output
