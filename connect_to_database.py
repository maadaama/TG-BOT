"""
Режимы открытия файлов:
r - read - чтение (режим по-умолчанию)
w - write - запись (предыдущее содержимое файла удаляется)
a - append - ДОзапись
"""

filename = 'text.txt'


def write_to_db(user_id, grade, name, photo):
    user_id = str(user_id)
    with open(filename, 'a') as file:
        file.write(user_id)
        file.write('\t')
        file.write(grade)
        file.write('\t')
        file.write(name)
        file.write('\t')
        file.write(photo)
        file.write('\n')
    return


def get_user_from_db(my_user_id):
    with open(filename, 'r') as file:
        for line in file:
            user_id, grade, name, photo = line.strip().split('\t')
            if my_user_id == user_id:
                return {'user_id': user_id, 'class': grade, 'name': name, 'photo': photo}


if __name__ == '__main__':
    write_to_db('1234', '10н', 'Каледа Таня', 'нет фото')