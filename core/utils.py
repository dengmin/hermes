import smtplib
from email.mime .text import MIMEText
import string
import hashlib
from random import choice
from flask import current_app

def create_token(length=16):
    chars = list(string.ascii_lowercase + string.digits)
    salt = ''.join([choice(chars) for i in range(length)])
    return salt

def create_password(raw):
    salt = create_token(8)
    passwd = '{0}{1}'.format(salt, raw)
    hsh = hashlib.sha1(passwd.encode('utf-8')).hexdigest()
    return "%s$%s" % (salt, hsh)

def switch_pub_port(pos):
    if pos not in ('master', 'slave'):
        raise Exception('must be master or slave')
    if pos == 'master':
        return '81'
    if pos == 'slave':
        return '82'

def send_html_email(subject, body, **kwargs):
    server = current_app.config.get('EMAIL_SERVER')
    username = current_app.config.get('EMAIL_USER')
    password = current_app.config.get('EMAL_PASSWORD')
    to_list = kwargs.get('to_list', [])
    try:
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = '自动化发布系统 <{0}>'.format(username)
        msg['Accept-Language'] ='zh-CN'
        msg['Accept-Charset'] = 'ISO -8859-1,utf-8'
        msg['To'] = ';'.join(to_list)
        smtp = smtplib.SMTP()
        smtp.connect(server)
        smtp.login(username, password)
        smtp.sendmail(username, [to_list, 'dengmin@baie.com.cn'], msg.as_string())
        smtp.quit()
    except Exception as e:
        current_app.logger.error('send email error')