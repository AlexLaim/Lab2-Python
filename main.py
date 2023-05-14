import string
import os
import hashlib
import re
import datetime
import argparse
import fnmatch
import shlex
import numpy as np
from pydub import *

def count_chars(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        print('Исходный текст:\n' + data + '\n')
        freq = {}
        for char in data:
            if char not in string.punctuation and char.isalpha():
                char = char.lower()
                if char in freq:
                    freq[char] += 1
                else:
                    freq[char] = 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq


def zad1():
    for char, count in count_chars('russian.txt'):
        print(char, count)
    for char, count in count_chars('english.txt'):
        print(char, count)


def zad2():
    # вывести текущую директорию
    print("Текущая деректория:", os.getcwd())
    directory = input('Введите название директории, в которой необходимо проверить дубликаты: ')
    os.chdir(directory)
    # словарь для хранения контрольных сумм и списков файлов
    hash_dict = {}
    # распечатать все файлы и папки в текущем каталоге
    for dirpath, dirnames, filenames in os.walk("."):
        # перебрать каталоги
        for dirname in dirnames:
            print("Каталог:", os.path.join(dirpath, dirname))
        # перебрать файлы
        for filename in filenames:
            print("Файл:", os.path.join(dirpath, filename))
            # расчет контрольной суммы MD5 файла
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'rb') as f:
                hash_md5 = hashlib.md5(f.read()).hexdigest()

            # добавление файла в список файлов с данной контрольной суммой
            hash_dict.setdefault(hash_md5, []).append(file_path)

    # вывод дубликатов
    for key, value in hash_dict.items():
        if len(value) > 1:
            print(f"Контрольная сумма: {key}")
            print("Дубликаты:")
            for file_path in value:
                print(f"\t{file_path}")


def zad3():
    # вывести текущую директорию
    print("Текущая деректория:", os.getcwd())
    directory = input('Введите название директории, в которой находятся треки: ')
    os.chdir(directory)
    with open('PlayList.txt', 'r', encoding='utf-8') as file:
        play_list = file.read().split('\n')
        # перебрать файлы
    for filename in os.listdir():
        for new_name in play_list:
            # Извлекаем название песни из строки в формате "номер. название [длительность]"
            song_name = new_name.split('. ')[1].split(' [')[0]

            # Извлекаем расширение файла
            ext = os.path.splitext(filename)[1]

            # Склеиваем название песни и расширение файла в новое имя файла
            new_filename = new_name.split('. ')[0] + '. ' + song_name + ext

            # Переименовываем файл, если его имя совпадает с названием песни
            if song_name == os.path.splitext(filename)[0]:
                os.rename(filename, new_filename)


def zad4():
    filename = input('Введите название файла: ')
    with open(filename, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, start=1):
            for match in re.finditer(r'\(\+7\s?949\s?\)?\d{3}(-?)\d{2}\1\d{2}', line):
                print(f'Строка: {i}, позиция: {match.start()}, найдено: {match.group(0)}')


def zad5():
    text = input('Введите текст:\n')
    pattern = r'\b[A-Z][a-z]*\d{2}(?:\d{2})?\b'

    matches = re.findall(pattern, text)
    print(matches)


def zad6():
    # Директория пользователя
    print('Введите необходимые данные:\n ')
    directory = input('Директория:')
    days = input('\nДни: ')
    size = input('\nРазмер (байт):')
    small_file = False
    # Смена текущей директории
    os.chdir(directory)
    # Проход по файлам директории
    for filename in os.listdir():
        small_file = False
        # Проверка размера файла
        if os.path.isfile(filename) and os.path.getsize(filename) <= int(size):
            # Перемещение файла в папку Small
            if not os.path.exists('Source/Small'):
                os.makedirs('Source/Small')
            os.rename(filename, os.path.join('Source/Small', filename))
            small_file = True
        if not small_file:
            # Проверка даты создания файла
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
            if os.path.isfile(filename) and (datetime.datetime.now() - file_mod_time).days > int(days):
                # Перемещение файла в папку Archive
                if not os.path.exists('Source/Archive'):
                    os.makedirs('Source/Archive')
                os.rename(filename, os.path.join('Source/Archive', filename))


