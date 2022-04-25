#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 20:53
# @Author  : Rebekah Jiang
# @File    : config.py
# @Software: PyCharm
import os


class Config:
    # mySQL
    MYSQL = {
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '',
        'DATABASE': 'yuntranscopy',
        'MINSIZE': 3,
        'MAXSIZE': 5
    }

    MAX_FILE = 2
    #MAX_CHARACTERS = 18000
    MAX_CHARACTERS = 1000

    BASE_PATH = os.path.dirname(os.path.dirname(__file__))

    MODEL_CONFIG_PATH = "model.conf"

    DOC_UPLOAD_FOLDER = "/home/jiangst/sanic_test/app/documentTranslation/upload/"
    DOC_RESULT_FOLDER = "/home/jiangst/sanic_test/app/documentTranslation/translation/"
    DOC_TEMP_FOLDER = "/home/jiangst/sanic_test/app/documentTranslation/temp/"
    DOC_SPLIT_FOLDER = "/home/jiangst/sanic_test/app/documentTranslation/split/"

    MODEL_PATH = {
        ('zh', 'vi'): 'http://116.52.164.142:5001/v2/translation',
        ('vi', 'zh'): 'http://116.52.164.142:5001/v1/translation',
        ('zh', 'th'): 'http://116.52.164.142:5001/v2/translation',
        ('th', 'zh'): 'http://116.52.164.142:5001/v1/translation',
        ('zh', 'kh'): 'http://116.52.164.142:5001/v2/translation',
        ('kh', 'zh'): 'http://116.52.164.142:5001/v2/translation',
        ('zh', 'lo'): 'http://116.52.164.142:5001/v2/translation',
        ('lo', 'zh'): 'http://116.52.164.142:5001/v2/translation',
        ('zh', 'my'): 'http://116.52.164.142:5001/v2/translation',
        ('my', 'zh'): 'http://116.52.164.142:5001/v2/translation',
        ('zh', 'en'): 'http://116.52.164.142:5001/v2/translation',
        ('en', 'zh'): 'http://116.52.164.142:5001/v1/translation',
        ('zh', 'uy'): 'http://116.52.164.142:5001/v1/translation',
        ('uy', 'zh'): 'http://116.52.164.142:5001/v1/translation'
    }

    PDF_MAX_PAGE = 1
    PDF_RECOGNIZE_TYPE = 2
    PDF_RECOGNIZE_URL = "http://116.52.164.142:5002/ocr"
    #PDF_RECOGNIZE_URL = "http://yuntrans.vip:8003/api/ocr/re"
    PDF_FONTS = "/home/jiangst/YuntransDocTranslatorV1.0.SERVERPY3/fonts/"
    PDF_RECOGNIZE_LANG = {
        'my': 'mm',
        'lo': 'lao',
        'zh': 'zh',
        'th': 'th',
        'vi': 'vi',
        'en': 'en'
    }
