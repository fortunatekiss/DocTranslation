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
from pdf2image import convert_from_path
import base64

class PdfTrans(object):
    def __init__(self) -> None:
        self.p = pdbc.PdbcConnector()
        self.file_convert = file_type_convert()
        self.utils = Utils()
    
    def pdfTransThread(self, split_path, file_path, file_name, src, tgt, document_id, user_id, document_name):
        print("############ translate file " + file_path + " ################")
        
        image = open(file_path, "rb")

        image_byte = image.read()
        img_base6 = base64.b64encode(image_byte)
        img_data = {"img":img_base6.decode('ascii'), "lang": Config.PDF_RECOGNIZE_LANG[src]}
        
        try:
            #time.sleep(5)
            data = self.utils.pdf_recognize(src, img_data)
            data = data['data']
            all_pages = []
            record_src_text = ""
            record_tgt_text = ""
            doc_save_name = os.path.split(file_path)[1]
            
            source_text = ""
            id_index = 0
            source_list = []
            source_len = 0
            source_text = ""
            trans_result = []
                
            for value in data:
                source_text += value
                source_len += len(value)
                if source_len > Config.MAX_CHARACTERS:
                    data = {}
                    data['id'] = id_index
                    data['text'] = source_text
                    record_src_text += source_text
                    id_index += 1
                    source_list.append(data)
                    result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                    if result:
                        #记录翻译内容到数据库
                        self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
                        record_src_text = ""
                        for i in result:
                            record_tgt_text += i['trans_text']
                        self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
                        record_tgt_text = ""  
                    if not result:
                        self.p.updateDocumentStatus(document_id, '3')
                        return False
                    trans_result.extend(result)
                    source_len = 0
                    source_list = []
                    source_text = ""
            if source_len != 0:
                data = {}
                data['id'] = id_index
                data['text'] = source_text
                record_src_text += source_text
                id_index += 1
                source_list.append(data)
                #time.sleep(5)
                result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                if result:
                    #记录翻译内容到数据库
                    self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
                    record_src_text = ""
                    for i in result:
                        record_tgt_text += i['trans_text']
                    self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
                    record_tgt_text = ""  
                # print(result)
                if not result:
                    self.p.updateDocumentStatus(document_id, '3')
                    return False
                trans_result.extend(result)
                all_pages.append(trans_result)
                print(all_pages)
                    
                
            # for key,value in data.items():
            #     source_text = ""
            #     id_index = 0
            #     source_list = []
            #     source_len = 0
            #     trans_result = []
            #     for item in value:
            #         source_text += item
            #         source_len += len(item)
            #         if source_len > Config.MAX_CHARACTERS:
            #             data = {}
            #             data['id'] = id_index
            #             data['text'] = source_text
            #             record_src_text += source_text
            #             id_index += 1
            #             source_list.append(data)
            #             #time.sleep(5)
            #             result = self.utils.getNmtJson(src, tgt, source_list, user_id)
            #             if result:
            #                 #记录翻译内容到数据库
            #                 self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
            #                 record_src_text = ""
            #                 if result:
            #                     for i in result:
            #                         record_tgt_text += i['trans_text']
            #                     self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
            #                     record_tgt_text = ""  
            #             if not result:
            #                 self.p.updateDocumentStatus(document_id, '3')
            #                 return False
            #             trans_result.extend(result)
            #             source_len = 0
            #             source_list = []
            #             source_text = ""
            #     if source_len != 0:
            #         data = {}
            #         data['id'] = id_index
            #         data['text'] = source_text
            #         record_src_text += source_text
            #         id_index += 1
            #         source_list.append(data)
            #         #time.sleep(5)
            #         result = self.utils.getNmtJson(src, tgt, source_list, user_id)
            #         if result:
            #             #记录翻译内容到数据库
            #             self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
            #             record_src_text = ""
            #             if result:
            #                 for i in result:
            #                     record_tgt_text += i['trans_text']
            #                 self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
            #                 record_tgt_text = ""  
            #         # print(result)
            #         if not result:
            #             self.p.updateDocumentStatus(document_id, '3')
            #             return False
            #         trans_result.extend(result)
            #     all_pages.append(trans_result)
            #     print(all_pages)
            
            
            # self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
            # record_tgt_text = ""
            # for line in trans_result:
                # record_tgt_text += line['trans_text']
            # self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
            
            pdf_file_name = os.path.splitext(file_name)[0] +'.pdf'
            if split_path is not None:
                result = self.utils.generate_pdf(os.path.join(split_path, 'concat'), pdf_file_name, all_pages)
            else:
                result = self.utils.generate_pdf(Config.DOC_RESULT_FOLDER, pdf_file_name, all_pages)
            if result:
                return True
            return False
        except Exception as e:
            print(e)
            self.p.updateDocumentStatus(document_id, '3')
            return False
    
    
    def pdfTransThreadOld(self, split_path, file_path, file_name, src, tgt, document_id, user_id, document_name):
        print("############ translate file " + file_path + " ################")
        
        image = open(file_path, "rb")

        image_byte = image.read()
        img_base6 = base64.b64encode(image_byte)
        img_data = {"img":img_base6.decode('ascii'), "lang": Config.PDF_RECOGNIZE_LANG[src]}
        
        try:
            #time.sleep(5)
            data = self.utils.pdf_recognize(src, img_data)
            data = data['data']
            all_pages = []
            record_src_text = ""
            record_tgt_text = ""
            doc_save_name = os.path.split(file_path)[1]
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
                        record_src_text += source_text
                        id_index += 1
                        source_list.append(data)
                        #time.sleep(5)
                        result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                        if result:
                            #记录翻译内容到数据库
                            self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
                            record_src_text = ""
                            if result:
                                for i in result:
                                    record_tgt_text += i['trans_text']
                                self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
                                record_tgt_text = ""  
                        if not result:
                            self.p.updateDocumentStatus(document_id, '3')
                            return False
                        trans_result.extend(result)
                        source_len = 0
                        source_list = []
                        source_text = ""
                if source_len != 0:
                    data = {}
                    data['id'] = id_index
                    data['text'] = source_text
                    record_src_text += source_text
                    id_index += 1
                    source_list.append(data)
                    #time.sleep(5)
                    result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                    if result:
                        #记录翻译内容到数据库
                        self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
                        record_src_text = ""
                        if result:
                            for i in result:
                                record_tgt_text += i['trans_text']
                            self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
                            record_tgt_text = ""  
                    # print(result)
                    if not result:
                        self.p.updateDocumentStatus(document_id, '3')
                        return False
                    trans_result.extend(result)
                all_pages.append(trans_result)
                print(all_pages)
            
            
            # self.p.record_src_text(user_id, src, tgt, record_src_text, len(record_src_text), document_name, doc_save_name, document_id)
            record_tgt_text = ""
            for line in trans_result:
                record_tgt_text += line['trans_text']
            # self.p.record_tgt_text(user_id, record_tgt_text, document_name, doc_save_name, document_id)
            
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
            
    def pdfTrans(self, file_path, document_save_name, src, tgt, document_id, user_id, document_name):
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
                                       args=(split_path, save_path, str(index) + '.pdf', src, tgt, document_id, user_id, document_name))
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
                result = self.pdfTransThread(None, file_path, document_save_name, src, tgt, document_id, user_id, document_name)
                if result:
                    self.p.updateDocumentStatus(document_id, '2')
                else:
                    self.p.updateDocumentStatus(document_id, '3')
            except Exception as e:
                print(e)
                self.p.updateDocumentStatus(document_id, '3')
                return False
            
    def pdf_trans_new(self, file_path, document_save_name, src, tgt, document_id, user_id, document_name):
        split_path = os.path.join(Config.DOC_SPLIT_FOLDER, document_id)
        os.mkdir(split_path)
        os.mkdir(os.path.join(split_path, 'concat'))
        
        im_list = convert_from_path(file_path)
        pdfThreads = []
        for i, img in enumerate(im_list):
            name = os.path.join(split_path, str(i) + ".png") 
            img.save(name)
            aThread = threading.Thread(target=self.pdfTransThread,
                                       args=(split_path, name, str(i) + '.png', src, tgt, document_id, user_id, document_name))
            pdfThreads.append(aThread)
                
        for thread in pdfThreads:
                time.sleep(5)
                thread.start()

        for t in pdfThreads:
            t.join()
            
            # res = requests.post(url=url, data=data)
            # image.close()
            # os.remove(path)
            
        try:
            all_pdf_writer = PyPDF2.PdfFileWriter()
            for index in range(0, len(im_list)):
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