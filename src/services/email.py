import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List


class EmailService:
    @staticmethod
    def send_confirmation_email(
        to_email: str, subject: str, name: str, order_id: str, tickets: List[Dict[str, int]]
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
                <p><strong>Tickets purchased:</strong></p>
                <ul style="list-style-position: inside; padding-left: 0; margin-left: 0; color: #555;">
                  {ticket_lines}
                </ul>
                <p>
                  This is your confirmation email. Please keep this for your records.<br/>
                  If you run into any trouble, speak to organisers or send an email with your order id to 
                  <a href="mailto:fawleydogshow@gmail.com">fawleydogshow@gmail.com</a>.
                </p>
                <p>Kind regards,<br/>Fawley Dog Show Team</p>
              </body>
            </html>
            """

        # Email setup
        from_email = "fawleydogshow@gmail.com"
        from_password = os.getenv("DOGSHOW_EMAIL_PASSWORD")
        if not from_password:
            raise ValueError(f"No email password")
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        # Connect and send
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            server.quit()
            print(f"Confirmation email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise e
