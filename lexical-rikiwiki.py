import nltk
import argparse
from nltk.corpus import wordnet
import re
from nltk.tokenize import PunktSentenceTokenizer

# /Users/dustingulley/nku/CSC-540/RikiWiki/wiki_flask/content/test2_v3.md

def combine_lines(lines, separator):
    """Combine list of strings into one string separated by the separator"""
    line = ""
    firstLine = True
    for l in lines:
        if firstLine:
            line += l
            firstLine = False
        else:
            line += (separator + l)

    return line


def get_frequency_distribution(line):
    """Get the frequency distribution of each word"""

    tokens = nltk.word_tokenize(line)
    return nltk.FreqDist(tokens)

def get_length(lines):
    """Get the length of the content of a file"""

    length = 0
    for line in lines:
        length += len(line)

    return length

def get_all_synonyms(combined_line):
    """Get the synonyms of all the words in a file"""

    unique_words = []
    synonyms = {}
    clean_synonyms = {}
    temp_word = None

    frequency = get_frequency_distribution(combined_line)
    for key, val in frequency.items():
        unique_words.append(str(key))

    for unique_word in unique_words:
        temp_word = unique_word.strip()
        if len(temp_word) > 0 and temp_word.isalpha():
            synonyms[temp_word] = []
            for synonym in wordnet.synsets(temp_word):
                for lemma in synonym.lemmas():
                    synonyms[unique_word].append(lemma.name())

    for key, val in synonyms.iteritems():
        clean_synonyms[key] = set(val)

    return clean_synonyms

def get_all_antonyms(combined_line):
    """Get the antonyms of all the words in a file"""

    unique_words = []
    synonyms = {}
    clean_synonyms = {}
    temp_word = None

    frequency = get_frequency_distribution(combined_line)
    for key, val in frequency.items():
        unique_words.append(str(key))

    for unique_word in unique_words:
        temp_word = unique_word.strip()
        if len(temp_word) > 0 and temp_word.isalpha():
            synonyms[temp_word] = []
            for antonym in wordnet.synsets(temp_word):
                for lemma in antonym.lemmas():
                    if lemma.antonyms():
                        synonyms[unique_word].append(lemma.antonyms()[0].name())

    for key, val in synonyms.iteritems():
        clean_synonyms[key] = set(val)

    return clean_synonyms

def get_clean_lines(file):
    "Removes all non alphanumeric characters from lines"
    pattern = re.compile('([^\s\w]|_)+')
    clean_lines = []
    dirty_lines = file.readlines()
    for line in dirty_lines:
        clean_lines.append(pattern.sub('', line))

    return clean_lines

def get_tagged_words(combined_line):
    tags = {
        "cc": [], "cd": [], "dt": [], "ex": [], "fw": [],
        "in": [], "jj": [], "jjr": [], "jjs": [], "ls": [], "md": [], "nn": [],
        "nns": [], "nnp": [], "nnps": [], "pdt": [], "pos": [], "prp": [],
        "prp$": [], "rb": [], "rbr": [], "rbs": [], "rp": [], "sym": [], "to": [],
        "uh": [], "vb": [], "vbd": [], "vbg": [], "vbn": [],
        "vbp": [], "vbz": [], "wdt": [], "wp": [], "wp$": [], "wrb": []
    }
    sentences = nltk.sent_tokenize(combined_line)
    tokenized_line = []

    for s in sentences:
        tokenized_line.append(nltk.pos_tag(nltk.word_tokenize(s)))

    for tagged_line in tokenized_line:
        for tl in tagged_line:
            if tl[1].lower() in tags:
                tags[tl[1].lower()].append(tl[0])

    return tags

def format_tag_message(tagged_words):
    message = ""
    first_check = True
    unique_vals = None
    tags_abbrv_name = {
        "cc": "Coordinating conjunction", "cd": "Cardinal number",
        "dt": "Determiner", "ex": "Existential there", "fw": "Foreign word",
        "in": "Preposition or subordinating", "jj": "Adjective",
        "jjr": "Adjective, comparative", "jjs": "Adjective, superlative",
        "ls": "List item marker", "md": "Modal", "nn": "Noun, singular or mass",
        "nns": "Noun, plural", "nnp": "Proper noun, singular", "nnps": "Proper noun, plural",
        "pdt": "Predeterminer", "pos": "Possessive ending", "prp": "Personal pronoun",
        "prp$": "Possessive pronoun", "rb": "Adverb", "rbr": "Adverb, comparative",
        "rbs": "Adverb, superlative", "rp": "Particle", "sym": "Symbol", "to": "To",
        "uh": "interjection", "vb": "Verb, base form", "vbd": "Verb, past tense",
        "vbg": "Verb, gerund or present", "vbn": "Verb, past participle",
        "vbp": "Verb, non-third person singular", "vbz": "Verb third-person singular",
        "wdt": "Wh-determiner", "wp": "Wh-pronoun", "wp$": "Possessive wh-pronoun",
        "wrb": "Wh-adverb"
    }
    message = "Parts of speech:\n"
    for key, vals in tagged_words.iteritems():
        if len(vals) > 0:
            message += tags_abbrv_name[key] + ": "
            unique_vals = set(vals)
            for val in unique_vals:
                if first_check:
                    message += val
                    first_check = False
                else:
                    message += ", " + val
            message += "\n"

    return message

def analyze_file(args):
    """A file is present analyze it"""

    file = args.f
    lines = get_clean_lines(file)
    combined_line = combine_lines(lines, " ")
    length = None
    message = ""
    frequency = None
    synonyms = None
    first_check = True
    antonyms = None
    tagged_words = None

    if args.fr:
        frequency = get_frequency_distribution(combined_line)
        message += "Frequency:\n"
        for key, val in frequency.items():
            message += (str(key) + ':' + str(val)) + "\n"
        message += "\n************************************\n"

    if args.l:
        length = get_length(lines)
        message += " Length: {}\n".format(length)
        message += "\n************************************\n"

    if args.s:
        synonyms = get_all_synonyms(combined_line)
        message += "Synonyms: \n"
        for key, vals in synonyms.iteritems():
            message += key + ": "
            for val in vals:
                if first_check:
                    message += val
                    first_check = False
                else:
                    message += ", " + val
            message += "\n"
            first_check = True
        first_check = True
        message += "\n************************************\n"

    if args.a:
        antonyms = get_all_antonyms(combined_line)
        message += "Antonyms: \n"
        for key, vals in antonyms.iteritems():
            message += key + ": "
            for val in vals:
                if first_check:
                    message += val
                    first_check = False
                else:
                    message += ", " + val
            message += "\n"
            first_check = True
        first_check = True
        message += "\n************************************\n"

    if args.pos:
        tagged_words = get_tagged_words(combined_line)
        message += format_tag_message(tagged_words)


    return message


if __name__ == '__main__':

    message = None  # The message to print to the user
    parser = None   # The argparse instance

    parser = argparse.ArgumentParser()  # Create the parser

    """Add the parser arguments"""
    parser.add_argument('-f', type=argparse.FileType('r'), help='Path to the wiki file.')
    parser.add_argument('-l', help='Get the length of the file content.', action="store_true")
    parser.add_argument('-fr', help='Get the word frequency distribution.', action="store_true")
    parser.add_argument('-s', help='Get synonyms for each word in the file.', action="store_true")
    parser.add_argument('-a', help='Get antonyms for each word in the file.', action="store_true")
    parser.add_argument('-pos', help='Gets part of speech tagging for each word.', action="store_true")
    args = parser.parse_args()

    if args.f is not None:
        message = analyze_file(args)
    else:
        print "Please provide a file to analyze"

    print message

