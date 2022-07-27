from IPython.display import display
from ipymarkup import show_span_ascii_markup as show_markup
from razdel import sentenize
from yargy import (
    Parser
)

from facts.number import NUMBER_FACT
from facts.number_extractor import NumberExtractor


class Fact_extractor:
    def __init__(self):
        self.number_extractor = NumberExtractor()
        self.parser = Parser(NUMBER_FACT)

    def extract_fact_from_text(self, text: str):
        fixed_text = self.number_extractor.replace_groups(text)
        matches = self.parser.findall(fixed_text)
        matches = sorted(matches, key=lambda _: _.span)
        spans = [(_.span.start, _.span.stop - 1) for _ in matches]
        facts = [_.fact for _ in matches]
        facts = self.process_facts(facts, spans, fixed_text)
        return fixed_text, facts

    def process_facts(self, facts, spans, text):
        processed_facts = {}
        sentences = list(sentenize(text))
        for fact, span in zip(facts, spans):
            if len(fact.adjs) != 0:
                fact_adjs = " ".join([" ".join(adj.parts) for adj in fact.adjs])
            else:
                fact_adjs = ""
            if len(fact.nouns) != 0:
                fact_nouns = " ".join([" ".join(noun.parts) for noun in fact.nouns])
            else:
                fact_nouns = ""
            fact_object = (fact_adjs + " " + fact_nouns).strip()

            fact_info = {"number": fact.number[0], 'start': span[0], 'end': span[1],
                         'sentence': self.get_sentence_with_fact(sentences, span)}
            if fact_object in processed_facts.keys():
                processed_facts[fact_object].append(fact_info)
            else:
                processed_facts[fact_object] = [fact_info]
        return processed_facts

    @staticmethod
    def get_sentence_with_fact(sentences, span):
        for sentence in sentences:
            if span[0] >= sentence.start and span[1] <= sentence.stop:
                return sentence.text
        return None


def show_matches(rule, *lines):
    parser = Parser(rule)
    for line in lines:
        matches = parser.findall(line)
        matches = sorted(matches, key=lambda _: _.span)
        spans = [_.span for _ in matches]
        show_markup(line, spans)
        if matches:
            facts = [_.fact for _ in matches]
            if len(facts) == 1:
                facts = facts[0]
            display(facts)


# text = "Выплаты за второго-третьего ребенка выросли на пятьсот двадцать пять тысячных процента и составили 90 тысяч рублей"

extractor = NumberExtractor()

# for match in extractor(text):
#     print(match.fact)

# print(extractor.replace(text))
# print(extractor.replace_groups(text))

# fixed_text = extractor.replace_groups(text)
#
# show_matches(NUMBER_FACT,
#              fixed_text
#              )
# fact_extractor = Fact_extractor()


text = 'Москва обошла европейские столицы в рейтинге инноваций по устойчивости к COVID-19, опередив Лондон и Барселону, сообщается на официальном сайте мэра Москвы.\nРоссийская столица также заняла третье место среди мировых мегаполисов. В пятерку лидеров вошли Бостон и Лондон.\nЗанять лидирующие позиции в рейтинге Москве помогли около 50 передовых решений, которые применяются для борьбы с распространением COVID-19.\nОдно из таких решений - алгоритмы компьютерного зрения на основе искусственного интеллекта, которые уже помогли рентгенологам проанализировать более трех миллионов исследований.\nТакже высоким результатам способствовали технологии, помогающие адаптировать жизнь москвичей во время пандемии. Среди них - проекты в сфере умного туризма, электронной коммерции и логистики, дистанционной работы и онлайн-образования.\nЭксперты оценивали, как принятые в Москве меры влияют на эпидемиологические показатели и экономику.'

text_source = 'Москва признана первой среди европейских городов в рейтинге инноваций, помогающих в формировании устойчивости коронавирусу. Она опередила Лондон и Барселону.\nСреди мировых мегаполисов российская столица занимает третью строчку — после Сан-Франциско и Нью-Йорка. Пятерку замыкают Бостон и Лондон. Рейтинг составило международное исследовательское агентство StartupBlink.\n\nДобиться высоких показателей Москве помогло почти 160 передовых решений, которые применяются для борьбы с распространением коронавируса. Среди них алгоритмы компьютерного зрения на основе искусственного интеллекта. Это методика уже помогла рентгенологам проанализировать более трех миллионов исследований.\n\nЕще одно инновационное решение — облачная платформа, которая объединяет пациентов, врачей, медицинские организации, страховые компании, фармакологические производства и сайты. Способствовали высоким результатам и технологии, которые помогают адаптировать жизнь горожан во время пандемии. Это проекты в сфере умного туризма, электронной коммерции и логистики, а также дистанционной работы и онлайн-образования.\n\nЭксперты агентства StartupBlink оценивали принятые в Москве меры с точки зрения эпидемиологических показателей и влияния на экономику.\n\nВ борьбе с коронавирусом Москва отказалась от крайностей. Ставку сделали на профилактику: увеличили количество пунктов бесплатного экспресс-тестирования и вакцинации, запатентовали онлайн-программы и платформы для обучения, развивали возможности телемедицины.\n\nМосковская система здравоохранения за время пандемии накопила достаточно большой запас прочности, который позволяет не останавливать плановую и экстренную помощь даже в периоды пиков заболеваемости COVID-19.\n\nСтолица поддерживает бизнес, выделяя субсидии и предоставляя льготы. В этом году мерами поддержки воспользовалось около 25 тысяч предприятий малого и среднего бизнеса.\n\nРейтинг составляется на базе глобальной карты инновационных решений по борьбе с коронавирусом и оценивает около 100 ведущих городов и 40 стран мира. Глобальная карта была создана в марте 2020 года, и в течение года на нее было добавлено более тысячи решений.'

# data_test = pd.read_excel("./data/output.xlsx")


results = []

# for ind, row in data_test.iterrows():
#     print(ind)
#     text_init = row["initial_text"]
#     # text_source = row["source_text"]
#     result = text_source_facts_comparison(text_init, None, None, text_source, None, None)
#     # result = check_percent_of_copy_from_source(text_init, None, None, text_source, None, None)
#     results.append(result)
#
# text_source_facts_comparison(text, None, None, text_source, None, None)
