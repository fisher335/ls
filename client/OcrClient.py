# coding:utf-8
import os

from aip import AipOcr


class OcrClient:
    """ 你的 APPID AK SK """
    APP_ID = '16667601'
    API_KEY = 'T3xjr0oIM7Pv6cOBU4N6cn90'
    SECRET_KEY = 'IK4bMvckG5yMYEAswKRYeGGFlfQddUlV'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    """ 读取图片 """

    @staticmethod
    def simple_ocr(file_byte):
        client = OcrClient.client
        result = client.basicGeneral(file_byte)
        words = ""
        if result.get('log_id', '') != "":
            for i in result.get('words_result'):
                words += i['words'] + '''<br>'''
        else:
            words = str(result)
        return words

    @staticmethod
    def fapiao_file_path(file_path, type='normal'):
        options = {}
        options['type'] = type
        result = OcrClient.client.vatInvoice(open(file_path, 'rb').read(), options=options)
        print(result)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            ticket = result['words_result']
            print(ticket)
            print('合计金额', ticket['TotalAmount'])
            print('合计税额', ticket['TotalTax'])
            print('平均税率', format(float(ticket['TotalTax']) / float(ticket['TotalAmount']) * 100, '0.2f') + '%')
            print('价税合计', ticket['AmountInWords'])
            print('价税合计', ticket['AmountInFiguers'])
            print()
            print('销售方名称', ticket['SellerName'])
            print('销售方纳税人识别号', ticket['SellerRegisterNum'])
            print('销售方地址及电话', ticket['SellerAddress'])
            print('销售方开户行及账号', ticket['SellerBank'])
            print()
            print('购方名称', ticket['PurchaserName'])
            print('购方纳税人识别号', ticket['PurchaserRegisterNum'])
            print('购方地址及电话', ticket['PurchaserAddress'])
            print('购方开户行及账号', ticket['PurchaserBank'])
            print()
            print('收款人', ticket['Payee'])
            print('复核', ticket['Checker'])
            print('开票人', ticket['NoteDrawer'])
            print('开票日期', ticket['InvoiceDate'])
            return ticket
        os.remove(file_path)

    def fapiao_file_byte(file, type='normal'):
        options = {}
        options['type'] = type
        result = OcrClient.client.vatInvoice(file, options=options)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            ticket = result['words_result']
            print(ticket)
            print('合计金额', ticket['TotalAmount'])
            print('合计税额', ticket['TotalTax'])
            print('平均税率', format(float(ticket['TotalTax']) / float(ticket['TotalAmount']) * 100, '0.2f') + '%')
            print('价税合计', ticket['AmountInWords'])
            print('价税合计', ticket['AmountInFiguers'])
            print()
            print('销售方名称', ticket['SellerName'])
            print('销售方纳税人识别号', ticket['SellerRegisterNum'])
            print('销售方地址及电话', ticket['SellerAddress'])
            print('销售方开户行及账号', ticket['SellerBank'])
            print()
            print('购方名称', ticket['PurchaserName'])
            print('购方纳税人识别号', ticket['PurchaserRegisterNum'])
            print('购方地址及电话', ticket['PurchaserAddress'])
            print('购方开户行及账号', ticket['PurchaserBank'])
            print()
            print('收款人', ticket['Payee'])
            print('复核', ticket['Checker'])
            print('开票人', ticket['NoteDrawer'])
            print('开票日期', ticket['InvoiceDate'])
            return ticket

    @staticmethod
    def rec_idcard(file, side="front"):
        """
        识别身份证的信息
        :param file:
        :return:
        """
        result = OcrClient.client.idcard(file, side)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            idcard = result['words_result']
            d = {}
            for i in idcard.keys():
                d[i] = idcard[i]["words"]
            return d

    @staticmethod
    def rec_bankcard(file):
        """
        识别身份证的信息
        :param file:
        :return:
        """
        result = OcrClient.client.bankcard(file)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            bankcard = result['result']
            return bankcard

    @staticmethod
    def rec_fapiao(file):
        """
        识别通用机打发票
        :param file:
        :return:
        """
        """ 如果有可选参数 """
        result=OcrClient.client.invoice(file)
        print(result)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            fapiao = result['words_result']
            return fapiao

    @staticmethod
    def rec_taxi_receipt(file):
        """
        识别出租车票
        :param file:
        :return:
        """
        """ 如果有可选参数 """
        options = {}
        options['type'] = 'roll'
        result = OcrClient.client.taxiReceipt(file, options)
        print(result)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            _re = result['words_result']
            return _re

if __name__ == '__main__':
    OcrClient.hello();
