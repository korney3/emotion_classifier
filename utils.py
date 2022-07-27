from collections import Counter

from razdel import sentenize
from translate import Translator
from wiki_ru_wordnet import WikiWordnet

from fact_extractor import find_first_number_obj_with_given_num


def translate_text(text, from_lang, to_lang) -> str:
    """
    :param text: text for translation
    :param from_lang: origin language code according ISO_639-1 (see: https://en.wikipedia.org/wiki/ISO_639-1)
    :param to_lang: target language code according ISO_639-1 (see: https://en.wikipedia.org/wiki/ISO_639-1)
    :return: translated text
    """
    sentences = list(sentenize(text))
    result = ''

    for sentence in sentences:
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        result = result + translator.translate(sentence.text) + ' '

    return result


def compare_numerical_facts(source_numerical_facts, text_numerical_facts):
    error_messages = []
    for key in text_numerical_facts.keys():
        if key == "" or key == "год":
            continue
        if len(key.split()) <= 1:
            res, synonyms = check_if_key_or_synonyms_in_list(key, source_numerical_facts.keys())
        else:
            res = True
            synonyms = [key]
        if res:
            text_num_fact = text_numerical_facts[key]
            source_num_fact = []
            for synonym in synonyms:
                source_num_fact += source_numerical_facts[synonym]
            text_nums = [num_obj['number'] for num_obj in text_num_fact]
            source_nums = [num_obj['number'] for num_obj in source_num_fact]
            different_numbers = list(set(text_nums) - set(source_nums))
            if len(different_numbers) > 0:
                message = "\nФакты требуют подтверждения: \n"
                source_message = "Факты в источнике: \n"
                source_fact_texts = "\n\n".join(
                    [f"Факт: {fact['number']} {synonym}\n Текст: {fact['sentence']}" for fact in
                     source_num_fact])
                text_message = f"\n\n\nФакты в тексте: \n"
                diff_facts = [find_first_number_obj_with_given_num(text_num_fact, number) for number in
                              different_numbers]
                text_fact_texts = "\n\n".join(
                    [f"Факт: {fact['number']}  {key}\n Текст: {fact['sentence']}" for fact in diff_facts])
                error_messages.append(f"{message}{source_message}{source_fact_texts}{text_message}{text_fact_texts}")
    return error_messages


def check_if_key_or_synonyms_in_list(key, list_check):
    if key in list_check:
        return True, [key]
    wikiwordnet = WikiWordnet()
    synsets = wikiwordnet.get_synsets(key)
    synonyms = []
    for synset in synsets:
        for w in synset.get_words():
            synonyms.append(w.lemma())
    if key == "место":
        synonyms.append("строчка")
    intersection = list(set(synonyms).intersection(set(list_check)))
    if len(intersection) != 0:
        return True, intersection
    else:
        return False, [key]


def compare_ner_facts(source_ner_facts, text_ner_facts):
    ner_types = {"PER": "ЛИЧНОСТЬ",
                 "LOC": "ЛОКАЦИЯ",
                 "ORG": "ОРГАНИЗАЦИЯ"}
    error_messages = []

    for key in source_ner_facts.keys():
        source_ner_fact = source_ner_facts[key]
        if len(source_ner_fact) > 2:
            values = [fact["Normal spans"] for fact in source_ner_fact]
            counter = Counter(values)
            most_important_value = counter.most_common(1)[0][0]
            if key in text_ner_facts:
                values_text = [fact["Normal spans"] for fact in text_ner_facts[key]]
            else:
                values_text = []
            if most_important_value not in values_text:
                message = "\nВажная сущность исходного текста пропущена: \n"
                source_message = f"Сущность в источнике: {most_important_value}, тип: {ner_types[key]}\n"
                source_fact_texts = "\n\n".join(
                    [f"Текст: {fact['sentence']}" for fact in source_ner_fact])
                error_messages.append(f"{message}{source_message}{source_fact_texts}")

    for key in text_ner_facts.keys():
        if key in source_ner_facts.keys():
            text_ner_fact = text_ner_facts[key]
            source_ner_fact = source_ner_facts[key]
            text_values = [fact["Normal spans"] for fact in text_ner_fact]
            source_values = [fact["Normal spans"] for fact in source_ner_fact]
            different_values = list(set(text_values) - set(source_values))
            if len(different_values) > 0:
                if len(different_values) != 1 or different_values[0] != 'covid-19':
                    message = f"\nВ тексте появились сущности типа {ner_types[key]}, не совпадающие с сущностями этого типа в источнике: \n"

                    diff_facts = [fact for fact in text_ner_fact if
                                  fact["Normal spans"] in different_values and fact["Normal spans"] != "covid-19"]
                    text_fact_texts = "\n\n".join(
                        [f"Факт: {fact['Normal spans']} {ner_types[key]}\n Текст: {fact['sentence']}" for fact in
                         diff_facts])
                    error_messages.append(f"{message}{text_fact_texts}")
        else:
            message = f"\nВ тексте появился тип сущностей {ner_types[key]}, не представленный в источнике: \n"

            text_fact_texts = "\n\n".join(
                [f"Факт: {fact['Normal spans']} {ner_types[key]}\n Текст: {fact['sentence']}" for fact in
                 text_ner_facts[key]])
            error_messages.append(f"{message}{text_fact_texts}")
    return error_messages