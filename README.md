# технология командной разработки ПО

Telegram бот, который позволит удобно и быстро организовать дружескую встречу. Через серию вопросов бот будет собирать предпочитаемые варианты времяпрепровождения у группы людей, далее на основе результатов опросов составлять план мероприятия.

решает проблему флуда в беседах
решает проблему нерешительности участников, берет на себя ответственность за принятие окончательных решений
не переходит на личности, что исключает наличие конфликтов в чате
позволяет оптимально выбрать параметры встречи исходя из возможностей и мнений всех участников мероприятия
предоставляет возможность не тратить время на поиски обсуждаемых предложений в общей беседе
ограничивает варианты ответов, что повышает вероятность принятия общего решения
позволяет дополнить организацию мероприятия индивидуальными опросами такими, как “кого брать тамадой?” или “кто повезет всех по домам после праздника?”
формирует всю полезную информацию в одно сообщение, оперативно оповещает всех участников об итоговом решении.

Бот использует библиотеку telegram.ext, os
Чтобы установить все зависимости надо запустить
`pip install -r requirements.txt`
Чтобы заставить бота работать нужно запустить его следующим образом:
`python main.py`
Пока работает программа, живет бот.
версия - Python 3.7.9

Status of last CI run:
![status](https://github.com/IamLena/trkpo/actions/workflows/main.yml/badge.svg)
