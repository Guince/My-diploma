import pymorphy2
import math
from operator import itemgetter
from pprint import pprint
from natasha import (
    NamesExtractor,
    DatesExtractor
)
import re
import random

NUM_OF_TOPICS = 11
PUNCTUATION = ",.:;\/()!?$%^&*+=`~#"
PERCENT = 0.9
TOP = ['Адрес', 'График работы', 'Доступ к журналу', 'Инфа об учёном', 'Книги по теме', 'Мероприятия',
       'Наличие книги', 'Новые поступления', 'Опубликовать статью', 'Связь с отделом', 'Связь с человеком']

def open_entire_sample_r():
    file_0 = open("Вся выборка\Адрес библиотеки.txt", "r")
    file_1 = open("Вся выборка\График работы.txt", "r")
    file_2 = open("Вся выборка\Доступ к журналу.txt", "r")
    file_3 = open("Вся выборка\Инфа об учёном.txt", "r")
    file_4 = open("Вся выборка\Книги по теме.txt", "r")
    file_5 = open("Вся выборка\Мероприятия в библиотеке.txt", "r")
    file_6 = open("Вся выборка\Наличие книги.txt", "r")
    file_7 = open("Вся выборка\Новые поступления.txt", "r")
    file_8 = open("Вся выборка\Опубликовать статью.txt", "r")
    file_9 = open("Вся выборка\Связь с отделом.txt", "r")
    file_10 = open("Вся выборка\Связь с человеком.txt", "r")
    files = [file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10]
    return files

