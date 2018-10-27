import urllib
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize
from gender_novels.corpus import Corpus
from gender_novels.novel import Novel
import os.path
import time

def get_parser(path_to_jar, path_to_models_jar):
    """
    The jar files are too big to commit directly, so download them
    :param path_to_jar: local path to stanford-parser.jar
    :param path_to_models_jar: local path to stanford-parser-3.9.1-models.jar

    >>> parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    >>> parser == None
    False
    """

    url_to_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser.jar"
    url_to_models_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser-3.9.1-models.jar"
    if not os.path.isfile(path_to_jar):
        urllib.request.urlretrieve(url_to_jar, path_to_jar)
    if not os.path.isfile(path_to_models_jar):
        urllib.request.urlretrieve(url_to_models_jar, path_to_models_jar)

    parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)
    return parser


def parse_novel(novel, parser):
    """
    This function parses all sentences in the novel
    :param novel: Novel object we want to analyze
    :param parser: Stanford dependency parser
    :return: the counts of male and female subject and object occurrences + list of male/female
    adjectives and verbs

    >>> parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    >>> novels = Corpus('sample_novels').novels
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': None, 'text': "He told her"}
    >>> toy_novel = Novel(novel_metadata)
    >>> parse_novel(toy_novel, parser)
    (1, 0, 0, 1, [], [], [], ['told'])

    """

    sentences = sent_tokenize(novel.text.lower().replace("\n", " "))
    result = parser.raw_parse_sents(sentences)
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    tree = list(result)
    # counts = count_gender_subj_obj(tree)
    # return counts

    male_subj_count = male_obj_count = female_subj_count = female_obj_count = 0
    female_adjectives = []
    male_adjectives = []
    female_verbs = []
    male_verbs = []
    for sentence in tree:
        for triple in next(sentence).triples():
            if triple[1] == "nsubj" and triple[2][0] == "he":
                male_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "him":
                male_obj_count += 1
            if triple[1] == "nsubj" and triple[2][0] == "she":
                female_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "her":
                female_obj_count += 1
            if triple[1] == "nsubj" and triple[0][1] == "JJ":
                if triple[2][0] == "she":
                    female_adjectives.append(triple[0][0])
                elif triple[2][0] == "he":
                    male_adjectives.append(triple[0][0])
            if triple[1] == "nsubj" and triple[0][1] == "VBD":
                if triple[2][0] == "she":
                    female_verbs.append(triple[0][0])
                elif triple[2][0] == "he":
                    male_verbs.append(triple[0][0])

    return (male_subj_count, male_obj_count, female_subj_count, female_obj_count,
            female_adjectives, male_adjectives, female_verbs, male_verbs)


def test_analysis():
    """
    This function contains all analysis code to be run (previously in main function)
    """

    # parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    #
    # novels = Corpus('sample_novels').novels
    # novel = novels[0]
    # start = time.time()
    # print(parse_novel(novel, parser))
    # end = time.time()
    # print(end-start)

    parser = get_parser("assets/stanford-parser.jar",
                             "assets/stanford-parser-3.9.1-models.jar")
    novels = Corpus('sample_novels').novels
    novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter', 'corpus_name': 'sample_novels',
                      'date': '1900', 'filename': None, 'text': "He told her. She was blue as she hit the red man. She "
                                                                "ate chicken and ran. He killed "
                                                                "her. She was killed by him. "}
    toy_novel = Novel(novel_metadata)
    print(parse_novel(toy_novel, parser))


if __name__ == "__main__":
    test_analysis()
