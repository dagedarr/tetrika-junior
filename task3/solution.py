def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Объединяет пересекающиеся интервалы"""

    if not intervals:
        return []

    intervals.sort()  # сортируем по началу интервала
    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # есть пересечение
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)

    return merged


def split_pairs(flat_list: list[int]) -> list[list[int]]:
    """Разбивает список вида [a, b, c, d] в пары [[a, b], [c, d]]"""

    return [[flat_list[i], flat_list[i + 1]] for i in range(0, len(flat_list), 2)]


def clip_interval(interval: list[int], bounds: list[int]) -> list[int] | None:
    """Обрезает интервал по границам урока. Возвращает None, если пересечения нет."""

    start = max(interval[0], bounds[0])
    end = min(interval[1], bounds[1])
    return [start, end] if start < end else None


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil_intervals = split_pairs(intervals['pupil'])
    tutor_intervals = split_pairs(intervals['tutor'])

    # Обрезаем интервалы по границам урока
    pupil_intervals = [clip_interval(interval, lesson) for interval in pupil_intervals]
    tutor_intervals = [clip_interval(interval, lesson) for interval in tutor_intervals]
    pupil_intervals = [i for i in pupil_intervals if i]
    tutor_intervals = [i for i in tutor_intervals if i]

    # Перебираем все пары: ученик и учитель
    overlaps = []
    for p_start, p_end in pupil_intervals:
        for t_start, t_end in tutor_intervals:
            start = max(p_start, t_start)
            end = min(p_end, t_end)
            if start < end:
                overlaps.append([start, end])

    # Объединяем пересекающиеся интервалы
    merged = merge_intervals(overlaps)

    # Суммируем длительности всех интервалов
    total_time = sum(end - start for start, end in merged)
    return total_time

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
