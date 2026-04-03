import smtplib
from email.mime.text import MIMEText

SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587

EMAIL_ADDRESS="rugved0149@gmail.com"
EMAIL_PASSWORD="ogvfmofhxbvvunas"


def send_otp_email(email,otp):

    msg=MIMEText(
        f"Your PHEMA verification OTP is: {otp}"
    )

    msg["Subject"]="PHEMA OTP Verification"
    msg["From"]=EMAIL_ADDRESS
    msg["To"]=email

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)