import sys


class _code(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:  # 判断是否已经被赋值，如果是则报错
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():  # 判断所赋值是否是全部大写，用来做第一次赋值的格式判断，也可以根据需要改成其他判断条件
            raise self.ConstCaseError('const name "%s" is not all supercase' % name)

        self.__dict__[name] = value


proviceCode = _code()
proviceCode.JIANGSU = '19'
proviceCode.HUBEI = '20'
proviceCode.ZHEJIANG = '21'
proviceCode.ANHUI = '22'
proviceCode.BEIJING = '22'

cityCode = _code()
cityCode.SUZHOU = proviceCode.JIANGSU + '0401'
cityCode.NANJING = proviceCode.JIANGSU + '0101'
cityCode.XUZHOU = proviceCode.JIANGSU + '0801'
cityCode.JIANGYIN = proviceCode.JIANGSU + '0202'
cityCode.WUXI = proviceCode.JIANGSU + '0201'
cityCode.BEIJING = '010100'



# 浙江
cityCode.JIAXING = proviceCode.ZHEJIANG + '0301'
cityCode.ANJI = proviceCode.ZHEJIANG + '0203'
cityCode.HANGZHOU = proviceCode.ZHEJIANG + '0101'

countyCode = _code()
countyCode.DANGSHAN = proviceCode.ANHUI + '0702'


