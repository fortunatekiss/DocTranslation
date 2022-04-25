# coding=utf-8

#import MySQLdb
import pymysql
from config import Config


class PdbcConnector(object):
    def __init__(self):
        self.db_host = Config.MYSQL['HOST']
        self.db_user = Config.MYSQL['USER']
        self.db_pwd = Config.MYSQL['PASSWORD']
        self.db_name = Config.MYSQL['DATABASE']
        self.db_port = Config.MYSQL['PORT']
        #pymysql.install_as_MySQLdb() 

    def dbConnector(self):
        try:
            db = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_pwd, database=self.db_name, port=self.db_port, charset='utf8')
            print("DATABASE CONNECTED")
            #db = MySQLdb.connect(self.db_host, self.db_user, self.db_pwd, self.db_name, self.db_port)
            #db.set_character_set('utf8')
            return db
        except Exception as e:
            print(e)
            exit('Database connection error.')

    def dbQuery(self, sql):
        try:
            self.db = self.dbConnector()
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            self.db.close()
            return results
        except:
            return 0

    def dbUpdate(self, sql):
        try:
            self.db = self.dbConnector()
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            cursor.close()
            self.db.close()
            return 1
        except:
            self.db.rollback()
            #cursor.close()
            self.db.close()
            return 0
            
    # 获取未翻译文档
    def getUnTranslatedDocument(self, max_file):
        sql = "SELECT document_id, user_id, document_save_name, src_lang, tgt_lang, document_name, document_size FROM user_document_tab WHERE document_status='0' LIMIT %d" % max_file
        return self.dbQuery(sql)

    # 更新文档状态
    def updateDocumentStatus(self, docid, status):
        sql = "UPDATE user_document_tab SET document_status='%s' WHERE document_id='%s'" % (status, docid)
        return self.dbUpdate(sql)

    # 导入译文
    def importTranslation(self, sentenceid, docid, userid, srclang, tgtlang, srctext, tgttext):
        sql = "INSERT INTO doc_translation_tab(translation_id, user_id, doc_id, src_text, tgt_text, src_lang, tgt_lang) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
            sentenceid, userid, docid, srctext, tgttext, srclang, tgtlang)
        return self.dbUpdate(sql)

    # 更新document_save_name为docx or xlsx
    def updateDocumentSaveName(self, docid, document_save_name):
        sql = "UPDATE user_document_tab SET document_save_name = '%s' WHERE document_id = '%s'" % (
            document_save_name, docid)
        return self.dbUpdate(sql)
    
    def get_user_memory_dict_by_username_langpair(self, username, src, tgt):
        sql = "SELECT dict_id, dict FROM user_dict_tab WHERE user_id = '%s' AND src_lang = '%s' AND tgt_lang = '%s' AND del = '0'" % (username, src, tgt)
        return self.dbQuery(sql)
    
    def get_all_user_memory_dict_by_langpair(self, src, tgt):
        sql = "SELECT dict_id, dict FROM user_dict_tab WHERE src_lang = '%s' AND tgt_lang = '%s' AND del = '0'" % (src, tgt)
        return self.dbQuery(sql)
    
    def record_src_text(self, username, src, tgt, src_text, char_length, trans_source, doc_save_name, document_id):
        src_text = src_text.replace("\"", "'")
        sql = "INSERT INTO ol_translation_tab (user_id, src_lang, tgt_lang, src_text, char_length, trans_source, doc_save_name, doc_id) VALUES ('%s', '%s', '%s', \"%s\", %s, '%s', '%s', '%s') ON DUPLICATE KEY UPDATE src_text=CONCAT(IFNULL(src_text,''), \" %s\"), char_length=char_length+%s" % (username, src, tgt, src_text, char_length, trans_source, doc_save_name, document_id, src_text, char_length)
        # sql_update = "UPDATE ol_translation_tab SET tgt_text=\"%s\" WHERE user_id='%s' AND trans_source='%s' AND doc_save_name='%s' AND doc_id='%s'" % (tgt_text, username, trans_source, doc_save_name, document_id)
        # sql = "INSERT INTO ol_translation_tab (user_id, src_lang, tgt_lang, src_text, char_length, trans_source, doc_save_name, doc_id) VALUES ('%s', '%s', '%s', \"%s\", %s, '%s', '%s', '%s')" % (username, src, tgt, src_text, char_length, trans_source, doc_save_name, document_id)
        print(sql)
        return self.dbUpdate(sql)
    
    def record_tgt_text(self, username, tgt_text, trans_source, doc_save_name, document_id):
        tgt_text = tgt_text.replace("\"", "'")
        sql = "UPDATE ol_translation_tab SET tgt_text=CONCAT(IFNULL(tgt_text,''), \"%s\") WHERE user_id='%s' AND trans_source='%s' AND doc_save_name='%s' AND doc_id='%s'" % (tgt_text, username, trans_source, doc_save_name, document_id)
        print(sql)
        return self.dbUpdate(sql)

    # # 获取未翻译文档
    # def getUnTranslatedDocument(self, max_file):
    #     self.db = self.dbConnnector()
    #     cursor = self.db.cursor()
    #     sql = "SELECT document_id, user_id, document_save_name, src_lang, tgt_lang, document_name FROM user_document_tab WHERE document_status='0' LIMIT %d" % max_file
    #
    #     try:
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         return result
    #     except:
    #         return 0
    #
    # # 更新文档状态
    # def updateDocumentStatus(self, docid, status):
    #     self.db = self.dbConnnector()
    #     cursor = self.db.cursor()
    #     sql = "UPDATE user_document_tab SET document_status='%s' WHERE document_id='%s'" % (status, docid)
    #
    #     try:
    #         cursor.execute(sql)
    #         self.db.commit()
    #         return 1
    #     except:
    #         self.db.rollback()
    #         return 0
    #
    # # 导入译文
    # def importTranslation(self, sentenceid, docid, userid, srclang, tgtlang, srctext, tgttext):
    #     self.db = self.dbConnnector()
    #     cursor = self.db.cursor()
    #
    #     sql = "INSERT INTO doc_translation_tab(translation_id, user_id, doc_id, src_text, tgt_text, src_lang, tgt_lang) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
    #         sentenceid, userid, docid, srctext, tgttext, srclang, tgtlang)
    #
    #     try:
    #         cursor.execute(sql)
    #         self.db.commit()
    #         return 1
    #     except:
    #         return 0
    #
    # # 更新document_save_name为docx or xlsx
    # def updateDocumentSaveName(self, docid, document_save_name):
    #     self.db = self.dbConnnector()
    #     cursor = self.db.cursor()
    #
    #     sql = "UPDATE user_document_tab SET document_save_name = '%s' WHERE document_id = '%s'" % (
    #         document_save_name, docid)
    #
    #     try:
    #         cursor.execute(sql)
    #         self.db.commit()
    #         return 1
    #     except:
    #         self.db.rollback()
    #         return 0

# pdbc = PdbcConnector()
# print(pdbc.getUnTranslatedDocument())
# pdbc.updateDocumentStatus('2020031902345','2')
# pdbc.importTranslation('2020042612345678', '1234567', 'admin', 'en', 'zh', 'hello', '你好')