def open_test_file_r():
    '''Возвращает набор открытых для чтения файлов ДЛЯ ПРОВЕРКИ ТОЧНОСТИ АЛГОРИТМА'''
    file_0 = open(r"Для проверки\0 Совсем сырые запросы\Адрес библиотеки.txt", "r")
    file_1 = open(r"Для проверки\0 Совсем сырые запросы\График работы.txt", "r")
    file_2 = open(r"Для проверки\0 Совсем сырые запросы\Доступ к журналу.txt", "r")
    file_3 = open(r"Для проверки\0 Совсем сырые запросы\Инфа об учёном.txt", "r")
    file_4 = open(r"Для проверки\0 Совсем сырые запросы\Книги по теме.txt", "r")
    file_5 = open(r"Для проверки\0 Совсем сырые запросы\Мероприятия в библиотеке.txt", "r")
    file_6 = open(r"Для проверки\0 Совсем сырые запросы\Наличие книги.txt", "r")
    file_7 = open(r"Для проверки\0 Совсем сырые запросы\Новые поступления.txt", "r")
    file_8 = open(r"Для проверки\0 Совсем сырые запросы\Опубликовать статью.txt", "r")
    file_9 = open(r"Для проверки\0 Совсем сырые запросы\Связь с отделом.txt", "r")
    file_10 = open(r"Для проверки\0 Совсем сырые запросы\Связь с человеком.txt", "r")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_start_file_r():
    '''Возвращает набор открытых для чтения СОВСЕМ СЫРЫХ файлов'''
    file_0 = open(r"Для обучения\0 Совсем сырые запросы\Адрес библиотеки.txt", "r")
    file_1 = open(r"Для обучения\0 Совсем сырые запросы\График работы.txt", "r")
    file_2 = open(r"Для обучения\0 Совсем сырые запросы\Доступ к журналу.txt", "r")
    file_3 = open(r"Для обучения\0 Совсем сырые запросы\Инфа об учёном.txt", "r")
    file_4 = open(r"Для обучения\0 Совсем сырые запросы\Книги по теме.txt", "r")
    file_5 = open(r"Для обучения\0 Совсем сырые запросы\Мероприятия в библиотеке.txt", "r")
    file_6 = open(r"Для обучения\0 Совсем сырые запросы\Наличие книги.txt", "r")
    file_7 = open(r"Для обучения\0 Совсем сырые запросы\Новые поступления.txt", "r")
    file_8 = open(r"Для обучения\0 Совсем сырые запросы\Опубликовать статью.txt", "r")
    file_9 = open(r"Для обучения\0 Совсем сырые запросы\Связь с отделом.txt", "r")
    file_10 = open(r"Для обучения\0 Совсем сырые запросы\Связь с человеком.txt", "r")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_initial_file_r():
    '''Возвращает набор открытых для чтения НАЧАЛЬНЫХ файлов (с корректными пробелами)'''
    file_0 = open(r"Для обучения\1 Сырые запросы\Адрес библиотеки.txt", "r")
    file_1 = open(r"Для обучения\1 Сырые запросы\График работы.txt", "r")
    file_2 = open(r"Для обучения\1 Сырые запросы\Доступ к журналу.txt", "r")
    file_3 = open(r"Для обучения\1 Сырые запросы\Инфа об учёном.txt", "r")
    file_4 = open(r"Для обучения\1 Сырые запросы\Книги по теме.txt", "r")
    file_5 = open(r"Для обучения\1 Сырые запросы\Мероприятия в библиотеке.txt", "r")
    file_6 = open(r"Для обучения\1 Сырые запросы\Наличие книги.txt", "r")
    file_7 = open(r"Для обучения\1 Сырые запросы\Новые поступления.txt", "r")
    file_8 = open(r"Для обучения\1 Сырые запросы\Опубликовать статью.txt", "r")
    file_9 = open(r"Для обучения\1 Сырые запросы\Связь с отделом.txt", "r")
    file_10 = open(r"Для обучения\1 Сырые запросы\Связь с человеком.txt", "r")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_natasha_file_r():
    '''Возвращает набор открытых для чтения файлов ПОСЛЕ НАТАШИ'''
    file_0 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Адрес библиотеки.txt", "r")
    file_1 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\График работы.txt", "r")
    file_2 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Доступ к журналу.txt", "r")
    file_3 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Инфа об учёном.txt", "r")
    file_4 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Книги по теме.txt", "r")
    file_5 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Мероприятия в библиотеке.txt", "r")
    file_6 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Наличие книги.txt", "r")
    file_7 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Новые поступления.txt", "r")
    file_8 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Опубликовать статью.txt", "r")
    file_9 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Связь с отделом.txt", "r")
    file_10 = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Связь с человеком.txt", "r")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_tokenized_file_r():
    '''Возвращает набор открытых для чтения ТОКЕНИЗИРОВАННЫХ файлов'''
    file_0 = open(r"Для обучения\3 Токенизированные запросы\Адрес библиотеки.txt", "r")
    file_1 = open(r"Для обучения\3 Токенизированные запросы\График работы.txt", "r")
    file_2 = open(r"Для обучения\3 Токенизированные запросы\Доступ к журналу.txt", "r")
    file_3 = open(r"Для обучения\3 Токенизированные запросы\Инфа об учёном.txt", "r")
    file_4 = open(r"Для обучения\3 Токенизированные запросы\Книги по теме.txt", "r")
    file_5 = open(r"Для обучения\3 Токенизированные запросы\Мероприятия в библиотеке.txt", "r")
    file_6 = open(r"Для обучения\3 Токенизированные запросы\Наличие книги.txt", "r")
    file_7 = open(r"Для обучения\3 Токенизированные запросы\Новые поступления.txt", "r")
    file_8 = open(r"Для обучения\3 Токенизированные запросы\Опубликовать статью.txt", "r")
    file_9 = open(r"Для обучения\3 Токенизированные запросы\Связь с отделом.txt", "r")
    file_10 = open(r"Для обучения\3 Токенизированные запросы\Связь с человеком.txt", "r")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_normolized_file_r():
    '''Возвращает набор открытых для чтения НОРМАЛИЗОВАННЫХ файлов'''
    file_0 = open(r"Для обучения\4 Нормализованные запросы\Адрес библиотеки.txt", "r")
    file_1 = open(r"Для обучения\4 Нормализованные запросы\График работы.txt", "r")
    file_2 = open(r"Для обучения\4 Нормализованные запросы\Доступ к журналу.txt", "r")
    file_3 = open(r"Для обучения\4 Нормализованные запросы\Инфа об учёном.txt", "r")
    file_4 = open(r"Для обучения\4 Нормализованные запросы\Книги по теме.txt", "r")
    file_5 = open(r"Для обучения\4 Нормализованные запросы\Мероприятия в библиотеке.txt", "r")
    file_6 = open(r"Для обучения\4 Нормализованные запросы\Наличие книги.txt", "r")
    file_7 = open(r"Для обучения\4 Нормализованные запросы\Новые поступления.txt", "r")
    file_8 = open(r"Для обучения\4 Нормализованные запросы\Опубликовать статью.txt", "r")
    file_9 = open(r"Для обучения\4 Нормализованные запросы\Связь с отделом.txt", "r")
    file_10 = open(r"Для обучения\4 Нормализованные запросы\Связь с человеком.txt", "r")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_templated_file_r():
    '''Возвращает набор открытых для чтения файлов С ЗАМЕНЕННЫМИ ШАБЛОНАМИ запросы'''
    file_0_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Адрес библиотеки.txt", "r")
    file_1_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\График работы.txt", "r")
    file_2_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Доступ к журналу.txt", "r")
    file_3_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Инфа об учёном.txt", "r")
    file_4_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Книги по теме.txt", "r")
    file_5_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Мероприятия в библиотеке.txt", "r")
    file_6_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Наличие книги.txt", "r")
    file_7_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Новые поступления.txt", "r")
    file_8_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Опубликовать статью.txt", "r")
    file_9_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Связь с отделом.txt", "r")
    file_10_r = open(r"Для обучения\5 Заменили синонимы на шаблоны\Связь с человеком.txt", "r")
    return file_0_r, file_1_r, file_2_r, file_3_r, file_4_r, file_5_r, file_6_r, file_7_r, file_8_r, file_9_r, file_10_r

