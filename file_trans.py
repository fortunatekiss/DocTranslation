#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 21:35
# @Author  : Rebekah Jiang
# @File    : file_trans.py
# @Software: PyCharm

import os
from docx import Document
import pdbc
from file_type_convert import file_type_convert
from openpyxl import load_workbook
from cutString import cutString
from clean_f import clean_f
from merge import merge
from config import Config
from utils import Utils
import threading
import math
import time
from doc_trans import DocTrans
from excel_trans import ExcelTrans
from pdf_trans import PdfTrans
from txt_trans import TxtTrans

class fileTrans(object):
    def __init__(self):
        self.p = pdbc.PdbcConnector()
        self.file_convert = file_type_convert()
        self.cutString = cutString()
        self.clean_f = clean_f()
        self.merge = merge()
        self.utils = Utils()

        self.doc_trans = DocTrans()
        self.excel_trans = ExcelTrans()
        self.pdf_trans = PdfTrans()
        self.txt_trans = TxtTrans()

    def fileTransThread(self, document_id, user_id, document_save_name, src_lang, tgt_lang, document_name, document_size):
        file_type = os.path.splitext(document_save_name)[1]

        if file_type == '.doc' or file_type == '.docx':
            path, document_save_name = self.file_convert.doc_to_docx(Config.DOC_UPLOAD_FOLDER, document_save_name)
            self.doc_trans.docTrans(path, document_save_name, src_lang, tgt_lang, document_id, user_id)
        elif file_type == '.xls' or file_type == '.xlsx':
            path, document_save_name = self.file_convert.xls_to_xlsx(Config.DOC_UPLOAD_FOLDER, document_save_name)
            self.excel_trans.excelTrans(path, document_save_name, src_lang, tgt_lang, document_id, user_id)
        elif file_type == '.pdf':
            path = Config.DOC_UPLOAD_FOLDER + document_save_name
            self.pdf_trans.pdfTrans(path, document_save_name, src_lang, tgt_lang, document_id, user_id)
        elif file_type == '.txt':
            isSplit = False
            path = os.path.join(Config.DOC_UPLOAD_FOLDER, document_save_name)
            # path = Config.DOC_UPLOAD_FOLDER + document_save_name
            sub_file_nums = math.ceil(int(document_size) / 1048576)
           
            if sub_file_nums >= 2:
                isSplit = True
                split_file_names = self.utils.splitFile(path, document_id)
                fileThreads = []
                error_files = []
                for split_file_name in split_file_names:
                    txt_file_path = os.path.join(Config.DOC_SPLIT_FOLDER, document_id, split_file_name)
                    try:
                        self.txt_trans.txtTrans(txt_file_path, document_save_name, src_lang, tgt_lang, document_id, isSplit, user_id)
                    except Exception as e:
                        print("First translate error: "+ txt_file_path + " " + str(e))
                        error_files.append(txt_file_path)
                
                if len(error_files) != 0:
                    for error_file in error_files:
                        try:
                            print("TRY AGAIN: " + error_file)
                            self.txt_trans.txtTrans(error_file, document_save_name, src_lang, tgt_lang, document_id, isSplit, user_id)
                        except Exception as e:
                            print("Second translate error: "+ error_file + " " + str(e))
                            self.p.updateDocumentStatus(document_id, '3')
                    # aThread = threading.Thread(target=self.txtTrans,args=(txt_file_path, document_save_name, src_lang, tgt_lang, document_id, isSplit))
                    # fileThreads.append(aThread)
                
                # event = threading.Event()
            
                # for thread in fileThreads:
                    # thread.start()
                    # event.wait(5)
                
                # for t in fileThreads:
                    # t.join()
                
                try:
                    self.utils.concatFile(os.path.join(Config.DOC_SPLIT_FOLDER, document_id, 'concat'), document_save_name)
                except Exception as e:
                    print(e)
                    self.p.updateDocumentStatus(document_id, '3')
                # self.p.updateDocumentStatus(document_id, '2')
            else:
                try:
                    self.txt_trans.txtTrans(path, document_save_name, src_lang, tgt_lang, document_id, isSplit, user_id)
                except Exception as e:
                    print(e)
                    self.p.updateDocumentStatus(document_id, '3')

            self.p.updateDocumentStatus(document_id, '2')

        self.p.updateDocumentSaveName(document_id, document_save_name)
