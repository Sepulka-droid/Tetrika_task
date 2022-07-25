import requests
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

# все животные будут собраны в словаре, сгруппированном по алфавиту
# set() нужен, чтобы убрать возможные повторения
animals = {i: set() for i in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЫЭЮЯ'}
parameters = {'title': 'Категория:Животные_по_алфавиту'}
while True:
    r = requests.get('https://ru.wikipedia.org/w/index.php', params=parameters)
    total = sum(len(animals[i]) for i in animals.keys())  # считаем, сколько собрали животных
    check = False
    last_animal = ''
    for line in r.text.split('\n'):
        # конец получения списка животных
        if '</div></div><noscript>' in line:
            check = False
        # тут получаем очередное животное
        if check:
            # выдираем из HTML-записи животное
            animal = line.split('title="')[1].split('">')[0]

            # если название животного состоит из нескольких слов, убираем все прилагательные
            # в условии задачи это явно не указано, но выглядит логично
            if len(animal.split()) > 0:
                for word in animal.split():
                    entry = morph.parse(word)[0]
                    if 'NOUN' in entry.tag:
                        animal = word
                        break

            entry = morph.parse(animal)[0]

            # если в animal находится назввания отряда, рода и т.п. (например, лжекузнечиковые),
            # не заносим в словарь
            if 'NOUN' in entry.tag:
                # также логичным выглядит привести слово к единственному числу, если оно во множественном
                animal = entry.normalized.word.capitalize()

            # в списке попадают латинские названия, по условию задачи мы их не учитываем
                if animal[0] in animals.keys():
                    animals[animal[0]].add(animal)
                    last_animal = animal
        # начало получения списка животных
        if 'Предыдущая страница' in line:
            check = True
    # если нового животного на странице не нашлось, пора прекращать скрипт
    new_start = '+'.join(last_animal.split())
    # если после очередного прогона алгоритма число животных не поменялось, пора прекращать скрипт
    new_total = sum(len(animals[i]) for i in animals.keys())
    if len(new_start) == 0 or total == new_total:
        break
    parameters = {'title': 'Категория:Животные_по_алфавиту', 'pagefrom': new_start}

# ответ к задаче:
for letter, animal_list in animals.items():
    if len(animal_list):
        print(f'{letter}: {len(animal_list)}')