def zad7():

    action = input('Вызовите программу (trackmix --source "C:\Muz\Album" --count 5 --frame 15 -l -e):\n')

    if action.split()[0] != "trackmix":
        print('Для работы программы, необходимо в начале строки писать trackmxix!')
    else:
        args_list = shlex.split(action)
        args_list.pop(0)
        parser = argparse.ArgumentParser()
        parser.add_argument('--source', '-s', type=str, required='True', help='Директория с файлами')
        parser.add_argument('--destination', '-d', type=str, help='Имя выходного файла')
        parser.add_argument('--count', '-c', type=int, help='Количество файлов в нарезке')
        parser.add_argument('--frame', '-f', type=int, help='Время, которое вырезается из трека')
        parser.add_argument('--log', '-l', action='store_true', help='Лог процесса обработки файлов')
        parser.add_argument('--extended', '-e', action='store_true', help='Fade in/Fade out')


        args = parser.parse_args(args_list)
        if args.destination is None:
            args.destination = os.path.join(args.source, 'mix.mp3')
        else:
            args.destination = os.path.join(args.source, args.destination +'.mp3')

        # создаем список файлов в директории
        files = os.listdir(args.source)

        # фильтруем только файлы с расширением .mp3
        mp3_files = fnmatch.filter(files, "*.mp3")

        # создаем новый объект AudioSegment
        AudioSegment.converter = r"C:\FFmpeg\bin\ffmpeg.exe"
        AudioSegment.ffmpeg = r"C:\FFmpeg\bin\ffmpeg.exe"
        AudioSegment.ffprobe = r"C:\FFmpeg\bin\ffprobe.exe"
        new_audio = AudioSegment.empty()
        if mp3_files:
            try:
                if args.count:
                    i=1
                    count_file = mp3_files[:args.count]
                    for filename in count_file:
                        if args.log:
                            print(f"--- processing file {i}: {i.zfill(2)} - {filename}")
                        # получаем полный путь к файлу
                        file_path = os.path.join(args.source, filename)
                        file_path = file_path.replace("\\", "//")
                        # читаем файл в AudioSegment
                        # Загрузка аудиофайла с помощью pydub
                        audio = AudioSegment.from_mp3(file_path)
                        min_dur = np.min([len(audio), args.frame*1000])
                        # нарезаем отрезок звука нужной длины
                        sliced_audio = audio[:min_dur]
                        # добавляем нарезанный отрезок звука в новый объект
                        new_audio += sliced_audio
                        i += 1
                    if args.extended:
                        new_audio = new_audio.fade_in(int((new_audio.duration_seconds*1000)/2)).fade_out(int((new_audio.duration_seconds*1000)/2))
                    # экспортируем новый объект AudioSegment в файл
                    new_audio.export(args.destination, format="mp3")
                    print("--- done!")
                else:
                    i=1
                    for filename in mp3_files:
                        if args.log:
                            print(f"--- processing file {i}: {str(i).zfill(2)} - {filename}")
                        # получаем полный путь к файлу
                        file_path = os.path.join(args.source, filename)
                        file_path = file_path.replace("\\", "//")
                        # читаем файл в AudioSegment
                        # Загрузка аудиофайла с помощью pydub
                        audio = AudioSegment.from_mp3(file_path)
                        min_dur = np.min([len(audio), args.frame * 1000])
                        # нарезаем отрезок звука нужной длины
                        sliced_audio = audio[:min_dur]
                        # добавляем нарезанный отрезок звука в новый объект
                        new_audio += sliced_audio
                        # экспортируем новый объект AudioSegment в файл
                        i += 1
                    if args.extended:
                        new_audio = new_audio.fade_in((new_audio.duration_seconds+1000)/2).fade_out((new_audio.duration_seconds+1000)/2)
                    new_audio.export(args.destination, format="mp3")
                    print("--- done!")
            except Exception as e:
                print("EROR!\n"+str(e))

        else:
            print('В директории нет .mp3 файлов!')

if __name__ == '__main__':
    # zad1()
    # zad2()
    # zad3()
    # zad4()
    # zad5()
    # zad6()
    zad7()