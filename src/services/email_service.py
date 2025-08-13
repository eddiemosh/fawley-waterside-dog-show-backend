import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

from src.constants.email import FROM_EMAIL
from src.utils.stripe_utils import DOGSHOW_DOMAIN


class EmailService:
    def __init__(self):
        pass

    def __send_email(self, to_email: str, subject: str, msg: MIMEMultipart) -> None:
        from_password = os.getenv("DOGSHOW_EMAIL_PASSWORD")
        if not from_password:
            raise ValueError("No email password")
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(FROM_EMAIL, from_password)
        server.send_message(msg)
        server.quit()

    def send_order_confirmation_email(
        self,
        to_email: str,
        subject: str,
        name: str,
        order_id: str,
        tickets: List[Dict[str, int]],
        date_of_purchase: str,
        amount: str,
    ) -> bool:
        """
        Send an email to customers
        :return: True if email is successful
        """
        if tickets:
            ticket_lines = "".join(
                f"<li>{' '.join(ticket_name.split('_')).title()} x {quantity}</li>"
                for ticket_dict in tickets
                for ticket_name, quantity in ticket_dict.items()
                if quantity
            )
        else:
            ticket_lines = "<li>No tickets purchased.</li>"

        # Email content as HTML with inline styles
        body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <p>Hello {name},</p>
                <p>Thank you for your order!</p>
                <p><strong>Order ID:</strong> {order_id}</p>
                <p><strong>Date of Purchase:</strong> {date_of_purchase} (GMT)</p>
                <p><strong>Amount:</strong> £{amount}</p>
                <p><strong>Tickets purchased:</strong></p>
                <ul style="list-style-position: inside; padding-left: 0; margin-left: 0; color: #555;">
                  {ticket_lines}
                </ul>
                <p>
                  This is your confirmation email. Please keep this for your records.<br/>
                  If you run into any trouble, speak to organisers or send an email with your order id to
                  <a href="mailto:fawleydogshow@gmail.com"> fawleydogshow@gmail.com</a>.
                </p>
                <p>Kind regards,<br/>Fawley Dog Show Team</p>
                <img src="cid:dog_thank_you" alt="Thank you dog"
                 style="display: block; margin: 10px auto 0 auto; max-width: 300px; width: 100%; height: auto;"/>
              </body>
            </html>
            """

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "html"))

        # Attach the dog thank you image
        image_path = os.path.join(os.path.dirname(__file__), "../images/dog_thank_you.png")
        with open(image_path, "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header("Content-ID", "<dog_thank_you>")
            img.add_header("Content-Disposition", "inline", filename="Thank You!.png")
            msg.attach(img)

        # Connect and send
        try:
            self.__send_email(to_email, subject, msg)
            print(f"Confirmation email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise e

    def send_donation_confirmation_email(
        self,
        to_email: str,
        name: str,
        donation_id: str,
        date_of_donation: str,
        amount: str,
    ) -> bool:
        """
        Send a donation confirmation email to the customer, styled like the order confirmation email.
        :return: True if email is successful
        """
        subject = "Thank You For Your Donation!"
        body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <p>Hello {name},</p>
                <p><strong>Thank you so much for your generous donation!</strong></p>
                <p>Your support means a great deal to us and will directly help fund vital cancer research and support services.</p>
                <p><strong>Donation ID:</strong> {donation_id}</p>
                <p><strong>Date of Donation:</strong> {date_of_donation} (GMT)</p>
                <p><strong>Amount:</strong> £{amount}</p>
                <p>
                  Every contribution helps Southampton Cancer Research get closer to breakthroughs in cancer treatment and provides hope to those affected.<br/>
                  We are deeply grateful for your kindness and commitment to making a difference.
                </p>
                <p>
                  This is your donation confirmation email. Please keep this for your records.<br/>
                  If you have any questions, contact us at
                  <a href="mailto:fawleydogshow@gmail.com"> fawleydogshow@gmail.com</a>.
                </p>
                <p>With heartfelt thanks,<br/>Fawley Dog Show Team</p>
                <img src="cid:dog_thank_you" alt="Thank you dog"
                 style="display: block; margin: 10px auto 0 auto; max-width: 300px; width: 100%; height: auto;"/>
              </body>
            </html>
            """

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "html"))

        # Attach the dog thank you image
        image_path = os.path.join(os.path.dirname(__file__), "../images/dog_thank_you.png")
        with open(image_path, "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header("Content-ID", "<dog_thank_you>")
            img.add_header("Content-Disposition", "inline", filename="Thank You!.png")
            msg.attach(img)

        # Connect and send
        try:
            self.__send_email(to_email=to_email, subject=subject, msg=msg)
            print(f"Donation confirmation email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send donation email: {e}")
            raise e

    def _format_ticket_list(self, tickets: list[str]) -> str:
        if not tickets:
            raise Exception("No tickets provided for formatting")
        if len(tickets) == 1:
            return f"{tickets[0]} ticket"
        if len(tickets) == 2:
            return f"{tickets[0]} and {tickets[1]} tickets"
        return f"{', '.join(tickets[:-1])} and {tickets[-1]} tickets"

    def send_feedback_email(self, name: str, to_email: str, tickets: list[str]):
        subject = "Thank You for Attending the Fawley Dog Show! Any feedback?"
        feedback_url = f"{DOGSHOW_DOMAIN}/feedback"
        body = f"""
            <html>
              <body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">
                <p>Hey {name.title()}!</p>
                <p style=\"background: #f63131; color: #fff; padding: 12px 18px; border-radius: 6px; 
                font-weight: bold; text-align: center;\">
                <strong>I'd really appreciate some feedback if you have 30 seconds?</strong></p>
                <p><strong>Thank you for coming to the Fawley Dog Show!</strong></p>
                <p>I see you bought the {self._format_ticket_list(tickets)}. <strong>I really appreciate your 
                support for cancer research!</strong></p>
                <p>We're proud to share that, together, we raised roughly <strong>£1000</strong> for cancer research.
                 Your support helps fund vital research and brings hope to those affected by cancer.</p>
                <p>Our event is organised and run entirely by volunteers, and we're still growing. 
                We are also funded by generous sponsors who make this event possible.</p>
                <p>Your feedback is invaluable to us as we strive to make each year even better.
                 Please take a moment to let us know about your experience:</p>
                <div style=\"margin: 32px 0; text-align: center;\">
                  <a href=\"{feedback_url}\" style=\"background: #f63131; color: white; padding: 12px 24px; 
                  text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;\">
                  Give Feedback</a>
                </div>
                <p><strong>Check out the Composite Doors from our sponsor, Salarian Homes!</strong><br/>
                For every door purchased, <strong>£25 goes directly to cancer research</strong>.</p>
                <p>Thank you again for your generosity and for being part of our community.<br/>With gratitude,<br/>
                The Fawley Dog Show Team</p>
                <img src=\"cid:salarian_homes\" alt=\"Salarian Homes\"
                 style=\"display: block; margin: 10px auto 0 auto; max-width: 300px; width: 100%; height: auto;\"/>
                <p style=\"text-align: center; margin-top: 24px;\">
                  <a href=\"https://www.facebook.com/profile.php?id=61554694584616\" style=\"color: #4267B2; 
                  font-weight: bold; text-decoration: none; font-size: 1.1em;\">Click to find out what we're 
                  doing on our Facebook page!</a>
                </p>
              </body>
            </html>
            """
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "html"))
        image_path = os.path.join(os.path.dirname(__file__), "../images/salarian_homes.png")
        with open(image_path, "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header("Content-ID", "<salarian_homes>")
            img.add_header("Content-Disposition", "inline", filename="Salarian Homes.png")
            msg.attach(img)
        try:
            self.__send_email(to_email=to_email, subject=subject, msg=msg)
            print(f"Feedback email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send feedback email: {e}")
            raise e
