"""Checker for CSCA08 Assignment 3"""

import sys, io

sys.path.insert(0, './pyta')

print("================= Start: checking coding style =================")

import python_ta
python_ta.check_all('tweets.py', config='pyta/a3_pyta.txt')

print("================= End: checking coding style =================\n")

print("================= Start: checking parameter and return types =================")

import builtins
import tweets  # imported here so code that doesn't import correctly gets style checked

# Check for use of functions print and input.

our_print = print
our_input = input
our_open = open

def disable_print(*_args, **_kwargs):
    """ Notices if print is called """
    raise Exception("You must not call built-in function print!")


def disable_input(*_args, **_kwargs):
    """ Notices if input is called """
    raise Exception("You must not call built-in function input!")

def disable_open(*_args, **_kwargs):
    """ Notices if open is called """
    raise Exception("You must not call built-in function open!")

builtins.print = disable_print
builtins.input = disable_input
builtins.open = disable_open


TWEETS_DICTIONARY = {'UofTCompSci': 
                      [('#UofT Prof @ArvindUofT co-authors a '
                       'report on retraining mid-career workers for #tech\n'
                       'https://t.co/L80Ch8FUQb (via @ConversationCA)\n',
                        20180928220512, 'Hootsuite Inc.', 1, 4), 
                      ('Psst... did you know that you can pair'
                       'your studies in #compsci with just about any other '
                       'discipline in @UofTArtSci?  https://t.co/7yEzsGo26R\n',
                        20181020151013, 'Hootsuite Inc.', 9, 2)],
                     'UofTArtSci': 
                      [('Are @Uber and public transit friends or'
                        ' foes? It depends on the size of city, #UofT study '
                        'finds     https://t.co/hjG2vooQoE\n', 20181026184500,
                        'TweetDeck', 0, 0)]} 
TWEETS_FILE = io.StringIO('''UofTCompSci:
20180928220512,Unknown Location,Hootsuite Inc.,1,4
#UofT Prof @ArvindUofT co-authors a report on retraining mid-career workers for #tech
https://t.co/L80Ch8FUQb (via @ConversationCA)
<<<EOT
20181020151013,Unknown Location,Hootsuite Inc.,9,2
Psst... did you know that you can pair your studies in #compsci with just about any other discipline in @UofTArtSci?  https://t.co/7yEzsGo26R
<<<EOT
UofTArtSci:
20181026184500,Unknown Location,TweetDeck,0,0
Are @Uber and public transit friends or foes? It depends on the size of city, #UofT study finds     https://t.co/hjG2vooQoE
<<<EOT
''')

# tweets.extract_mentions
result = tweets.extract_mentions('#UofT Prof @ArvindUofT co-authors a '
                       'report on retraining mid-career workers for #tech '
                       'https://t.co/L80Ch8FUQb (via @ConversationCA)\n')
assert isinstance(result, list), \
    '''tweets.extract_mentions should return a list, but returned {0}\n'''.format(type(result))
try:
    assert isinstance(result[0], str), \
        '''tweets.extract_mentions should return a list of strings, but the first item of the list returned was a {0}
        '''.format(type(result[0]))
except IndexError:
    assert False, \
      '''The list returned by extract_mentions was empty and should have contained data.\n'''

# tweets.extract_hashtags
result = tweets.extract_hashtags('#UofT Prof @ArvindUofT co-authors a report'
                       'report on retraining mid-career workers for #tech '
                       'https://t.co/L80Ch8FUQb (via @ConversationCA)\n')
assert isinstance(result, list), \
    '''tweets.extract_hashtags should return a list, but returned {0}\n'''.format(type(result))
try:
    assert isinstance(result[0], str), \
        '''tweets.extract_hashtags should return a list of strings, but the first item of the list returned was a {0}
        '''.format(type(result[0]))
except IndexError:
    assert False, \
        '''The list returned by extract_hashtags was empty and should have contained data.\n'''

# tweets.count_words
word_d = {'computer': 1, 'day': 1}
result = tweets.count_words("#UofT researcher by day, singer @goodkidband by night", word_d)
assert isinstance(result, type(None)), \
    '''tweets.count_words should return None, but returned {0}\n'''.format(type(result))
assert len(word_d) == 6, \
    '''tweets.count_words should modify the argument dictionary\n'''

# tweets.common_words
word_d = {'statement': 10, 'regarding': 1}
result = tweets.common_words(word_d, 1)
assert isinstance(result, type(None)), \
    '''tweets.common_words should return None, but returned {0}\n'''.format(type(result))
assert len(word_d) == 1, \
    '''tweets.common_words should modify the argument dictionary'''

# tweets.read_tweets
try:
    result = tweets.read_tweets(TWEETS_FILE)
    assert isinstance(result, dict), \
        '''tweets.read_tweets should return a dict, but returned {0}\n'''.format(type(result))
    key = list(result.keys())[0]
    assert isinstance(key, str), \
        '''tweets.read_tweets should contains strings as keys, but the key we checked was a {0}
        '''.format(type(key))
    assert isinstance(result[key], list), \
        '''tweets.read_tweets should contains lists as values, but the value we checked was a {0}
        '''.format(type(result[key]))
except IndexError:
    assert False, \
        '''The dictionary returned by read_tweets was empty and should have contained data.\n'''

# tweets.most_popular
tweet_d = {key: value[:] for (key, value) in TWEETS_DICTIONARY.items()}
result = tweets.most_popular(tweet_d, 20180501000000, 20180801000000)
assert isinstance(result, str), \
    '''tweets.most_popular should return a str, but returned {0}\n'''.format(type(result))

# tweets.detect_author
tweet_d = {key: value[:] for (key, value) in TWEETS_DICTIONARY.items()}
result = tweets.detect_author(tweet_d, 'Join me! #YouIn?')
assert isinstance(result, str), \
    '''tweets.detect_author should return a str, but returned {0}\n'''.format(type(result))


builtins.print = our_print
builtins.input = our_input
builtins.open = our_open 

print("================= End: checking parameter and return types =================\n")

print("The parameter and return type checker passed.")
print("This means we will be able to test your code.")
print("It does NOT mean your code is necessarily correct.")
print("You should run your own thorough tests to convince yourself your code is correct.")
print()
print("Review the messages above to see the results of the style checking.")
