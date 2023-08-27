import graphene
from .models import EmailConfigurationType, EmailConfiguration
import imaplib
import email
from email.header import decode_header
from .models import ExtendUser as User

class QueryEmailConfiguration(graphene.ObjectType):
    email_configuration = graphene.List(EmailConfigurationType)

    def resolve_email_configuration(self, info):
        return EmailConfiguration.objects.all()


class FetchEmails(graphene.ObjectType):
    fetch_emails = graphene.List(graphene.String, mailbox=graphene.String(), nb_fetching=graphene.Int())

    def resolve_fetch_emails(self, info, mailbox, nb_fetching):
        user = User.objects.get(pk=info.context.user.id)
        
        if user.is_authenticated:
            try:
                emails = fetch_email(user.email, user.app_password,
                    user.email_conf.incoming_server, mailbox, nb_fetching)
                return [email_dict_to_string(e) for e in emails]
            except Exception as e:
                return [str(e)]  # Return error message
        else:
            return ["User is not authenticated"]

def fetch_email(email_user, email_pass, user_incoming_server, mailbox, nb_fetching):
    mail = imaplib.IMAP4_SSL(user_incoming_server)
    mail.login(email_user, email_pass)
    mail.select(mailbox)

    # Search for the last N emails in the mailbox
    status, email_ids = mail.search(None, "ALL")
    email_ids = email_ids[0].split()[-nb_fetching:]
    emails = []

    for email_id in email_ids:
        email_data = fetch_single_email(mail, email_id)
        emails.append(email_data)

    mail.logout()
    return emails

def fetch_single_email(mail, email_id):
    email_data = {}
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Get email details
    subject, encoding = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")
    sender = email_message.get("From")
    date = email_message.get("Date")

    email_data['subject'] = subject
    email_data['sender'] = sender
    email_data['date'] = date

    return email_data

def email_dict_to_string(email_data):
    return f"Subject: {email_data['subject']}\n" \
           f"From: {email_data['sender']}\n" \
           f"Date: {email_data['date']}\n" \
           f"{'=' * 50}"










"""
class FetchEmails(graphene.ObjectType):
    fetch_emails = graphene.List(graphene.String)

    def resolve_fetch_emails(self, info, mailbox, nb_fetching):
        user = User.objects.get(pk=info.context.user.id)
        emails=fetch_email(user.email, user.app_password ,mailbox, nb_fetching)
        return emails



def fetch_email(email_user, email_pass , mailbox, nb_fetching):
    mail = imaplib.IMAP4_SSL("imap.example.com")
    mail.login(email_user, email_pass)
    mail.select(mailbox)

    # Search for all emails in the mailbox
    status, email_ids = mail.search(None, "ALL")
    email_ids = email_ids[0].split()[-nb_fetching:]
    emails=[]
    # Fetch and process each email
    for email_id in email_ids:
        email={}
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        # Get email details
        subject, encoding = decode_header(email_message["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        sender = email_message.get("From")
        date = email_message.get("Date")
        
        print("Subject:", subject); email['subject']=subject
        print("From:", sender); email['sender']=sender
        print("Date:", date); email['date']=date
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Body:", body); email['body']=body
        else:
            body = email_message.get_payload(decode=True).decode()
            print("Body:", body); email['body']=body
        print("=" * 50)
        
        emails.append(email)
    mail.logout()
    return emails

"""