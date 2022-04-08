import os
from docx import Document
import pdbc
from file_type_convert import file_type_convert
from openpyxl import load_workbook
from config import Config
from utils import Utils
import time

class TxtTrans(object):
    def __init__(self) -> None:
        self.p = pdbc.PdbcConnector()
        self.file_convert = file_type_convert()
        self.utils = Utils()
    
    def txtTrans(self, file_path, document_save_name, src, tgt, document_id, isSplit, user_id):
        print("############ translate file " + file_path + " ################")
        with open(file_path, 'r') as fr:
            id_index = 0
            source_list = []
            source_len = 0
            trans_result = []

            for source_text in fr.readlines():
                if source_text.lstrip().rstrip() != '':
                    data = {}
                    data['id'] = id_index
                    data['text'] = source_text
                    id_index += 1
                    source_list.append(data)
                    source_len += len(source_text)
                
                if source_len > Config.MAX_CHARACTERS:
                    result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                        # print(result)
                    if not result:
                        time.sleep(5)
                        result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                        if not result:
                            result = source_list
                        # try:
                        #     result = self.utils.getNmtJson(src, tgt, source_list)
                        #     # print(result)
                        # except Exception as e:
                        #     print(e)
                        #     # return False
                        #     result = source_list
                    trans_result.extend(result)
                    source_len = 0
                    source_list = []
            
            if source_len != 0:
                result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                if not result:
                    time.sleep(5)
                    result = self.utils.getNmtJson(src, tgt, source_list, user_id)
                    if not result:
                        result = source_list
                    # try:
                    #     result = self.utils.getNmtJson(src, tgt, source_list)
                    #     # print(result)
                    # except Exception as e:
                    #     print(e)
                    #     # return False
                    #     result = source_list
                trans_result.extend(result)
        
        try:
            save_path = Config.DOC_RESULT_FOLDER + document_save_name
            if isSplit:
                save_path = os.path.join(os.path.split(file_path)[0], 'concat', os.path.split(file_path)[1])
            
            with open(file_path, 'r') as fr, open(save_path, 'w') as fw:
                for source_text in fr:
                    if source_text.lstrip().rstrip() != '':
                        replace_text = trans_result[0]['trans_text'] if 'trans_text' in trans_result[0] else trans_result[0]['text']
                        source_text = source_text.replace(source_text, replace_text)
                        del (trans_result[0])
                    fw.write(source_text)
                # for tgt_text in trans_result:
                #     fw.write(tgt_text['trans_text'])
        except Exception as e:
            print(e)
            return False

        # self.p.updateDocumentStatus(document_id, '2')
        return True