def open_start_file_w():
    '''Возвращает набор открытых для чтения СОВСЕМ СЫРЫХ файлов'''
    file_0 = open(r"Для обучения\0 Совсем сырые запросы\Адрес библиотеки.txt", "w")
    file_1 = open(r"Для обучения\0 Совсем сырые запросы\График работы.txt", "w")
    file_2 = open(r"Для обучения\0 Совсем сырые запросы\Доступ к журналу.txt", "w")
    file_3 = open(r"Для обучения\0 Совсем сырые запросы\Инфа об учёном.txt", "w")
    file_4 = open(r"Для обучения\0 Совсем сырые запросы\Книги по теме.txt", "w")
    file_5 = open(r"Для обучения\0 Совсем сырые запросы\Мероприятия в библиотеке.txt", "w")
    file_6 = open(r"Для обучения\0 Совсем сырые запросы\Наличие книги.txt", "w")
    file_7 = open(r"Для обучения\0 Совсем сырые запросы\Новые поступления.txt", "w")
    file_8 = open(r"Для обучения\0 Совсем сырые запросы\Опубликовать статью.txt", "w")
    file_9 = open(r"Для обучения\0 Совсем сырые запросы\Связь с отделом.txt", "w")
    file_10 = open(r"Для обучения\0 Совсем сырые запросы\Связь с человеком.txt", "w")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_test_file_w():
    '''Возвращает набор открытых для чтения СОВСЕМ СЫРЫХ файлов'''
    file_0 = open(r"Для проверки\0 Совсем сырые запросы\Адрес библиотеки.txt", "w")
    file_1 = open(r"Для проверки\0 Совсем сырые запросы\График работы.txt", "w")
    file_2 = open(r"Для проверки\0 Совсем сырые запросы\Доступ к журналу.txt", "w")
    file_3 = open(r"Для проверки\0 Совсем сырые запросы\Инфа об учёном.txt", "w")
    file_4 = open(r"Для проверки\0 Совсем сырые запросы\Книги по теме.txt", "w")
    file_5 = open(r"Для проверки\0 Совсем сырые запросы\Мероприятия в библиотеке.txt", "w")
    file_6 = open(r"Для проверки\0 Совсем сырые запросы\Наличие книги.txt", "w")
    file_7 = open(r"Для проверки\0 Совсем сырые запросы\Новые поступления.txt", "w")
    file_8 = open(r"Для проверки\0 Совсем сырые запросы\Опубликовать статью.txt", "w")
    file_9 = open(r"Для проверки\0 Совсем сырые запросы\Связь с отделом.txt", "w")
    file_10 = open(r"Для проверки\0 Совсем сырые запросы\Связь с человеком.txt", "w")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_initial_file_w():
    '''Возвращает набор открытых (созданных) для записи фвйлов, в них запищутся НАЧАЛЬНЫЕ файлы (с корректными пробелами)'''
    file_0 = open(r"Для обучения\1 Сырые запросы\Адрес библиотеки.txt", "w")
    file_1 = open(r"Для обучения\1 Сырые запросы\График работы.txt", "w")
    file_2 = open(r"Для обучения\1 Сырые запросы\Доступ к журналу.txt", "w")
    file_3 = open(r"Для обучения\1 Сырые запросы\Инфа об учёном.txt", "w")
    file_4 = open(r"Для обучения\1 Сырые запросы\Книги по теме.txt", "w")
    file_5 = open(r"Для обучения\1 Сырые запросы\Мероприятия в библиотеке.txt", "w")
    file_6 = open(r"Для обучения\1 Сырые запросы\Наличие книги.txt", "w")
    file_7 = open(r"Для обучения\1 Сырые запросы\Новые поступления.txt", "w")
    file_8 = open(r"Для обучения\1 Сырые запросы\Опубликовать статью.txt", "w")
    file_9 = open(r"Для обучения\1 Сырые запросы\Связь с отделом.txt", "w")
    file_10 = open(r"Для обучения\1 Сырые запросы\Связь с человеком.txt", "w")
    return file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10

