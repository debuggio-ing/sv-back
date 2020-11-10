import smtplib
import ssl
from email.message import EmailMessage


# Send email to verify email.
def send_email(user_email: str, code: int):
    port = 465  # For SSL
    sender_email = "debuggioinc@gmail.com"
    password = "debuggio123"

    receiver_email = user_email

    SUBJECT = "Verificar email"
    TEXT = "Ingrese el siguiente codigo para verificar su email: " + str(code)

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=message)
