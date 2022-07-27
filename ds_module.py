from typing import Tuple, List

from scipy.stats import cosine

from clickbait_predictor import Clickbait_predictor
from fact_extractor import get_facts_from_text
from rationality_intuition_scorer import Rationality_intuition_scorer
from sentiment_extractor import Sentiment_extractor
from utils import translate_text, compare_numerical_facts, compare_ner_facts


def text_source_sentiment_score(text, title, text_source, title_source) -> float:  # delta_tone_vector
    """
    :param text: Текст статьи(новости)
    :param title: Заголовок новости
    :param text_source: Текст статьи(новости) источника
    :param title_source: Заголовок новости источника
    :return: sentiment distance - чем ближе к 0 - тем ближе тексты, чем ближе к 1 - тем дальше
    """
    text_vector = get_sentiment_scores(text, title)
    source_vector = get_sentiment_scores(text_source, title_source)

    # column_names = ["negative", "positive", "neutral", "skip", "speech", 'clickbait_score', 'rationality',
    # 'intuition'] text_vector = [text_scores[column] for column in column_names] source_vector = [source_scores[
    # column] for column in column_names]

    distance = cosine(text_vector, source_vector)

    return distance


def get_sentiment_scores(text, title) -> List[float]:
    """
    :param text: Текст статьи(новости)
    :param title: Заголовок новости
    :return: Текст статьи(новости) str и
    результаты анализа текста в виде: Dict ["positive": float, "negative": float, "neutral": float, "skip": float,
    "speech": float, "clickbait_score":float]
    """

    sentiment_extractor_obj = Sentiment_extractor()
    clickbait_predictor_obj = Clickbait_predictor()
    rationality_intuition_scorer_obj = Rationality_intuition_scorer()

    sentiment_scores_dict, _ = sentiment_extractor_obj.get_sentiment_scores(text)
    eng_title = translate_text(title, 'ru', 'en')
    clickbait_score = clickbait_predictor_obj.get_clickbait_score(eng_title)
    rationality_intuition_scores_dict = rationality_intuition_scorer_obj.get_rationality_intuition_score(text)
    sentiment_scores_dict['clickbait_score'] = clickbait_score
    for key in rationality_intuition_scores_dict.keys():
        sentiment_scores_dict[key] = rationality_intuition_scores_dict[key]

    column_names = ["negative", "positive", "neutral", "skip", "speech", 'clickbait_score', 'rationality', 'intuition']
    text_vector = [sentiment_scores_dict[column] for column in column_names]
    return text_vector


def text_source_facts_comparison(text, text_source) -> Tuple[float, float, str]:
    """
    :param text: Текст статьи(новости)
    :param text_source: Текст статьи(новости) источника
    :return: list of error messages для фактов-числительных and list of errors messages для фактов-объектов
    """
    text_numerical_facts, text_ner_facts = get_facts_from_text(text)
    source_numerical_facts, source_ner_facts = get_facts_from_text(text_source)
    numerical_error_messages = compare_numerical_facts(
        source_numerical_facts,
        text_numerical_facts)

    ner_error_messages = compare_ner_facts(source_ner_facts, text_ner_facts)

    if len(text_numerical_facts) != 0:
        error_numerical_facts_score = len(numerical_error_messages)  # / len(text_numerical_facts)
    else:
        error_numerical_facts_score = 1

    if len(text_ner_facts) != 0:
        error_ner_facts_score = len(ner_error_messages)  # / len(text_ner_facts)
    else:
        error_ner_facts_score = 1

    facts_message = "\n".join(numerical_error_messages + ner_error_messages)
    return error_numerical_facts_score, error_ner_facts_score, facts_message


