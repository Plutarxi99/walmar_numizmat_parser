import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def control_last_iter(type_work: str, value=None) -> int:
    """
    Для того, чтобы восстановить работу после сбоя
    Создается файл с последней итерацией
    При сбое и восстановление работы мы делаем срез на последней итераици
    И начинаем с полднего значения на чем остановились


    start = нужен для начало и создание файла last_iter.txt или чтения из файла


    write = нужен для записи в файл текущей итерации перед записью в бд
    :param type_work: start | write
    :param value: значение id аукциона
    :return: значение id аукциона, на чем остановилось
    """
    path_to_file = BASE_DIR / 'data_test/last_iter.txt'
    last_iter = 0
    if type_work == 'start':
        is_file = os.path.exists(path_to_file)
        if is_file is not True:
            with open(path_to_file, 'w') as f:
                f.write(str(last_iter))
        else:
            with open(path_to_file, 'r') as f:
                last_iter = int(f.read())

    elif type_work == 'write':
        with open(path_to_file, 'w') as f:
            f.write(value)
    else:
        raise "Не правильное передачи тип работы <start | write>"
    return last_iter