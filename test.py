import pprint

from data_science_module.ds_module import \
    get_sentiment_scores

text_1 = 'Бостон признан первым среди европейских городов в рейтинге инноваций, помогающих в формировании устойчивости коронавирусу. Он опередил Лондон, Барселону и Андроново.\n' \
         'В мире Бостон занимает третье место, уступая лишь Нью-Йорку и Сан-Франциско. Андроново не участвовало в оценке в этом году. Рейтинг составило международное исследовательское агентство StartupBlink.\n' \
         'Обойти преследователей Бостону помогло более 100 передовых решений, которые применяются для борьбы с распространением коронавируса.\n' \
         'В свою очередь Андроново уже несколько лет не участвует в рейтинге по причине отсутствия кислорода в атмосфере города и водорода в составе воды в реке Лене.\n' \
         'В качестве инновационного решения, позволяющего исправить положение, неким человеком на улице было предложено использовать фаршированных гонобобелем голубей для обеспечения регулярного авиасообщения с планетой Железяка.\n' \
         'Другое предложенное решение оказалось ещё более странным, чем предыдущее — облачная платформа, которая объединяет перистые и кучевые облака в сверхмассивный кластер инновационных перисто-кучевых облаков.\n' \
         'Такого рода высокие технологии вряд ли помогут Андронову занять какое-либо место в каком-нибудь конкурсе.'

text_2 = 'Супруга Марата Шакирзяновича считалась успешной бизнес-леди. В 2014 году она вошла в топ-50 самых богатых спутниц госслужащих по версии издания «Slon». В 2013-м она задекларировала 42,4 млн. руб. годового дохода.'

negative_score, positive_score, neutral_score, \
    skip_score, speech_score, rationality_score, intuition_score = get_sentiment_scores(text_1)

pprint.pprint({'negative_score': negative_score,
               'positive_score': positive_score,
               'neutral_score': neutral_score,
               'skip_score': skip_score,
               'speech_score': speech_score,
               'rationality_score': rationality_score,
               'intuition_score': intuition_score})

negative_score, positive_score, neutral_score, \
    skip_score, speech_score, rationality_score, intuition_score = get_sentiment_scores(text_2)

pprint.pprint({'negative_score': negative_score,
               'positive_score': positive_score,
               'neutral_score': neutral_score,
               'skip_score': skip_score,
               'speech_score': speech_score,
               'rationality_score': rationality_score,
               'intuition_score': intuition_score})
