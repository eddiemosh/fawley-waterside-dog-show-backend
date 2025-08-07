import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List


class EmailService:
    @staticmethod
    def send_confirmation_email(to_email: str, subject: str, name: str, order_id: str, tickets: List[Dict[str, int]]) -> bool:
        """
        Send an email to customers
        :return: True if email is successful
        """
        # Format ticket details
        if tickets:
            ticket_lines = "\n".join(
                f"- {' '.join(ticket_name.split('_')).title()}: {quantity}"
                for ticket_dict in tickets
                for ticket_name, quantity in ticket_dict.items()
            )
        else:
            ticket_lines = "No tickets purchased."

        # Email content
        body = f"""
        Hello {name},
    
        Thank you for your order!
    
        Order ID: {order_id}
        
        Tickets purchased:
        {ticket_lines}
    
        This is your confirmation email. Please keep this for your records. 
        If you run into any trouble, speak to organisers or send an email with your order id to hardyedward18@gmail.com.
    
        Kind regards,  
        Fawley Dog Show Team
        """

        # Email setup
        from_email = "hardyedward18@gmail.com"
        from_password = os.getenv("DOGSHOW_EMAIL_PASSWORD")  # Use an App Password for Gmail
        if not from_password:
            raise ValueError(f"No email password")
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

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
