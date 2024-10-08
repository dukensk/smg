from common.messages import RandomMessageGenerator


class DownloadErrorMessage(RandomMessageGenerator):
    _titles: [str] = [
        'ОЙ!',
        'ОЙ! ОЙ! ОЙ! ОЙ! ОЙ!',
        'АЙ! АЙ! АЙ! АЙ! АЙ!',
        'Ой-вей!',
        'Йоперный театр!',
        'Ядрить его в дышло!',
        'Да сколько можно?!',
        'Пристрелите меня!',
        'Убейте меня!',
        'Я так больше не могу!',
        'YOU DIED',
        'Как вы живете с таким инетом?!',
        'ѣѣ (Дабл ять)! Ну сколько можно?!',
        'Да как так-то?!',
        'Мать моя женщина!!',
        'ОМГ',
        'Это невыносимо...',
        'Нас reboot, а мы крепчаем!..',
        'Ты не поверишь!',
        'Здесь могла быть ваша реклама',
        'Продам гараж',
        'Началось в колхозе утро',
        'Я фигею в этих камышах!',
        'Да блин!',
        'Да блинский!',
        'Вот так всегда!',
        'Это какой-то позор...',
        'Врагу не сдается наш гордый "Варяг"!..',
        'Это кто-нибудь читает вообще?!',
        'Без меня вы вообще бы ничего не скачали',
        'Я буду жаловаться в ООН!',
        'Я напишу в Спортлото!',
        'В рот мне ноги!',
        'Фигня случается',
        'Такие дела',
        'Случилось некоторое дерьмо',
        'ШТОШ',
        'Мне молоко за вредность давать пора',
        'В гробу я видала такую работу!',
        'Тут такое дело',
        'Я так просто не сдамся',
        'Я обязательно выживу',
        'Этот день будет долгим',
        'Прорвемся',
        'Нас не сломить!',
        'Breaking news',
        'Ломающие новости',
        'Лядский шмель!',
        'Я вам всем покажу!',
        'Без пруда не выловишь и рыбку из него',
        'Бороться и искать, найти и перепрятать!',
        'Я что-то нажала, и все зависло',
        'Чебурнет к нам мчится',
        'Вот так всегда, на самом интересном месте!',
        'Как же все бесит!',
        'Жизнь — это боль',
        'Мы не ищем легких путей',
        'Хьюстон, у нас проблемы',
        'Лучше бы я число π до 9000 знаков после запятой считала :(',
        'Враг не пройдет',
        'Вы меня с ума сведете',
        'Вы меня в могилу сведете',
        'Это фиаско, братан',
    ]

    _texts: [str] = [
        'Что-то пошло не так, пробую возобновить загрузку',
        'Нихрена не грузится, но я пробую снова',
        'Оно не качается, но я попробую еще',
        'Опять прервалась загрузка, попробую возобновить',
        'Загрузка навернулась, пробую возобновить',
        'Враги прервали закачку, но не тут-то было. Возобновляю',
        'Опять какая-то фигня с закачкой, пробую побороть ее',
        'Cнова не качается, но это поправимо',
        'Закачка отвалилась, пробую исправить положение',
    ]


class MetadataLoadingErrorMessage(DownloadErrorMessage):
    _texts: [str] = [
        'Что-то пошло не так, пробую получить метаданные снова',
        'Метаданные не грузятся, но я попробую еще',
        'Опять не грузятся метаданные, попробую еще разок',
        'Не могу получить метаданные, пробую еще',
        'Враги мешают получить метаданные, пробую снова',
        'Враги не отдают метаданные, пробую их добыть',
        'Иллюминаты скрывают метаданные, но я докопаюсь до сути',
    ]
