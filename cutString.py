# coding=utf-8

class cutString(object):

    # 中文码区过滤
    def isZhUnicode(self, value):
        if 0x4E00 <= value <= 0x9FA5:
            return True
        elif 0x0800 <= value < 0x4E00:
            return True
        return False


    # def isJapanUnicode(value):
    #         if value >= 0x0800 and value < 0x4E00:
    #             return True
    #         return False

    # 英文码区过滤
    def isEnglishUnicode(self, value):
        if 0x61 <= value <= 0x7a:
            return True
        if 0x41 <= value <= 0x5a:
            return True
        return False


    # 缅甸语码区过滤
    def isBurmeseUnicode(self, value):
        if 0x1000 <= value <= 0x109f:
            return True
        return False


    # 泰语码区过滤
    def isThaiUnicode(self, value):
        if 0x0E00 <= value <= 0x0E16:
            return True
        if 0x0E17 <= value <= 0x0E2D:
            return True
        if 0x0E2E <= value <= 0x0E30:
            return True
        if 0x0E31 <= value <= 0x0E3A:
            return True
        if 0x0E3F <= value <= 0x0E46:
            return True
        if 0x0E47 <= value <= 0x0E4E:
            return True
        if 0x0E4F <= value <= 0x0E5B:
            return True
        return False


    # 柬埔寨语码区过滤
    def isKmUnicode(self, value):
        if 0x1780 <= value <= 0x17FF:
            return True
        return False


    # 老挝语码区过滤
    def isLaoUnicode(self, value):
        if 0x0E80 <= value <= 0x0EFF:
            return True
        return False


    # 越南语码区过滤
    def isVinamUnicode(self, value):
        if 0x00C0 <= value <= 0x00C3:
            return True
        if 0x00C8 <= value <= 0x00CA:
            return True
        if 0x00CC <= value <= 0x00CD:
            return True
        if 0x00D2 <= value <= 0x00D5:
            return True
        if 0x00D9 <= value <= 0x00DA:
            return True
        if value >= 0x00DD >= value:
            return True
        if 0x00E0 <= value <= 0x00E3:
            return True
        if 0x00E8 <= value <= 0x00EA:
            return True
        if 0x00EC <= value <= 0x00ED:
            return True
        if 0x00F2 <= value <= 0x00F5:
            return True
        if 0x00F9 <= value <= 0x00FA:
            return True
        if value >= 0x00FD >= value:
            return True
        if 0x0102 <= value <= 0x0103:
            return True
        if 0x0110 <= value <= 0x0111:
            return True
        if 0x0128 <= value <= 0x0129:
            return True
        if 0x0168 <= value <= 0x0169:
            return True
        if 0x01A0 <= value <= 0x01A1:
            return True
        if 0x01AF <= value <= 0x01B0:
            return True
        if 0x1EA0 <= value <= 0x1EF9:
            return True
        return False
    
    def isZangUnicode(self, value):
        if 0x0F00 <= value <= 0x0FDA:
            return True
        return False

    def isUyUnicode(self, value):
        if 0x0600 <= value <= 0x06FF:
            return True
        return False

    def getLang(self, code, last_code):
        if code in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return "num"
        if code in "）！/:\"%‘，}“”|+`-—;^。（：【@>~),#]{…】；<-￥》&=、《？*($!?[.'_·±":
            return "ts"
        code = ord(code)
        if self.isEnglishUnicode(code) or self.isVinamUnicode(code):
            return "en-vi"
        elif self.isBurmeseUnicode(code):
            return "my"
        elif self.isKmUnicode(code):
            return "km"
        elif self.isLaoUnicode(code):
            return "lo"
        elif self.isThaiUnicode(code):
            return "th"
        elif self.isZangUnicode(code):
            return "ti"
        elif self.isUyUnicode(code):
            return "uy"
        elif self.isZhUnicode(code):
            return "zh"
        elif code == 32:
            return last_code
        else:
            return "un"


    def get_cut_word(self, str):
        result = []
        langList = []
        temp_code = self.getLang(str[0], "blank")
        for index, j in enumerate(str):
            code = self.getLang(j, temp_code)
            temp_code = code
            result.append(j)
            langList.append(code)
        temp = langList[0]
        start = 0
        return_data = []
        for index, lang in enumerate(langList):
            if temp != lang and lang != "blank":
                data_tuple = self.get_tuple(result[start:index], temp)
                return_data.append(data_tuple)
                temp = lang
                start = index
            if index == len(langList) - 1:
                data_tuple = self.get_tuple(result[start:], temp)
                return_data.append(data_tuple)
                temp = lang
                start = index
        return return_data


    def get_tuple(self, data, lang):
        if lang == "zh":
            _lang = self.zh_or_ja(data)
            return "".join(data), _lang
        elif lang == "en-vi":
            for i in data:
                if self.isVinamUnicode(ord(i)):
                    return ("".join(data), "vi")
            return "".join(data), "en"
        else:
            return "".join(data), lang


    def zh_or_ja(self, data):
        zh = 0
        ja = 0
        for word in data:
            if 0x0800 <= ord(word) < 0x4E00:
                ja += 1
            else:
                zh += 1
        if zh > ja:
            return "zh"
        else:
            return "ja"
