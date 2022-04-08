# -*-coding:utf-8-*-

import os
import pdbc
import time
from file_trans import fileTrans
from config import Config
from utils import Utils
import threading

if __name__ == '__main__':
    fileTrans = fileTrans()
    p = pdbc.PdbcConnector()
    utils = Utils()

    while 1:
        time.sleep(20)
        #max_file = utils.getMaxFile()
        document = p.getUnTranslatedDocument(Config.MAX_FILE)
        if not document:
            continue
        fileThreads = []
        for each_file in document:
            document_id, user_id, document_save_name, src_lang, tgt_lang, document_name, document_size = each_file
            if not os.path.exists(Config.DOC_UPLOAD_FOLDER + document_save_name):
                p.updateDocumentStatus(document_id, '3')
                print('not found')
            if src_lang not in ['zh', 'en', 'vi', 'my', 'kh', 'th', 'lo']:
                p.updateDocumentStatus(document_id, '3')
                continue

            p.updateDocumentStatus(document_id, '1')

            aThread = threading.Thread(target=fileTrans.fileTransThread,
                                       args=(
                                           document_id, user_id, document_save_name, src_lang, tgt_lang, document_name, document_size))
            fileThreads.append(aThread)

        for thread in fileThreads:
            thread.start()
