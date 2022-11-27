 
import smtplib, ssl
import config

context = ssl.create_default_context()

def sendEmail(
    messageBody,
    to = config.CLIENT_EMAIL,
    messageSender = config.SENDER):

    message = f"""\
    From: "Rasperry Pi 3" <{messageSender}>\n\
    To:  <{to}>\n
    
    \n
    {messageBody}

    """
    try:
        with smtplib.SMTP_SSL(config.SMTPSERVER, config.SMTPPORT, context=context) as smtp:
            smtp.login(messageSender, config.PASSWORD)
            print("logged in")
            smtp.sendmail(messageSender, to, message)
            print("Message sent")
            smtp.quit()
    except Exception as e:
        print(e)
        print("Error: unable to send email")

def main(): 
    try: 
        #smtp.ehlo()
        #smtp.ehlo()
        with smtplib.SMTP_SSL(config.SMTPSERVER, config.SMTPPORT, context=context) as smtp:
            print("loging in")
            smtp.login(sender, password)
            print("logged in")
            print("waiting for message")
            smtp.sendmail(sender, receivers, "test")
    except Exception as e: 
        print("error")
        print(e)
    finally:
        smtp.quit()

if __name__ == "__main__": 
    try:
        sendEmail("temp: 57 degrees too hot!")
    except KeyboardInterrupt:
        print("exiting program")
        