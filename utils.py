#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 21:37
# @Author  : Rebekah Jiang
# @File    : utils.py
# @Software: PyCharm

import os
from config import Config
import urllib3, json
import PyPDF2
import requests
import pdbc
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak, Table, LongTable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY


class Utils(object):
    def __init__(self) -> None:
        self.pdbc = pdbc.PdbcConnector()

    def getNmtJson(self, src, tgt, source_list, user_id):
        if len(source_list) == 0:
            return False
        url = Config.MODEL_PATH[(src, tgt)]
        #url = self.getPath(src, tgt)
        
        try:
            postData = {
                'src': src,
                'tgt': tgt,
                'content': source_list
            }
            dicts = self.pdbc.get_user_memory_dict_by_username_langpair(user_id, src, tgt)
            if len(dicts) > 0:
                dicts = json.loads(dicts[0][1])
                postData['userdict'] = [dicts]
                
            http = urllib3.PoolManager()
            print(json.dumps(postData, ensure_ascii=False))
            res = http.request('POST', url, body=json.dumps(postData), headers={'Content-Type': 'application/json'})
            return json.loads(res.data.decode('utf-8'))['trans_result']
        except Exception as e:
            print(e)
            print(json.dumps(postData))
            #print(json.loads(res.data.decode('utf-8')))
            return False

    def splitFile(self, upload_file, document_id):
        split_path = os.path.join(Config.DOC_SPLIT_FOLDER, document_id)
        os.mkdir(split_path)
        split_comm = 'split -l 2000 ' + upload_file + ' -d ' + split_path + '/'
        # split_comm = 'split -b 1M ' + upload_file + ' -d -a 2 ' + split_path + '/'
        os.system(split_comm)
        split_file_names = os.listdir(split_path)
        print(split_file_names)
        os.mkdir(os.path.join(split_path, 'concat'))
        # os.system('split -b 1M 1634092594.txt -d -a 2 split/')
        return split_file_names

    def concatFile(self, split_file, document_save_name):
        print(os.listdir(split_file))
        cat_comm = 'cat ' + split_file + '/* > ' + os.path.join(Config.DOC_RESULT_FOLDER, document_save_name)
        os.system(cat_comm)
        
    # def convertFileEncoding(self, file_name_list, source_dir, target_dir):
    #     for file_name in file_name_list:
    #         convert_comm = 'iconv -f latin1 -t UTF-8 01 -o 011'
        


    def splitPDF(self, file_path, save_path, start_page, end_page):
        try:
            pdfFile = open(file_path, 'rb')

            pdfReader = PyPDF2.PdfFileReader(pdfFile)

            pdfWriter = PyPDF2.PdfFileWriter()
            for index in range(start_page, end_page):
                pageObj = pdfReader.getPage(index)
                pdfWriter.addPage(pageObj)
                # ?????????????????????????????????????????????
            pdfWriter.write(open(save_path, 'wb'))
            return True
        except Exception as e:
            print(e)
            return False
    
    def pdf_recognize(self, src, img_data):
        try:
            url = Config.PDF_RECOGNIZE_URL
            
            response = requests.request("POST", url, data=img_data)

            print(response.text)
            return json.loads(response.text)
        except Exception as e:
            print(e)
            return False

    def generate_pdf(self, file_path, file_name, pages):
        try:
            pdfmetrics.registerFont(TTFont('simhei', os.path.join(Config.PDF_FONTS, 'simhei.ttf')))  # ??????????????????????????????????????????
            stylesheet = getSampleStyleSheet()  # ???????????????
            stylesheet.add(
            ParagraphStyle(name='body',
                           fontName="simhei",
                           fontSize=10,
                           textColor='black',
                           leading=20,  # ?????????
                           spaceBefore=0,  # ????????????
                           spaceAfter=10,  # ????????????
                           leftIndent=0,  # ?????????
                           rightIndent=0,  # ?????????
                           firstLineIndent=20,  # ??????????????????????????????10
                           alignment=TA_JUSTIFY,  # ????????????

                       # bulletFontSize=15,       #bullet??????????????????????????????
                       # bulletIndent=-50,
                       # bulletAnchor='start',
                       # bulletFontName='Symbol'
                       )
            )
            body = stylesheet['body']
            story = []
            # content = "ABCDFED"
            for content in pages:
                for para in content:
                    story.append(Paragraph(para['trans_text'], body))
                story.append(PageBreak())
            doc = SimpleDocTemplate(os.path.join(file_path, file_name))
            doc.build(story)
            return True
        except Exception as e:
            print(e)
            return False
