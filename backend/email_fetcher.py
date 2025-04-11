import requests  # Make sure requests is installed
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from logger import log_service_request  # Use the shared logger

# Define the ML Model API URL (Flask app for ML predictions)
ML_MODEL_API_URL = "http://127.0.0.1:5000/predict"  # Update if deployed elsewhere

def clean_html(html_content):
    """Extract plain text from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def connect_and_fetch():
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("elaranoelle24@gmail.com", "lubv mffy shmx juru")

        # Select the inbox
        mail.select("inbox")

        # Search for unread emails
        status, messages = mail.search(None, '(UNSEEN)')
        email_ids = messages[0].split()

        print(f"\n📬 Found {len(email_ids)} unread email(s).\n")

        for e_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # Decode the subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    # Get sender
                    from_ = msg.get("From")

                    # Initialize email body
                    body = ""

                    # Extract the email content (plain text, or fallback to HTML)
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                break
                            elif content_type == "text/html" and not body:
                                html_content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                body = clean_html(html_content)
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        elif content_type == "text/html":
                            html_content = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                            body = clean_html(html_content)

                    # Send the email body to the ML model API for prediction
                    response = requests.post(
                        ML_MODEL_API_URL,
                        json={"message": body}  # Payload as JSON
                    )

                    if response.status_code == 200:
                        prediction = response.json()
                        print("Prediction:", prediction)
                        # Prepare a log message combining email details and ML prediction
                        log_message = (
                            f"Email Received - From: {from_}, Subject: {subject}, "
                            f"Body (truncated): {body.strip()[:100]}, Prediction: {prediction}"
                        )
                        log_service_request(log_message)
                    else:
                        err_message = f"Error with prediction for email from {from_}: {response.json()}"
                        print(err_message)
                        log_service_request(err_message)
        mail.logout()

    except Exception as e:
        error_message = f"Email fetcher error: {str(e)}"
        print("❌ Error:", error_message)
        log_service_request(error_message)

if __name__ == "__main__":
    connect_and_fetch()
