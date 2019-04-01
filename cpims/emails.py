"""Test email."""
# !/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings


def send_email(email, tmsg, hmsg, settings):
    """Method to send emails."""
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        fmail = "CPIMS Notification <%s>" % (sender)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "CPIMS"
        msg['From'] = fmail
        msg['To'] = email

        part1 = MIMEText(tmsg, 'plain')
        part2 = MIMEText(hmsg, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP(host, port, timeout=5)
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, email, msg.as_string())
        s.quit()
        print 'mail sent'
    except Exception, e:
        print 'Error sending email - %s' % (str(e))
    else:
        pass


if __name__ == '__main__':
    em = 'nmugaya@gmail.com'
    tm = 'Hi!\nThis is a test email.'
    hm = '<p>Hi!<br/>This is a test email'
    send_email(em, tm, hm, settings)