def open_natasha_file_w():
    '''Возвращает набор открытых для записи файлов ДЛЯ НАТАШИ'''
    file_0_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Адрес библиотеки.txt", "w")
    file_1_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\График работы.txt", "w")
    file_2_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Доступ к журналу.txt", "w")
    file_3_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Инфа об учёном.txt", "w")
    file_4_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Книги по теме.txt", "w")
    file_5_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Мероприятия в библиотеке.txt", "w")
    file_6_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Наличие книги.txt", "w")
    file_7_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Новые поступления.txt", "w")
    file_8_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Опубликовать статью.txt", "w")
    file_9_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Связь с отделом.txt", "w")
    file_10_w = open(r"Для обучения\2 Заменили именованные сущности на шаблоны\Связь с человеком.txt", "w")
    return file_0_w, file_1_w, file_2_w, file_3_w, file_4_w, file_5_w, file_6_w, file_7_w, file_8_w, file_9_w, file_10_w

def open_tokenized_file_w():
    '''Возвращает набор открытых (созданных) для записи файлов, в них запищутся ТОКЕНИЗИРОВАННЫЕ запросы'''
    file_0_w = open(r"Для обучения\3 Токенизированные запросы\Адрес библиотеки.txt", "w")
    file_1_w = open(r"Для обучения\3 Токенизированные запросы\График работы.txt", "w")
    file_2_w = open(r"Для обучения\3 Токенизированные запросы\Доступ к журналу.txt", "w")
    file_3_w = open(r"Для обучения\3 Токенизированные запросы\Инфа об учёном.txt", "w")
    file_4_w = open(r"Для обучения\3 Токенизированные запросы\Книги по теме.txt", "w")
    file_5_w = open(r"Для обучения\3 Токенизированные запросы\Мероприятия в библиотеке.txt", "w")
    file_6_w = open(r"Для обучения\3 Токенизированные запросы\Наличие книги.txt", "w")
    file_7_w = open(r"Для обучения\3 Токенизированные запросы\Новые поступления.txt", "w")
    file_8_w = open(r"Для обучения\3 Токенизированные запросы\Опубликовать статью.txt", "w")
    file_9_w = open(r"Для обучения\3 Токенизированные запросы\Связь с отделом.txt", "w")
    file_10_w = open(r"Для обучения\3 Токенизированные запросы\Связь с человеком.txt", "w")
    return file_0_w, file_1_w, file_2_w, file_3_w, file_4_w, file_5_w, file_6_w, file_7_w, file_8_w, file_9_w, file_10_w

def open_normolized_file_w():
    '''Возвращает набор открытых (созданных) для записи файлов, в них запищутся НОРМАЛИЗОВАННЫЕ запросы'''
    file_0_w = open(r"Для обучения\4 Нормализованные запросы\Адрес библиотеки.txt", "w")
    file_1_w = open(r"Для обучения\4 Нормализованные запросы\График работы.txt", "w")
    file_2_w = open(r"Для обучения\4 Нормализованные запросы\Доступ к журналу.txt", "w")
    file_3_w = open(r"Для обучения\4 Нормализованные запросы\Инфа об учёном.txt", "w")
    file_4_w = open(r"Для обучения\4 Нормализованные запросы\Книги по теме.txt", "w")
    file_5_w = open(r"Для обучения\4 Нормализованные запросы\Мероприятия в библиотеке.txt", "w")
    file_6_w = open(r"Для обучения\4 Нормализованные запросы\Наличие книги.txt", "w")
    file_7_w = open(r"Для обучения\4 Нормализованные запросы\Новые поступления.txt", "w")
    file_8_w = open(r"Для обучения\4 Нормализованные запросы\Опубликовать статью.txt", "w")
    file_9_w = open(r"Для обучения\4 Нормализованные запросы\Связь с отделом.txt", "w")
    file_10_w = open(r"Для обучения\4 Нормализованные запросы\Связь с человеком.txt", "w")
    return file_0_w, file_1_w, file_2_w, file_3_w, file_4_w, file_5_w, file_6_w, file_7_w, file_8_w, file_9_w, file_10_w

