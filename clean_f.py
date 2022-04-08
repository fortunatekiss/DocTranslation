# coding=utf-8
import emoji
import re


class clean_f(object):

    def __init__(self):
        self.URL_REGEX = re.compile(
            r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
            re.IGNORECASE)
        self.T1 = re.compile('#\w+')
        self.T2 = re.compile('@\w+')
        self.T3 = re.compile(r"\:\S+\:")
        self.T4 = re.compile(r"\&\S+\;")
        self.T5 = re.compile(r"\(.*\)")
        self.T6 = re.compile(r"^\s*")
        self.T7 = re.compile(r"([=,-,*])\1+")
        self.T8 = re.compile(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s\d{1,2}:\d{1,2}\d{1,2}:\d{1,2}|\d{4}[-/]\d{1,2}[-/]\d{1,2}\s\d{1,2}:\d{1,2}|\d{4}[-/]\d{1,2}[-/]\d{1,2})")

        # 多余的字符串添加在这里
        self.RE = ['Read more here:', '复制', 'RT', 'Read More - - -', '■', 'T', '内容']

    def clean(self, t):
        print(t)
        if self.T8.fullmatch(t):
            return ''
        if self.URL_REGEX.fullmatch(t):
            return ''
        out = self.T1.sub(r'', t)
        out = self.T2.sub(r'', out)
        out = emoji.demojize(out)
        # 可以保留表情信息 作为str标签
        if not self.T8.sub(r'', out):
            out = self.T3.sub(r'', out)
        #out = self.T3.sub(r'', out)
        out = self.T4.sub(r'', out)
        out = self.T5.sub(r'', out)
        out = self.T6.sub(r'', out)
        out = self.T7.sub(r'', out)
        #out = self.URL_REGEX.sub(r'', out)
        #if re.search(self.URL_REGEX, out):
            #match_url = re.search(self.URL_REGEX, out)
            #pos = -1
            #while '//' in out:
                #if pos == out.index('//'):
                    #break
                #pos = out.index('//')
                #if out.index('//') < match_url.start() or out.index('//') > match_url.end():
                    #out = out[:out.index('//')] + out[out.index('//')+2:]
                    #match_url = re.search(self.URL_REGEX, out)

        for s in self.RE:
            out = out.replace(s, '')
        return out
