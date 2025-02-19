# Built-In Libraries/Modules/Packages
import smtplib
import ssl

# Third Party Libraries/Modules/Packages
import pandas as pd
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def read_template(filename) -> str:
    """
    Reads a file completely and returns it as a string.
    """
    filehandle = open(filename, 'r', encoding='utf-8')
    content = filehandle.read()
    filehandle.close()
    return content


def file_object(file_name):
    try:
        with open(file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )

        return part
    except Exception as e:
        print(f'Oh no! We didnt found the attachment!n{e}')
        exit()


mail_subject = ""
sender_email = ""
sender_name = ""
password = ""
template_file = "template.html"
csv_file = "details.csv"

e = pd.read_csv(csv_file)
receiver_emails = e['EmailAddress'].values
receiver_names = e["Name"].values

for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
    print("Sending to " + receiver_name)
    msg = MIMEMultipart()
    msg['Subject'] = mail_subject
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = formataddr((receiver_name, receiver_email))
    mail_content = read_template(template_file)
    mail_content = mail_content.replace('{receiver_name}', receiver_name)
    msg.attach(MIMEText(mail_content, 'html'))

    # filename = "filename.pdf"
    # msg.attach(file_object(filename))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent!')
    except Exception as e:
        print(f'Oh no! Something bad happened!n{e}')
        break
    finally:
        print('Closing the server...')
        server.quit()