def open_templated_file_w():
    '''Возвращает набор открытых (созданных) для записи файлов, в них запищутся НОРМАЛИЗОВАННЫЕ запросы'''
    file_0_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Адрес библиотеки.txt", "w")
    file_1_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\График работы.txt", "w")
    file_2_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Доступ к журналу.txt", "w")
    file_3_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Инфа об учёном.txt", "w")
    file_4_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Книги по теме.txt", "w")
    file_5_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Мероприятия в библиотеке.txt", "w")
    file_6_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Наличие книги.txt", "w")
    file_7_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Новые поступления.txt", "w")
    file_8_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Опубликовать статью.txt", "w")
    file_9_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Связь с отделом.txt", "w")
    file_10_w = open(r"Для обучения\5 Заменили синонимы на шаблоны\Связь с человеком.txt", "w")
    return file_0_w, file_1_w, file_2_w, file_3_w, file_4_w, file_5_w, file_6_w, file_7_w, file_8_w, file_9_w, file_10_w


def length_of_initial_files():
    '''Возвращает список, элементы которого - количество символов в каждом из 11 НАЧАЛЬНЫХ файлов'''
    file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10 = open_initial_file_r()
    files = [file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10]
    length_of_file = []
    for i in range(NUM_OF_TOPICS):
        length = len(files[i].read())
        length_of_file.append(length)
        files[i].close()
    return length_of_file

def length_of_tokenized_files():
    '''Возвращает список, элементы которого - количество символов в каждом из 11 ТОКЕНИЗИРОВАННЫХ файлов'''
    file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10 = open_tokenized_file_r()
    files = [file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10]
    length_of_file = []
    for i in range(NUM_OF_TOPICS):
        length = len(files[i].read())
        length_of_file.append(length)
        files[i].close()
    return length_of_file

def length_of_normolized_files():
    '''Возвращает список, элементы которого - количество символов в каждом из 11 НОРМАЛИЗОВАННЫХ файлов'''
    file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10 = open_normolized_file_r()
    files = [file_0, file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10]
    length_of_file = []
    for i in range(NUM_OF_TOPICS):
        length = len(files[i].read())
        length_of_file.append(length)
        files[i].close()
    return length_of_file

def journals():
    file = open("Синонимы/Журналы сырые - Copy.txt", 'r')
    file_w = open("Синонимы/Журналы.txt", 'w')
    for info in file:
        num_tab = info.find('\t')
        if num_tab != -1:
            info = info[:num_tab]
            file_w.write(info + '\n')


def separation():
    files = open_entire_sample_r()
    files_training_w = open_start_file_w()
    files_test_w = open_test_file_w()
    sum = number_of_requests()
    for j in range(NUM_OF_TOPICS):
        amount = sum[j]
        amount_training = round(amount * PERCENT)
        training_num = random.sample(range(amount), amount_training)    #возвращает список номеров запросов для обучающей выборки
        i = 0
        for str in files[j]:
            i += 1
            if i in training_num:
                files_training_w[j].write(str)
            else:
                files_test_w[j].write(str)

def correct_spaces_for_str(str):
    while str[0] == ' ' or str[0] == '\n':
        str = str[1:]
    line = ""
    for i in range(len(str) - 1):
        if str[i] == ' ' and str[i + 1] in ' \n,.:;!?$%^&*+=':
            line = line
        elif str[i] in ',.:;!?%^&*+=' and str[i + 1].isalpha():
            line += str[i] + ' '
        elif str[i].isalpha() and str[i + 1] in '([\\/&':
            line += str[i] + ' '
        elif str[i] in ')]\\/&' and str[i + 1].isalpha():
            line += str[i] + ' '
        else:
            line += str[i]
    line += str[len(str) - 1]
    return line

def correct_spaces():
    files = open_start_file_r()
    files_w = open_initial_file_w()

    for j in range(NUM_OF_TOPICS):
        for str in files[j]:
            line = correct_spaces_for_str(str)
            files_w[j].write(line)
        files[j].close()

def NEL_extraction_for_str(str):
    file = open("Синонимы/Сотрудники библиотеки ФИО.txt", 'r')
    extractor_names = NamesExtractor()
    extractor_dates = DatesExtractor()
    first = middle = last = first_worker = middle_worker = last_worker = None
    year = month = day = None
    new_str = str
    matches_n = extractor_names(str)
    for match in matches_n:
        start, stop = match.span
        first = match.fact.first
        middle = match.fact.middle
        last = match.fact.last
        substr = str[start:stop]
