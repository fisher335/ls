# coding=utf-8
"""
发送邮件,可发送html内容,普通文本内容,附件
"""
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_host = "mail.bjsasc.com"
mail_user = "netdisk@bjsasc.com"
mail_pass = "12345Aqwert"


# mailto_list = ["fengshaomin@bjsasc.com"]


# def send(to_list, subject, html_content=None, text_content=None, attachments=()):
def send(text_content=None, html_content=None, attachments=()):
    """
    send email,can send  html content,text content and attachments
    :param to_list:list of recievers
    :param subject: String of subject
    :param html_content:String of HTML content
    :param text_content:String of text content
    :param attachments:the list of attachment
    :return:boolean
    """

    # 设置固定值为往我自己的邮箱内发送
    # to_list = ["fengshaomin@bjsasc.com", 'wangyichong@bjsasc.com', 'zhangtianzhong@bjsasc.com']
    # to_list = ["fengshaomin@bjsasc.com", 'wangyichong@bjsasc.com']
    to_list = ["fengshaomin@bjsasc.com"]
    subject = '公司企业网盘错误通知'
    # ------------------------------------
    me = "netdisk<netdisk@bjsasc.com>"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject  # 设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    # html 内容
    if html_content:
        part2 = MIMEText(html_content, 'html', _charset='utf-8')
        msg.attach(part2)
    # 普通文本内容
    if text_content:
        part1 = MIMEText(text_content, 'plain', _charset='utf-8')
        msg.attach(part1)
    # 附件
    if attachments:
        for attach_file in attachments:
            part = MIMEApplication(open(attach_file, 'rb').read())
            filename = os.path.split(attach_file)[1]
            part.add_header('Content-ID', '<' + filename + '>')
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(part)
    # 备注:把邮件嵌入html正文,eg:图片.直接使用链接图片地址,大部分邮箱会屏蔽外链,由于不知道链接的安全性.
    # 要把图片嵌入到邮件正文中，需要先把图片作为附件添加进邮件，然后，在HTML中通过引用src="cid:XXX"  访问
    # eg:此处的cid 就是part.add_header('Content-ID', '<' + filename + '>') 中的filename
    # eg:此处邮件正文<img src='cid:%s'></img> %(filename)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception as e:
        print('%s' % e)
        return False


if __name__ == '__main__':
    file_name = "96_96.jpg"
    html_content = "<html><body>Hello,test send mail!<img src='cid:%s'  alt='%s'>%s</img></body></html>" % (
        file_name, file_name, file_name)
    text_content = "Hello,test send mail! text content"
    file1 = "C:/ls/1.py"
    file2 = "C:/ls/2.py"
    attach_files = (file1, file2)
    send( html_content=html_content, attachments=attach_files)
