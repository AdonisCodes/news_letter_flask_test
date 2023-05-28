from email.message import EmailMessage
import ssl
import smtplib

host = "fernssimon1111@gmail.com"  # the host email
password = "bvjamqvrciujvskj" #the host password
rec = ["s.f.businessacc@gmail.com", "willferns2000@gmail.com"] # the receiver email

subject = "a email"

body = """
    New video uploaded to youtube chan
"""


context = ssl.create_default_context()
for i in range(len(rec)):

    em = EmailMessage()
    em["From"] = host
    em["Subject"] = subject
    em.set_content(body)
    em["To"] = rec[i]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as sept:
        sept.login(host, password)
        sept.sendmail(host, rec, em.as_string())
    print("email")