#        for worker in file:
#            matches_worker = extractor_names(worker)
#            for match_worker in matches_worker:
#                start_worker, stop_worker = match_worker.span
#                first_worker = match_worker.fact.first
#                middle_worker = match_worker.fact.middle
#                last_worker = match_worker.fact.last
#                substr_worker = str[start_worker:stop_worker]
#                if first_worker == first and last_worker == last and middle_worker == middle:
#                    new_str = substitution_for_str(new_str, substr_worker, '_фамилия_сотрудника _имя_сотрудника _отчество_сотрудника')
#                elif last_worker == last and middle_worker == middle:
#                    new_str = substitution_for_str(new_str, substr_worker, '_фамилия_сотрудника _отчество_сотрудника')
#                elif first_worker == first and last_worker == last:
#                    new_str = substitution_for_str(new_str, substr_worker, '_имя_сотрудника _фамилия_сотрудника')
#                elif first_worker == first and middle_worker == middle:
#                    new_str = substitution_for_str(new_str, substr_worker, '_имя_сотрудника _отчество_сотрудника')
#                elif first_worker == first:
#                    new_str = substitution_for_str(new_str, substr_worker, '_имя_сотрудника')
#                elif middle_worker == middle:
#                    new_str = substitution_for_str(new_str, substr_worker, '_отчество_сотрудника')
#                elif last_worker == last:
#                    new_str = substitution_for_str(new_str, substr_worker, '_фамилия_сотрудника')
        if first and last and middle:
            new_str = substitution_for_str(new_str, substr, '_фамилия _имя _отчество')
        elif last and middle:
            new_str = substitution_for_str(new_str, substr, '_фамилия _отчество')
        elif first and last:
            new_str = substitution_for_str(new_str, substr, '_имя _фамилия')
        elif first and middle:
            new_str = substitution_for_str(new_str, substr, '_имя _отчество')
        elif first:
            new_str = substitution_for_str(new_str, substr, '_имя')
        elif middle:
            new_str = substitution_for_str(new_str, substr, '_отчество')
        elif last:
            new_str = substitution_for_str(new_str, substr, '_фамилия')
    matches_d = extractor_dates(new_str)
    for match in matches_d:
        start, stop = match.span
        year = match.fact.year
        month = match.fact.month
        day = match.fact.day
        substr = new_str[start:stop]
        if year and month and day:
            new_str = substitution_for_str(new_str, substr, '_день _месяц _год')
        elif month and day:
            new_str = substitution_for_str(new_str, substr, '_день _месяц')
        elif year and month:
            new_str = substitution_for_str(new_str, substr, '_месяц _год')
        elif year and day:
            new_str = substitution_for_str(new_str, substr, '_день _год')
        elif day:
            new_str = substitution_for_str(new_str, substr, '_день')
        elif month:
            new_str = substitution_for_str(new_str, substr, '_месяц')
        elif year:
            new_str = substitution_for_str(new_str, substr, '_год')
    return new_str

def NEL_extraction():
    files = open_initial_file_r()
    files_w = open_natasha_file_w()
    extractor_names = NamesExtractor()
    extractor_dates = DatesExtractor()
    first = middle = last = None
    year = month = day = None
    for j in range(NUM_OF_TOPICS):
        for str in files[j]:
            new_str = NEL_extraction_for_str(str)
            files_w[j].write(new_str)
        files[j].close()

def tokenization_str(str):
    words = str.split()
    line = ""
    symbol = ''
    for word in words:
        for i in range(len(word)):
            symbol = word[i]
            if symbol not in PUNCTUATION:
                line += symbol
        line += ' '
    return line

def tokenization():
    '''Переписывает запросы без знаков препинания'''
    files = open_natasha_file_r()
    files_w = open_tokenized_file_w()
    symbol = ''
    for j in range(NUM_OF_TOPICS):
        for i in range(length_of_initial_files()[j]):
            symbol = files[j].read(1)
            if symbol not in PUNCTUATION:
                files_w[j].write(symbol)
        files[j].close()

def substitution_for_str(str, substr, template):
    '''В строке str заменяет подстроку substr на наблон template'''
    start = 0
    finish = 0
    while start != -1:
        start = str.lower().find(substr.lower())
        if start == -1:
            break
        finish = start + len(substr)
        str = str[:start] + template + str[finish:]
    start = 0
    finish = 0
    return str

def normalization_for_str(str):
    morph = pymorphy2.MorphAnalyzer()
    line = ""
    words = str.split()
    for word in words:
        p = morph.parse(word)[0]
        normolized_word = p.normal_form
        line += normolized_word + ' '
    return line

def normalization():
    files = open_tokenized_file_r()
    files_w = open_normolized_file_w()
    morph = pymorphy2.MorphAnalyzer()
    for j in range(NUM_OF_TOPICS):
        for str in files[j]:
            words = str.split()
            for word in words:
                p = morph.parse(word)[0]
                normolized_word = p.normal_form
                files_w[j].write(normolized_word)
                files_w[j].write(' ')
            files_w[j].write('\n')
        files[j].close()

