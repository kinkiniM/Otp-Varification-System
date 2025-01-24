import random 
import smtplib
import re
import time
import logging

# Configuration Constants
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
TIMEOUT =  3 * 60 # Timeout duration in seconds 
MAX_ATTEMPTS = 3  # Maximum attemps to enter the otp

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OtpVerification:
    """
    OtpVerification class handles the generation, sending, and Varification of OTP
    """
    @staticmethod
    def welcome():
        """ Display The System Info """
        print('---------------------------------')
        print('OTP Verification System in Python')
        print('---------------------------------')

    def __init__(self, sender_mail: str, sender_password: str):
        """
        Initialize the OTP Varification System with Sender Email And Password

        Args:
            sender_mail (str): Sender email address.
            sender_password (str): Sender email password.
        """
        self.sender_mail = sender_mail
        self.sender_password = sender_password

    def generate_otp(self):
        """
        Generate a 6-digit OTP.

        Returns:
            str: A random 6-digit OTP.
        """
        return str(random.randint(100001, 999999))

    def send_otp(self, receiver_email, otp):
        """
        Send OTP to the reciever's email.

        Args:
            receiver_email(str): Receiver's email address.
            otp (str): OTP to Send.
        """
        try:
            subject = 'OTP Verification System in Python'
            msg = f"Subject: {subject}\n\nYour OTP is: {otp}"
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as settings:
                settings.starttls()
                settings.login(self.sender_mail, self.sender_password)
                settings.sendmail(self.sender_mail, receiver_email, msg)
                settings.quit()
            logging.info("OTP sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Failed to send OTP: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def start_verification(self):
        """
        start the OTP varification Process with userinput for email and OTP.
        It will send an OTP to the provided email and allow the user to varify it.
        """
        
        while True:
            receiver_email = input('Enter Your Email: ')
            if self.is_valid_email(receiver_email):
                otp = self.generate_otp()
                self.send_otp(receiver_email, otp)

                self.varify_otp(otp)
                break
            else:
                logging.warning('Invalid email. Please enter a valid email address.')
    def is_valid_email(self, email:str) -> bool:
        """
        Validate email format using regex.

        args:
            email(str): Email address to validate.

        Returns:
            bool: True if the email is true, False otherwise
        """
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        return bool(valid)
    def varify_otp(self, otp:str):
        """
        Handle OTP varification by allowing the user to input and varify the OTP.

        Args:
            otp(str): OTP to varify.
        """
        attempts = MAX_ATTEMPTS
        start_time = time.time()

        logging.info("You Have 3 Mins to Enter the OTP")

        while attempts > 0:
            # Calculate remaining time
            elapsed_time = time.time() - start_time
            remaining_time = int(TIMEOUT - elapsed_time)

            if remaining_time <= 0:
                logging.error("Time expired. Verification failed.")
                break

            # Display the countdown timer
            mins, secs = divmod(remaining_time, 60)
            timer = f"Time remaining: {mins:02}:{secs:02}"
            print(timer, end="\r", flush=True)

            # User input for OTP
            verify_otp = input('\nEnter Your OTP to Verify: ')

            if verify_otp == otp:
                logging.info('Your OTP is verified successfully.')
                logging.info('----- End -----')
                break
            else:
                attempts -= 1
                if attempts > 0:
                    logging.warning(f'Wrong OTP. You have {attempts} attempt(s) left. Please try again.')
                else:
                    logging.error('All attempts exhausted. Verification failed.')

if __name__ == "__main__":
    OtpVerification.welcome()
    otp = OtpVerification("e2166752@gmail.com","myqi vcao estb jhuf")  # Replace with your email and password
    otp.start_verification()