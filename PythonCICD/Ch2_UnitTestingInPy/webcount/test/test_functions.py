#! python3

from webcount import most_common_word_in_webpage
from webcount.functions import most_common_word
import pytest


def test_most_common_word():
    assert most_common_word(['a', 'b', 'c'], 'abbbcc') == 'b', \
        'Bad most common word, "b" expected'

def test_most_common_word_empty_candidate():
    from pytest import raises
    with raises(Exception):
        most_common_word([], 'abc')

def test_most_common_ambiguous():
    assert most_common_word(['a', 'b', 'c'], 'aaabbbcc') in ('a', 'b'), \
        'indeterminate result'

def test_with_mock_most_common_word_in_webpage():
    from unittest.mock import Mock
    mock_requests = Mock()
    mock_requests.get.return_value.text = 'aa bbb cc'
    result = most_common_word_in_webpage(
        ['a', 'b', 'c'],
        'https://python.org',
        req_agent=mock_requests)
    assert result == 'b', 'test using mock'
    assert mock_requests.get.call_count == 1
    assert mock_requests.get.call_args[0][0] == 'https://python.org', 'incorrect url'


@pytest.mark.skip(reason="patch doesn't seem to work")
def test_with_patch_most_common_word_in_webpage():
    from unittest.mock import Mock, patch
    mock_requests = Mock()
    mock_requests.get.return_value.text = 'bbb c aa'
    with patch('webcount.functions.requests', new=mock_requests):
        result = most_common_word_in_webpage(
            ['a', 'b', 'c'], 'https://python.org')
    assert result == 'b', 'b expected, got {}'.format(result)
    assert mock_requests.get.call_count == 1
    assert mock_requests.get.call_args[0][0] == 'https://python.org', 'incorrect url'