def to_templates_for_str(str):
    '''Возвращает строку, где
    приветствие заменено на _привет,
    день недели на _день,
    гпнтб на _библиотека,
    "название книги" на _название_книга,
    название отдале на _название_отдел,
    должность сотрудника на _должность_сотрудник'''
    f_hello = open("Синонимы/Здравствуйте.txt", 'r')
    f_day = open("Синонимы/День.txt", 'r')
    f_department = open("Синонимы/Отделы библиотеки.txt", 'r')
    f_worker = open("Синонимы/Сотрудники библиотеки Должности.txt", 'r')
    for line in f_hello:
        line = line[:len(line) - 1]
        str = substitution_for_str(str, line, "_привет")
    for line in f_day:
        line = line[:len(line) - 1]
        str = substitution_for_str(str, line, "_день")
    for line in f_department:
        line = line[:len(line) - 1]
        str = substitution_for_str(str, line, "_название_отдел")
    for line in f_worker:
        line = line[:len(line) - 1]
        str = substitution_for_str(str, line, "_должность_сотрудник")
    str = re.sub(r'(\"|\'|«)(\w|\s|\d|PUNCTUATION)+(\"|\'|»)', "_название_книга", str)
    f_hello.close()
    f_day.close()
    str = substitution_for_str(str, 'гпнтба', 'библиотека')
    #str += '\n'
    return str

def to_templates():
    '''Заменяет на шаблоны приветствие, дни недели и меняет "гпнтб" на "библиотека", названиае книги'''
    files = open_normolized_file_r()
    files_w = open_templated_file_w()
    for j in range(NUM_OF_TOPICS):
        for line in files[j]:
            line = to_templates_for_str(line)
            files_w[j].write(line)
        files[j].close()

def number_of_requests():
    '''Возвращает суммарное количество собранных запросов'''
    files = open_entire_sample_r()
    number_of_requests = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum = 0
    for j in range(NUM_OF_TOPICS):
        for str in files[j]:
            sum += 1
        number_of_requests[j] = sum
        sum = 0
        files[j].close()
    #print("Количество запросов по темам: ", number_of_requests)
    return number_of_requests

def create_dictionary():
    '''Возвращает список, содержащий каждое НОРМАЛИЗОВАННОЕ слово в единственном варианте'''
    files = open_templated_file_r()
    file_dict = open("Словарь.txt", "w")
    dictionary = []
    for j in range(NUM_OF_TOPICS):
        for str in files[j]:
            words = str.split() #возвращает список слов текущей строки
            for word in words:
                if word not in dictionary:
                    dictionary.append(word)
                    file_dict.write(word + '\n')
        files[j].close()
    return dictionary

def term_frequency():
    '''Возвращает список словарей. i-ый словарь характеризует i-ый запрос, где ключ - слово, значение - его TF'''
    files = open_templated_file_r()
    tf_0 = []
    tf_1 = []
    tf_2 = []
    tf_3 = []
    tf_4 = []
    tf_5 = []
    tf_6 = []
    tf_7 = []
    tf_8 = []
    tf_9 = []
    tf_10 = []
    tfs = [tf_0, tf_1, tf_2, tf_3, tf_4, tf_5, tf_6, tf_7, tf_8, tf_9, tf_10]
    for j in range(NUM_OF_TOPICS):
        for request in files[j]:
            words = request.split() #возвращает список слов текущей строки
            count_of_words = len(words)
            actual_request = {}
            for i in range(count_of_words):
                if words[i] not in actual_request:
                    actual_request[words[i]] = words.count(words[i])/count_of_words
            tfs[j].append(actual_request)
        files[j].close()
    return tfs

def inverse_document_frequency(dictionary):
    '''Возвращает словарь, где ключ - слово, значение - его IDF'''
    files = open_templated_file_r()
    amount = number_of_requests()
    sum = 0
    for j in range(NUM_OF_TOPICS):
        sum += amount[j]
    idf = {}
    for j in range(NUM_OF_TOPICS):
        for str in files[j]:
            for word in dictionary:
                if word in str:
                    if word not in idf:
                        idf[word] = 1
                    else:
                        idf[word] += 1
        files[j].close()
    for word in dictionary:
        idf[word] = math.log2(sum/idf[word])
    return idf

