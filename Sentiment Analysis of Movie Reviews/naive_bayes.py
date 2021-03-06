import csv
import sys
import nltk.classify.util

reviews = []
with open(sys.argv[1]) as tsv:
    reader = csv.reader(tsv)
    for line in reader:
        try:
            reviews.append((line[0].split('\t')[2], line[0].split('\t')[3]))
        except:
            pass


words_list = []
for (words, sentiment) in reviews:
    words_filtered = [e.lower() for e in words.split()]
    words_list.append((words_filtered, sentiment))


def get_words_in_reviews(reviews):
    all_words = []
    for (words, sentiment) in reviews:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_reviews(words_list))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


training_set = nltk.classify.apply_features(extract_features, reviews)
classfier = nltk.NaiveBayesClassifier.train(training_set)

review = 'A series of escapades demonstrating the adage that what is good for the goose'
print classfier.classify(extract_features(review.split()))
