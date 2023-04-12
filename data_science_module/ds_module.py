from typing import Tuple, List

from data_science_module.rationality_intuition.rationality_intuition_scorer import Rationality_intuition_scorer
from data_science_module.sentiment.sentiment_extractor import Sentiment_extractor


def get_sentiment_scores(text) -> List[float]:
    """
    :param text: Текст статьи(новости)
    :return:
    результаты анализа текста в виде: List ["positive": float, "negative": float, "neutral": float, "skip": float,
    "speech": float, "ratonality": float, "intuition": float]
    """

    sentiment_extractor_obj = Sentiment_extractor()
    rationality_intuition_scorer_obj = Rationality_intuition_scorer()

    sentiment_scores_dict, _ = sentiment_extractor_obj.get_sentiment_scores(text)
    rationality_intuition_scores_dict = rationality_intuition_scorer_obj.get_rationality_intuition_score(text)
    for key in rationality_intuition_scores_dict.keys():
        sentiment_scores_dict[key] = rationality_intuition_scores_dict[key]

    column_names = ["negative", "positive", "neutral", "skip", "speech", 'rationality', 'intuition']
    text_vector = [sentiment_scores_dict[column] for column in column_names]
    return text_vector