def term_frequency_inverse_document_frequency(tfs, idf):
    '''Возвращает список словарей. i-ый словарь характеризует i-ый запрос, где ключ - слово, значение - его TF-IDF'''
    tf_idf_0 = []
    tf_idf_1 = []
    tf_idf_2 = []
    tf_idf_3 = []
    tf_idf_4 = []
    tf_idf_5 = []
    tf_idf_6 = []
    tf_idf_7 = []
    tf_idf_8 = []
    tf_idf_9 = []
    tf_idf_10 = []
    tf_idfs = [tf_idf_0,  tf_idf_1, tf_idf_2, tf_idf_3, tf_idf_4, tf_idf_5, tf_idf_6, tf_idf_7, tf_idf_8, tf_idf_9, tf_idf_10]
    for j in range(NUM_OF_TOPICS):
        for actual_request in tfs[j]:
            for word in actual_request:
                actual_request[word] = actual_request[word]*idf[word]
            tf_idfs[j].append(actual_request)
    print(tf_idfs)
    #print(tf_idf_0)
    return tf_idfs

def characteristic_words(tf_idfs, dictionary):
    '''Возвразает список словарей. Словарь из 10 слов, харатеризующих тему (т.е. слов с самым большим суммарным tf-idf)'''
    char_words = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]   #каждый словарь для каждого слова из dictionary хранит суммарный tf-idf, посчитанный по всей теме
    best_words = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]   #каждый словарь хранит 10 слов с наибольщим суммырнам tf-idf
    importance = 0
    for j in range(NUM_OF_TOPICS):
        for request in tf_idfs[j]:
            for word in dictionary:
                if word in request:
                    importance = request[word]
                if word not in char_words[j]:
                    char_words[j][word] = importance
                else:
                    char_words[j][word] += importance
                importance = 0
        sort = sorted(char_words[j].items(), key=itemgetter(1))
        length = len(sort)
        for i in range(10):
            best_words[j][sort[length - 1 - i][0]] = sort[length - 1 - i][1]
    #pprint(best_words)
    return char_words

def manual_check():
    separation()
    correct_spaces()
    NEL_extraction()
    tokenization()
    normalization()
    to_templates()
    dict = create_dictionary()
    tfs = term_frequency()
    idf = inverse_document_frequency(dict)
    tf_idfs = term_frequency_inverse_document_frequency(tfs, idf)
    char_words = characteristic_words(tf_idfs, dict)
    request = ''
    while request != '1':
        request = input("Чего ты хочешь?\n")
        request = correct_spaces_for_str(request)
        request = NEL_extraction_for_str(request)
        request = tokenization_str(request)
        request = normalization_for_str(request)
        request = to_templates_for_str(request)
        print(request)
        topic = request_recognition(request, char_words)
        print(TOP[topic])

def request_recognition(request, char_words):
    topics = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    words = request.split()
    for word in words:
        for j in range(NUM_OF_TOPICS):
            if word in char_words[j]:
                topics[j] += char_words[j][word]
    max = 0
    num_topic = 0
    for j in range(NUM_OF_TOPICS):
        if topics[j] > max:
            max = topics[j]
            num_topic = j
    if max == 0:
        print("Извините, я не понимаю, что вы имеете в виду. Позвоните в справочную: +7 (383) 266–92–64")
    #print("Думаю, тебя интересует: " + top[num_topic])
    #print(topics)
    return num_topic

def main():
    all_error = 0
    errors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    goods = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    number = 0
    for i in range(100):
        print(i)
        separation()
        correct_spaces()
        NEL_extraction()
        tokenization()
        normalization()
        to_templates()
        dict = create_dictionary()
        tfs = term_frequency()
        idf = inverse_document_frequency(dict)
        tf_idfs = term_frequency_inverse_document_frequency(tfs, idf)
        char_words = characteristic_words(tf_idfs, dict)
        files = open_test_file_r()
        error = 0
        good = 0
        sr_error = 0
        for j in range(NUM_OF_TOPICS):
            for str in files[j]:
                #request = input("Чего ты хочешь?\n")
                request = str
                request = correct_spaces_for_str(request)
                request = NEL_extraction_for_str(request)
                request = tokenization_str(request)
                request = normalization_for_str(request)
                request = to_templates_for_str(request)
                #print(request)
                topic = request_recognition(request, char_words)
                if topic != j:
                    #print("ошибка :(")
                    error += 1
                    errors[j] += 1
                    #print("Думаю, тебя интересует:  ", TOP[topic])
                    #print("Реально тебя интересует: ", TOP[j], '\n')
                else:
                    #print("правильно :)")
                    good += 1
                    goods[j] += 1
        number += error + good
        sr_error = error/(error + good)
        all_error += sr_error
        print("Ошибка = ", sr_error)
        #request = input("Чего ты хочешь?\n")
    for j in range(NUM_OF_TOPICS):
        errors[j] = errors[j]/(errors[j] + goods[j])
    print("Средняя ошибка: ", all_error/100)
    print("Процент ошибок по темам:", errors)
    print("Всего было проверено ", number,"запросов")

#manual_check()
#main()