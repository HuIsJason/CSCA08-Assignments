'''A3. Tester for the function extract_mentions in tweets.
'''

import unittest
import tweets

class TestExtractMentions(unittest.TestCase):
    '''Tester for the function extract_mentions in tweets.
    '''

    def test_empty(self):
        '''Empty tweet.'''

        arg = ''
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_no_mention(self):
        '''Non-empty tweet with no mentions.'''

        arg = 'tweet test case'
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_all_mentions(self):
        '''Non-empty tweet with all mentions.'''

        arg = '@how @are @you @today @I @good @thanks'
        actual = tweets.extract_mentions(arg)
        expected = ['how', 'are', 'you', 'today', 'i', 'good', 'thanks']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_repeated_mentions(self):
        '''Non-empty tweet with repeated mentions.'''

        arg = 'it is @your @boy @jason @jason @jason @jason'
        actual = tweets.extract_mentions(arg)
        expected = ['your', 'boy', 'jason', 'jason', 'jason', 'jason']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_invalid_mentions(self):
        '''Non-empty tweet with an invalid mention.'''

        arg = 'omg I\'m gonna be @late for @work @tmwr @||||////\\'
        actual = tweets.extract_mentions(arg)
        expected = ['late', 'work', 'tmwr']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_all_invalid_mentions(self):
        '''Non-empty tweet with all invalid mentions.'''

        arg = '@@&#^*#@^@*&^#&@^@%^#&!, @||?|?|\/\/\/'
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_special_mentions(self):
        '''Non-empty tweet with special mentions.'''

        arg = 'it is your @\\\boy @jason_,,,,hu in this @house....!!!litttt'
        actual = tweets.extract_mentions(arg)
        expected = ['jason', 'house']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_uppercase_mentions(self):
        '''Non-empty tweet with uppercase mentions.'''

        arg = 'HELLO @WORLD IT IS A @wonderful @DAY!!!!TODAY'
        actual = tweets.extract_mentions(arg)
        expected = ['world', 'wonderful', 'day']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_ordered_mentions(self):
        '''Non-empty tweet with specifically-ordered mentions.'''

        arg = '@this is @mention1, @mention2, and the @3rdmention.'
        actual = tweets.extract_mentions(arg)
        expected = ['this', 'mention1', 'mention2', '3rdmention']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_numerical_mentions(self):
        '''Non-empty tweet with numerical mentions.'''

        arg = '@11111?????, @343523 @LOLOLOL420'
        actual = tweets.extract_mentions(arg)
        expected = ['11111', '343523', 'lololol420']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


if __name__ == '__main__':
    unittest.main(exit=False)
