# убираем наложения интервалов друг на друга
def del_intersections(data):
    i = 0
    while i != len(data) - 1:
        if data[i][1] >= data[i + 1][0]:
            data[i] = (min(data[i][0], data[i + 1][0]), max(data[i][1], data[i + 1][1]))
            data.pop(i + 1)
        else:
            i += 1


def appearance(intervals):
    lesson_start, lesson_stop = intervals['lesson']
    # улучшаем вид хранения интервалов, сначала собирая пары начало-конец отрезка в один список,
    # затем убирая наложения интервалов друг на друга
    pupil = intervals['pupil']
    pupil = sorted((pupil[i], pupil[i + 1]) for i in range(0, len(pupil), 2))
    del_intersections(pupil)

    tutor = intervals['tutor']
    tutor = sorted((tutor[i], tutor[i + 1]) for i in range(0, len(tutor), 2))
    del_intersections(tutor)

    # линейный алгоритм отработает за O(n+m) операций, где
    # n и m - длины списков pupil и tutor соответственно
    i, j = 0, 0
    result = []
    while i < len(pupil) and j < len(tutor):
        start, stop = max(pupil[i][0], tutor[j][0]), min(pupil[i][1], tutor[j][1])
        # если в интревале конец отрезка меньше его начала, такой нам не подходит
        # если интервал выходит за границы урока, его надо "подрезать"
        if stop >= start and stop >= lesson_start and start <= lesson_stop:
            result.append([max(start, lesson_start), min(stop, lesson_stop)])
        if pupil[i][1] < tutor[j][1]:
            i += 1
        else:
            j += 1

    return sum(interval[1] - interval[0] for interval in result)


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['data'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
