from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

class SentimentAnalysis(object):
    instance_items = 100
    subjects = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:instance_items]]
    objects = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:instance_items]]

    subject_train = subjects[:80]
    subject_test = subjects[80:100]
    object_train = objects[:80]
    object_test = objects[80:100]
    training_docs = subject_train+object_train
    testing_docs = subject_test+object_test
    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)

    trainer = NaiveBayesClassifier.train
    classifier = sentim_analyzer.train(trainer, training_set)

    def Analysis_Result(file_url):
        file = open(file_url, "r")
        content = file.read()
        content_list = tokenize.sent_tokenize(content)
        print("Analiz Başladı \n")
        print(content_list)
        print("")
        file.close()

        sentiment_intensity = SentimentIntensityAnalyzer()
        for line in content_list:
            print(line)
            sentiment_score = sentiment_intensity.polarity_scores(line)
            for k in sorted(sentiment_score):
                print('{0}: {1}, '.format(k, sentiment_score[k]), end='')
            print()