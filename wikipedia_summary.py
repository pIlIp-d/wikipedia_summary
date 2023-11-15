import collections
import re

import jsons as jsons
import wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class Summarizer:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self._stopWords = set(stopwords.words("english"))

    def gen_summarize_from_text(self, text):
        text = text.strip()
        if text == "" or text == "\n":
            return text

        words = word_tokenize(text)
        sentences = sent_tokenize(text)

        word_frequency = collections.Counter([word for word in words if word not in self._stopWords])

        sentence_scores = dict()
        for word, freq in word_frequency.items():
            for sentence in sentences:
                if word in sentence.lower():
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += freq
                    else:
                        sentence_scores[sentence] = freq

        average_score_of_sentences = sum(sentence_scores.values()) / len(sentence_scores)

        summary = " ".join(
            sentence for sentence in sentence_scores.keys()
            if (sentence_scores[sentence] > (1.2 * average_score_of_sentences))
        )
        return summary


def get_wiki_page(site_title: str) -> str:
    return wikipedia.page(site_title, auto_suggest=False).content


def iterate_in_pairs(value_list: list):
    """
    iteration of pairs of two of value_list
    returns the pairs 0,1; 2,3; 4,5... when iterating
    """
    for i in range(len(value_list) // 2):
        yield value_list[i * 2], value_list[i * 2 + 1]


def get_json_string_of_wikipedia_summary(wiki_page_title, maximum_allowed_chars: int = 1500) -> str:
    wiki_text = get_wiki_page(wiki_page_title)

    # split topics and add headline for the first paragraph
    # headlines are represented like that '== Headline =='
    list_of_content = ["General Information"] + re.split("==+", wiki_text)

    # create headline, body pairs for all parts of the wiki page
    summarized_site = []
    s = Summarizer()
    for head, body in iterate_in_pairs(list_of_content):
        while True:
            body = s.gen_summarize_from_text(body)
            if len(body) <= maximum_allowed_chars:
                break

        if body == "" or body.replace("\n\n", "\n") == "\n":
            continue
        summarized_site.append({"heading": head.strip(), "body": body.strip()})
    return jsons.dumps(summarized_site)


if __name__ == '__main__':
    wiki_json = get_json_string_of_wikipedia_summary("Rick Astley")
    with open("output.json", "w+") as f:
        f.write(wiki_json)
