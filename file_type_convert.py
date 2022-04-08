# coding=utf-8
import os


class file_type_convert(object):
    def doc_to_docx(self, upload_dir, document_save_name):
        path = upload_dir + document_save_name
        if os.path.splitext(document_save_name)[1] == ".doc":
            doc_path = upload_dir + document_save_name
            convert_command = "libreoffice --headless --convert-to docx --outdir " + upload_dir + " " + doc_path
            os.system(convert_command)
            path = path + 'x'
            document_save_name = document_save_name + 'x'
        return path, document_save_name

    def xls_to_xlsx(self, upload_dir, document_save_name):
        path = upload_dir + document_save_name
        if os.path.splitext(document_save_name)[1] == ".xls":
            doc_path = upload_dir + document_save_name
            convert_command = "libreoffice --headless --convert-to xlsx --outdir " + upload_dir + " " + doc_path
            os.system(convert_command)
            path = path + 'x'
            document_save_name = document_save_name + 'x'
        return path, document_save_name
