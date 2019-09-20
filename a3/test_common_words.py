'''A3. Tester for the function common_words in tweets.
'''

import unittest
import tweets

class TestCommonWords(unittest.TestCase):
    '''Tester for the function common_words in tweets.
    '''

    def test_empty(self):
        '''Empty dictionary.'''

        arg1 = {}
        arg2 = 1
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_one_word_limit_one(self):
        '''Dictionary with one word.'''

        arg1 = {'hello': 2}
        arg2 = 1
        exp_arg1 = {'hello': 2}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_multiple_word_limit(self):
        '''Dictionary with multiple words.'''

        arg1 = {'jason': 0, 'hu': 1, 'is': 2, 'cool': 3}
        arg2 = 3
        exp_arg1 = {'cool': 3, 'is': 2, 'hu': 1}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_multiple_word_limit_zero(self):
        '''Dictionary with multiple words and a zero-word limit.'''

        arg1 = {'rolf': 1, 'lmao': 4, 'lolz': 7}
        arg2 = 0
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_multiple_word_limit_large(self):
        '''Dictionary with multiple words and a large word limit.'''

        arg1 = {'UTSC': 12, 'UTM': 9, 'UTSG': 14}
        arg2 = 20
        exp_arg1 = {'UTSC': 12, 'UTM' : 9, 'UTSG': 14}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_multiple_word_limit_small(self):
        '''Dictionary with multiple words and a small word limit.'''

        arg1 = {'Naruto': 5, 'Sasuke': 7, 'Itachi': 9, 'Madara': 11}
        arg2 = 1
        exp_arg1 = {'Madara': 11}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_one_word_limit_large(self):
        '''Dictionary with one word and a large word limit.'''

        arg1 = {'LeBron James': 3}
        arg2 = 10
        exp_arg1 = {'LeBron James': 3}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_multiple_word_limit_tied_omit_tied(self):
        '''Dictionary with multiple words and a tie-inducing limit, removing \
        tied words.'''

        arg1 = {'Nike': 6, 'adidas': 4, 'UA': 4, 'Puma': 0}
        arg2 = 2
        exp_arg1 = {'Nike': 6}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_multiple_word_limit_tied_omit_all(self):
        '''Dictionary with multiple words and a tie-inducing limit, removing \
        all words.'''

        arg1 = {'Samsung': 3, 'Apple': 3, 'Google': 3, 'OnePlus': 1}
        arg2 = 2
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


if __name__ == '__main__':
    unittest.main(exit=False)
