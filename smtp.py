import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import os

smtp_host = ''
smtp_port = 465
smtp_is_ssl = True
smtp_user = ''
smtp_password = ''
smtp_from = ''
smtp_to = ['']
debuglevel = 0
folder_path = ''


def send(server, subject, text, send_from, send_to=[], files=[]):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for file_name in files:
        with open(file_name, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file_name))
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file_name)
            msg.attach(part)
    server.sendmail(send_from, send_to, msg.as_string())


def get_all_files(folder_path):
    files = os.listdir(folder_path)
    fs = []
    for file_name in files:
        name = os.path.join(folder_path, file_name)
        if os.path.isfile(name):
            fs.append(name)
    return fs


def connect(host, port, is_ssl=False, user=None, password=None):
    if is_ssl:
        s = smtplib.SMTP_SSL(host, port)
    else:
        s = smtplib.SMTP(host, port)
    s.debuglevel = debuglevel

    if user is not None and password is not None:
        s.login(user, password)
    return s


def main():
    s = connect(smtp_host, smtp_port, smtp_is_ssl, smtp_user, smtp_password)
    fs = get_all_files(folder_path)
    i = 1
    for filename in fs:
        send(s, 'Message {}'.format(i), 'File {}'.format(i), smtp_from, smtp_to, [filename])
        i += 1
    s.quit()
    s.close()


if __name__ == '__main__':
    main()
