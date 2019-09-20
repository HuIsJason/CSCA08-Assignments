"""Assignment 3: Tweet Analysis"""

from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'

# Order of data in the file
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4

# Helper functions.

def alnum_prefix(text: str) -> str:
    """Return the alphanumeric prefix of text, converted to
    lowercase. That is, return all characters in text from the
    beginning until the first non-alphanumeric character or until the
    end of text, if text does not contain any non-alphanumeric
    characters.

    >>> alnum_prefix('')
    ''
    >>> alnum_prefix('IamIamIam')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!andMore')
    'iamiamiam'
    >>> alnum_prefix('$$$money')
    ''

    """

    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[:index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.

    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'

    """

    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


def get_hashtags(tweets: Dict[str, List[tuple]]) -> List[str]:
    """Return a list of hastags used in a tweet.

    >>> d = {'Jason': [('#hello #world!', 20171108132750, \
    'Twitter for Android', 1, 4)], 'Jimmy': [('#hey guys', 20171009122851, \
    'Twitter for iPhone', 0, 3)]}
    >>> get_hashtags(d)
    {'Jason': ['hello', 'world'], 'Jimmy': ['hey']}
    >>> h = {'Sasuke': [('acquired the #Rinnegan today!', 20161009152362, \
    'Twitter for Nintendo DS', 12, 10)], 'Madara': \
    [('Revived the #Juubi today!', 20160411143675, 'Twitter for TI-84', 8, 14)]}
    >>> get_hashtags(h)
    {'Sasuke': ['rinnegan'], 'Madara': ['juubi']}

    """

    # create a dict with users referring to their hashtags they use
    user_to_hash = {}
    for user in tweets:
        user_hashtags = []
        # go thru each tuple of user
        for tup in tweets[user]:
            for hashtag in extract_hashtags(tup[TWEET_TEXT_INDEX]):
                # add hashtags in tweets of user into a list                
                user_hashtags.append(hashtag)
        # refer username to its list of hashtags
        user_to_hash[user] = user_hashtags
    return user_to_hash


def get_usernames(tweet_list: List[str]) -> List[str]:
    """Return a list of Twitter usernames from a list of tweet information.

    >>> line = ['UofTCompSci:', \
    '20181108132750,Unknown Location,Twitter for Android,0,5', \
    'RT @_AlecJacobson: @UofTCompSci St. George (Downtown) \
    Campus is hiring in Computational Geometry for a Tenure Stream Faculty \
    Position. Tell your friends!']
    >>> get_usernames(line)
    []

    """

    usernames = []
    for item in tweet_list:
        if item[:-2].isalnum() and item[-2:] == ':\n':
            usernames.append(item[:-2])
    return usernames


def get_index(lst: List[str], word: str) -> List[int]:
    """Return a list of indexes in lst where word occurs.

    >>> l = ['jason', 'hi', 'lol', 'whatup', 'jason', 'jason']
    >>> get_index(l, 'jason')
    [0, 4, 5]
    >>> d = ['1', '4', '56', '2', '4']
    >>> get_index(d, '4')
    [1, 4]

    """

    index_list = []
    for i in range(len(lst)):
        if lst[i] == word:
            index_list.append(i)
    return index_list


# Required functions

def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text, converted to lowercase, with
    duplicates included.

    >>> extract_mentions('Hi @UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many @cats$extra @meow?!')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @! here?')
    []

    """

    # make list to be returned
    mentions = []
    # convert text to list of words
    # go thru list
    for word in text.split():
        # if @ in word and is non-empty
        word_to_be_added = alnum_prefix(word[1:])
        if MENTION_SYMBOL in word and len(word_to_be_added) != 0:
            # strip @ and lower it and add it to list
            mentions.append(word_to_be_added)
    # return list
    return mentions


def extract_hashtags(tweet: str) -> List[str]:
    """Return a list of all hashtags in tweet, converted to lowercase, hashtag \
    symbol removed, non-duplicates only, and in the order they appear in tweet.

    >>> extract_hashtags('My name is #Jason and I am so #happy! today')
    ['jason', 'happy']
    >>> extract_hashtags('I study @at #UOFT, the best #uni!ever, #uoft!')
    ['uoft', 'uni']
    >>> extract_hashtags('Just finished playing basketball!!! #$$$')
    []

    """

    # make a list to be returned
    hashtags = []
    # convert tweet to list of words
    # go thru list
    for word in tweet.split():
        # if # in word and is not already in list and is non-empty
        word_to_be_added = alnum_prefix(word[1:])
        if HASH_SYMBOL in word and word_to_be_added not in hashtags and \
           len(word_to_be_added) != 0:
            # strip # and lower it and add it to list
            hashtags.append(word_to_be_added)
    # return list
    return hashtags


def count_words(tweet: str, word_dict: Dict[str, int]) -> None:
    """Modify word_dict so that its keys that represent lowercase alphanumeric \
    versions of words from tweets are updated by the amount of times they occur\
    in tweet (keys of lowercase alphanumeric hashtags, mentions, or URLs from \
    tweet are not updated). If a valid word from tweet does not have a key, \
    a key is made for it.

    >>> phrase = 'i am #jason and i am very http://happy.com'
    >>> dict = {'i': 0, 'am': 1, 'jason': 0}
    >>> count_words(phrase, dict)
    >>> dict
    {'i': 2, 'am': 3, 'jason': 0, 'and': 1, 'very': 1}
    >>> my_sentence = '#itsme over @Coachella with GIRL!!FRIEND!!'
    >>> word_counter = {'#itsme': 1, 'over': 2, 'Coachella': 0, 'girlfriend': 0}
    >>> count_words(my_sentence, word_counter)
    >>> word_counter
    {'#itsme': 1, 'over': 3, 'Coachella': 0, 'girlfriend': 1, 'with': 1}

    """

    # convert tweet into list of its words with left/right whitespace removed
    word_list = tweet.strip().split()
    # go thru list
    for word in word_list:
        # remove hashtags, mentions, and URLs
        if HASH_SYMBOL in word or MENTION_SYMBOL in word or URL_START in word:
            word_list.remove(word)
    # go thru word_list
    for i in range(len(word_list)):
        # if word of list not a key, add it to word_dict as a key referring to 0
        cleaned_word = clean_word(word_list[i])
        if cleaned_word not in word_dict:
            word_dict[cleaned_word] = 0
    # go thru word_list
    for i in range(len(word_list)):
        # add 1 to key value every time key occurs, can be multiple times
        cleaned_word = clean_word(word_list[i])
        word_dict[cleaned_word] += 1


def common_words(word_count: Dict[str, int], threshold: int) -> None:
    """Modify word_count so that it contains threshold number of the highest \
    value words. If there is a tie for the threshold'th highest number, those \
    numbers will not be included in word_count.

    >>> d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
    >>> common_words(d, 2)
    >>> d
    {'e': 4, 'f': 5}
    >>> intro = {'Hi!': 0, 'My': 1, 'name': 1, 'is': 1, 'Jason': 2, 'Hu': 3}
    >>> common_words(intro, 3)
    >>> intro
    {'Jason': 2, 'Hu': 3}

    """

    # get list of values in dict word_count
    list_of_values = list(word_count.values())
    # sort the list of values from largest to smallest
    list_of_values.sort(reverse=True)
    # remove smallest value from value list until there's threshold values
    while len(list_of_values) > threshold:
        list_of_values.remove(list_of_values[-1])
    # go thru keys of word_count
    for word in list(word_count.keys()):
        # if corresponding value not in the modified list of values, remove it
        if word_count[word] not in list_of_values:
            del word_count[word]   
    # check if length of word_count is still above threshold
    if len(word_count) > threshold:
        tied_value = min(word_count.values())
        # go thru keys of word_count
        for word in list(word_count.keys()):
            # if corresponding value equals the tied value, remove it
            if word_count[word] == tied_value:
                del word_count[word]


def read_tweets(tweets: TextIO) -> Dict[str, List[tuple]]:
    """Return a dictionary with the keys representing Twitter users, while they\
    should refer to a value of a list of tuples, in each tuple is the tweet \
    text followed by the date, location, favourite count, then retweet count.

    """

    tweets_to_dict = {}
    tweets_list = tweets.readlines()
    usernames = get_usernames(tweets_list)
    for i in range(len(usernames)):
        dict_value = []
        beginning = 1
        if (usernames[i] + ':\n') == (usernames[-1] + ':\n'):
            tweet_info = tweets_list[tweets_list.index(usernames[i] + ':\n'):]
        else:
            tweet_info = tweets_list[tweets_list.index(usernames[i] + ':\n'): \
                                 tweets_list.index(usernames[i + 1] + ':\n')]
        end_of_tweet = get_index(tweet_info, '<<<EOT\n')
        for eot in end_of_tweet:
            text = ''
            total_data = tweet_info[beginning:eot]
            information = total_data[0].split(',')
            for tweet_word in range(1, len(total_data)):
                text += total_data[tweet_word]
            dict_value += [(text.strip(), int(information[FILE_DATE_INDEX]), \
                            information[FILE_SOURCE_INDEX], \
                            int(information[FILE_FAVOURITE_INDEX]),\
                            int(information[FILE_RETWEET_INDEX].strip()))]
            beginning = eot + 1
        tweets_to_dict[clean_word(usernames[i])] = dict_value
    return tweets_to_dict


def most_popular(tweets: Dict[str, List[tuple]], beginning: int, end: int) -> \
    str:
    """Return the most popular user in tweets, based on the sum of their \
    favourite and retweet counts, in between the given date intervals.

    Precondition: beginning and end are expressed in the same integer format as\
    in the data file, and end >= beginning.

    >>> d = {'jason': [('hello world!', 20171108132750, 'Twitter for Android', \
    1, 4)], 'jimmy': [('what is up?', 20171009122851, 'Twitter for iPhone', \
    0, 3)]}
    >>> most_popular(d, 20170000000000, 20190000000000)
    'jason'
    >>> L = {'Sasuke': [('acquired the Rinnegan today!', 20161009152362, \
    'Twitter for Nintendo DS', 12, 10)], 'Madara': \
    [('Revived the Juubi today!', 20160411143675, 'Twitter for TI-84', 8, 14)]}
    >>> most_popular(L, 20160000152362, 20161109152362)
    'tie'

    """

    user_to_pop = {}
    pop_users = []
    for username in tweets:
        user_pop = []
        for tup in tweets[username]:
            # check if tweet's date is in given interval
            if beginning <= tup[TWEET_DATE_INDEX] <= end:
                user_pop.append(tup[TWEET_FAVOURITE_INDEX] + \
                                tup[TWEET_RETWEET_INDEX])
        # sum their suitable popularity counts, refer it to user in a dict
        user_to_pop[username] = sum(user_pop)
    max_pop = max(user_to_pop.values())
    # if user has the highest popularity, add it to list
    for username in user_to_pop:
        if user_to_pop[username] == max_pop:
            pop_users.append(username)
    if len(pop_users) == 1:
        return pop_users[0]
    else:
        return 'tie'


def detect_author(tweets: Dict[str, List[tuple]], unknown_tweet: str) -> str:
    """Return the most likely author of tweet unknown_tweet from dictionary \
    tweets, based on the hashtags they use and the hashtags appearing in \
    unknown_tweet.

    >>> d = {'Jason': [('#hello #world!', 20171108132750, \
    'Twitter for Android', 1, 4)], 'Jimmy': [('#hey guys', 20171009122851, \
    'Twitter for iPhone', 0, 3)]}
    >>> tweet = '#hello guys what is happening in your day?'
    >>> detect_author(d, tweet)
    'jason'
    >>> h = {'Sasuke': [('acquired the #Rinnegan today!', 20161009152362, \
    'Twitter for Nintendo DS', 12, 10)], 'Madara': \
    [('Revived the #Juubi today!', 20160411143675, 'Twitter for TI-84', 8, 14)]}
    >>> reference = '#revived my #rinnegan eye today!!!!'
    >>> detect_author(h, reference)
    'unknown'

    """

    # store hashtags of each argument into a dict and then a list, respectively
    ref_hash = extract_hashtags(unknown_tweet)
    user_to_hash = get_hashtags(tweets)
    likely_users = []
    for user in user_to_hash:
        likelihood = True        
        for hashtag in ref_hash:
            # check if each hashtag in unknown_tweet is in tweets of user
            if hashtag not in user_to_hash[user]:
                # if not a hashtag in tweets of user, they are disqualified
                likelihood = False
        # check if likelihood of user being the tweeter is true, add it a list
        if likelihood:
            likely_users.append(user.lower())
    # check if length of likely users is only 1 then return said user
    if len(likely_users) == 1:
        return likely_users[0]
    # if there are multiple or no likely users at all then return 'unknown'
    else:
        return 'unknown'


if __name__ == '__main__':
    pass

    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    import doctest
    doctest.testmod()
