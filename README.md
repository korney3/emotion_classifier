# Data Science Модуль Описание 

## Установка

### Requirements
python==3.9

```
conda create --name test_terminal_ds_module python=3.9
conda activate test_terminal_ds_module
pip install git+https://github.com/korney3/emotion_classifier
python -m dostoevsky download fasttext-social-network-model
```

## Пример использования

```
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
```


## Анализ эмоций

Модуль, отвечающий за скоринг эмоциональных аспектов текстов статьи. Состоит из трех частей: анализатора настроения текста, проверки заголовка статьи на кликбейтность и оценка рациональности\интуитивности текста. 

В нвоостях зачастую используется нейтральный стиль изложения. Появление выраженного эмоционального окраса присуще фейковым новостям. Также отличие эмоционального окраса в первоисточнике и анализируемой новости может свидетельствовать о появлении фейковости.

### Анализатор настроения текста

[Dostoevsky](https://github.com/bureaucratic-labs/dostoevsky) - библиотека, анализирующая настроение текста на русском языке. Классифицирует текст на 5 классов - негативное, позитивное и нейтральное настроение, а так же классифицирует части текста как речевой акт или в неясных случаях дает ответ "пропустить". Для каждого из 5 классов модель выдает скор от 0 до 1, скоры по 5-ти классам в сумме дают 1.

Наша гипотеза заключается в том, что появление высоких коэффициентов у негативного и позитивного классов может коррелировать с фейковостью новости.


### Оценка рациональности\интуитивности текста

Для оценки рациональности и интуитивности текста были созданы корпуса слов, которые имеют характер рациональности (`доказательство, анализировать, результат и т.д`) и интуитивности (`воображать, думать, чувствовать и т.д.`). Рациональность и интуитивность оцениваются как скор от 0 до 1 - относительное количество рациональных и интуитивных терминов к количеству слов в тексте.

В новостях, где интуитивный скор высокий, а рациональный - низкий, может присутствовать больше непроверенны фактов и голословных утверждений, что  может коррелировать с фейковостью.

Подход и стартовые корпуса слов взяты из проекта [polids](https://github.com/AndreCNF/polids) и переведены модулем [translate-python](https://github.com/terryyin/translate-python) с португальского на русский.

Сейчас этот модуль находится в стадии MVP (корпуса слов ограничены), при масштабировании решения они будут расширены.
