from cutString import cutString


class merge():
    def __init__(self):
        self.cutString = cutString()

    def ThLaoMyKmVi(self, str):
        code = ord(str)
        if self.cutString.isVinamUnicode(code):
            return "en-vi"
        elif self.cutString.isBurmeseUnicode(code):
            return "my"
        elif self.cutString.isKmUnicode(code):
            return "km"
        elif self.cutString.isLaoUnicode(code):
            return "lo"
        elif self.cutString.isThaiUnicode(code):
            return "th"

    def merge(self, result):
        out_list = []
        others = ["num", "ts", "un"]
        ThLaoMyKmVi = ["th", "lo", "my", "km", "vi"]
        while len(result) > 2:
            first_lang = result[0][1]
            second_lang = result[1][1]
            three_lang = result[2][1]
            if second_lang == first_lang and first_lang not in others:
                if three_lang == first_lang or three_lang in others:
                    tmp = (result[0][0] + result[1][0] + result[2][0], first_lang)
                    result.pop(0), result.pop(0), result.pop(0)
                    result.insert(0, tmp)
                elif three_lang not in others and three_lang != first_lang:
                    tmp = (result[0][0] + result[1][0], first_lang)
                    result.pop(0), result.pop(0)
                    result.insert(0, tmp)
            elif second_lang != first_lang and second_lang not in others and first_lang not in others:
                if three_lang == first_lang and three_lang not in others:
                    if len(result[1][0]) > 5:
                        out_list.append(result[0])
                        out_list.append(result[1])
                        result.pop(0), result.pop(0)
                    else:
                        set_lang = first_lang
                        if len(result[0][0]) + len(result[2][0]) < len(result[1][0]):
                            set_lang = second_lang
                        tmp = (result[0][0] + result[1][0] + result[2][0], set_lang)
                        result.pop(0), result.pop(0), result.pop(0)
                        result.insert(0, tmp)
                elif three_lang == second_lang and three_lang not in others:
                    tmp = (result[1][0] + result[2][0], second_lang)
                    result.pop(1), result.pop(1)
                    result.insert(1, tmp)
                elif first_lang != second_lang and second_lang != three_lang and three_lang != first_lang:
                    out_list.append(result[0])
                    result.pop(0)
                elif three_lang in others:
                    if len(result[1][0]) > 5:
                        out_list.append(result[0])
                        tmp = (result[1][0] + result[2][0], second_lang)
                        result.pop(0), result.pop(0), result.pop(0)
                        result.insert(0, tmp)
                    else:
                        tmp = (result[1][0] + result[2][0], second_lang)
                        result.pop(1), result.pop(1)
                        result.insert(1, tmp)
            elif second_lang in others and first_lang not in others:
                if three_lang == first_lang:
                    tmp = (result[0][0] + result[1][0] + result[2][0], first_lang)
                    result.pop(0), result.pop(0), result.pop(0)
                    result.insert(0, tmp)
                elif three_lang != first_lang and three_lang not in others:
                    if len(result[2][0]) > 5:
                        out_list.append((result[0][0] + result[1][0], first_lang))
                        result.pop(0), result.pop(0)
                    else:
                        tmp = (result[0][0] + result[1][0], first_lang)
                        result.pop(0), result.pop(0)
                        result.insert(0, tmp)
                elif three_lang in others:
                    tmp = (result[0][0] + result[1][0] + result[2][0], first_lang)
                    result.pop(0), result.pop(0), result.pop(0)
                    result.insert(0, tmp)
            elif first_lang in others and second_lang not in others:
                if three_lang in others:
                    tmp = (result[0][0] + result[1][0] + result[2][0], second_lang)
                    result.pop(0), result.pop(0), result.pop(0)
                    result.insert(0, tmp)
                elif three_lang not in others and three_lang == second_lang:
                    tmp = (result[0][0] + result[1][0] + result[2][0], second_lang)
                    result.pop(0), result.pop(0), result.pop(0)
                    result.insert(0, tmp)
                elif three_lang not in others and three_lang != second_lang:
                    tmp = (result[0][0] + result[1][0], second_lang)
                    result.pop(0), result.pop(0)
                    result.insert(0, tmp)
            elif first_lang in others and second_lang == others:
                tmp = (result[0][0] + result[1][0] + result[2][0], second_lang)
                result.pop(0), result.pop(0), result.pop(0)
                result.insert(0, tmp)
            elif first_lang in others and second_lang in others:
                tmp = (result[0][0] + result[1][0] + result[2][0], second_lang)
                result.pop(0), result.pop(0), result.pop(0)
                result.insert(0, tmp)

        if len(result) == 2:
            first_lang = result[0][1]
            second_lang = result[1][1]
            if first_lang == second_lang and first_lang not in others:
                out_list.append((result[0][0] + result[1][0], first_lang))
            elif first_lang not in others and first_lang != second_lang and second_lang not in others:
                out_list.append(result[0])
                out_list.append(result[1])
            elif first_lang not in others and second_lang in others:
                out_list.append((result[0][0] + result[1][0], first_lang))
            elif first_lang == second_lang and first_lang in others:
                pass
            elif first_lang in others and second_lang not in others:
                out_list.append(result[1])
        elif len(result) == 1:
            first_lang = result[0][1]
            if first_lang not in others:
                out_list.append(result[0])
            else:
                pass
        return out_list
