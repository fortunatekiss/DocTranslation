import os
from docx import Document
import pdbc
from file_type_convert import file_type_convert
from openpyxl import load_workbook
from config import Config
from utils import Utils
import threading
import math
import time
import PyPDF2

class PdfTrans(object):
    def __init__(self) -> None:
        self.p = pdbc.PdbcConnector()
        self.file_convert = file_type_convert()
        self.utils = Utils()
    
    def pdfTransThread(self, split_path, file_path, file_name, src, tgt, document_id, user_id):
        print("############ translate file " + file_path + " ################")
        try:
            #time.sleep(5)
            data = self.utils.pdf_recognize(src, file_path, file_name)
            data = data['data']
            all_pages = []
            for key,value in data.items():
                source_text = ""
                id_index = 0
                source_list = []
                source_len = 0
                trans_result = []
                for item in value:
                    source_text += item
                    source_len += len(item)
                    if source_len > Config.MAX_CHARACTERS:
                        data = {}
                        data['id'] = id_index
                        data['text'] = source_text
                        id_index += 1
                        source_list.append(data)
                        #time.sleep(5)
                        result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                        trans_result.extend(result)
                        source_len = 0
                        source_list = []
                        source_text = ""
                if source_len != 0:
                    data = {}
                    data['id'] = id_index
                    data['text'] = source_text
                    id_index += 1
                    source_list.append(data)
                    #time.sleep(5)
                    result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                    # print(result)
                    trans_result.extend(result)
                all_pages.append(trans_result)
                print(all_pages)
            if split_path is not None:
                result = self.utils.generate_pdf(os.path.join(split_path, 'concat'), file_name, all_pages)
            else:
                result = self.utils.generate_pdf(Config.DOC_RESULT_FOLDER, file_name, all_pages)
            if result:
                return True
            return False
        except Exception as e:
            print(e)
            self.p.updateDocumentStatus(document_id, '3')
            return False
            
    def pdfTrans(self, file_path, document_save_name, src, tgt, document_id, user_id):
        pdfFile = open(file_path, 'rb')

        pdfReader = PyPDF2.PdfFileReader(pdfFile)

        pages = pdfReader.numPages
        
        if pages > Config.PDF_MAX_PAGE:
            split_path = os.path.join(Config.DOC_SPLIT_FOLDER, document_id)
            os.mkdir(split_path)
            os.mkdir(os.path.join(split_path, 'concat'))
            temp_nums = math.ceil(pages / Config.PDF_MAX_PAGE)
            last_one = pages % Config.PDF_MAX_PAGE
            
            pdfThreads = []
            
            for index in range(0, temp_nums):
                start_page = index * Config.PDF_MAX_PAGE
                if index == temp_nums - 1 and last_one != 0:
                    end_page = index * Config.PDF_MAX_PAGE + last_one
                else:
                    end_page = (index + 1) * Config.PDF_MAX_PAGE
                #if index == temp_nums - 1:
                    #start_page = index * Config.PDF_MAX_PAGE
                    #if last_one != 0:
                        #end_page = index * Config.PDF_MAX_PAGE + last_one
                    
                #else:
                    #start_page = index * Config.PDF_MAX_PAGE
                    #end_page = (index + 1) * Config.PDF_MAX_PAGE
                print(start_page)
                print(end_page)

                pdfWriter = PyPDF2.PdfFileWriter()
                for i in range(start_page, end_page):
                    pageObj = pdfReader.getPage(i)
                    pdfWriter.addPage(pageObj)
                save_path = os.path.join(split_path, str(index) + '.pdf')
                print(save_path)
                pdfWriter.write(open(save_path, 'wb'))
                aThread = threading.Thread(target=self.pdfTransThread,
                                       args=(split_path, save_path, str(index) + '.pdf', src, tgt, document_id, user_id))
                pdfThreads.append(aThread)
            
            for thread in pdfThreads:
                time.sleep(5)
                thread.start()

            for t in pdfThreads:
                t.join()
            
            try:
                all_pdf_writer = PyPDF2.PdfFileWriter()
                for index in range(0, temp_nums):
                    concat_file_path = os.path.join(os.path.join(split_path, 'concat'), str(index) + '.pdf')
                    print(concat_file_path)
                    if os.path.exists(concat_file_path):
                        temp_pdf = open(concat_file_path, 'rb')
                        temp_pdf_reader = PyPDF2.PdfFileReader(temp_pdf)
                        for page in range(temp_pdf_reader.numPages):
                            all_pdf_writer.addPage(temp_pdf_reader.getPage(page))
                all_pdf_writer.write(open(os.path.join(Config.DOC_RESULT_FOLDER, document_save_name), 'wb'))
                    
                #self.utils.concatFile(os.path.join(split_path, 'concat'), document_save_name)
                self.p.updateDocumentStatus(document_id, '2')
            except Exception as e:
                print(e)
                self.p.updateDocumentStatus(document_id, '3')
                return False
        
        else:
            try:
                result = self.pdfTransThread(None, file_path, document_save_name, src, tgt, document_id, user_id)
                if result:
                    self.p.updateDocumentStatus(document_id, '2')
                else:
                    self.p.updateDocumentStatus(document_id, '3')
            except Exception as e:
                print(e)
                self.p.updateDocumentStatus(document_id, '3')
                return False
            