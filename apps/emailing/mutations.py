
import graphene
from .models import EmailConfigurationType, EmailConfiguration
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from graphene_file_upload.scalars import Upload
from .models import ExtendUser as User


class AssignEmailConfigurationToUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        email_conf_id = graphene.Int()
        app_password = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, user_id, email_conf_id=None, app_password=None ):
        user = User.objects.get(pk=user_id)
        if email_conf_id:
            conf = EmailConfiguration.objects.get(pk=email_conf_id)
            user.email_conf = conf
        if app_password:
            user.app_password = app_password
        user.save()
        return AssignEmailConfigurationToUser(success=True)

class SendingEmail(graphene.Mutation):
    class Arguments:
        user_id  = graphene.Int(required=True)
        email_to = graphene.String(required=True)
        subject  = graphene.String(required=True)
        content  = graphene.String(required=True)
        attachments = graphene.List(Upload)
    success = graphene.Boolean()

    def mutate(self, info, user_id, email_to, subject, content, attachments=None):
        conf = EmailConfiguration.objects.get(pk=user_id)
        user = User.objects.get(pk=user_id)
        sending(user.email, user.app_password, email_to, subject, content,
            conf.smtp_server, conf.smtp_port, attachments)
        return SendingEmail(success=True)

def sending(email_from, app_password, email_to,
         subject, content, smtp_server, smtp_port, attachments):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = email_from
        message["To"] = email_to
        part1 = MIMEText(content, "plain")
        message.attach(part1)

        if attachments:
            for attachment in attachments:
                if attachment:
                    message.attach(attachment.name, attachment.read(), attachment.content_type)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(email_from, app_password)
            server.sendmail(email_from, email_to, message.as_string())
    except Exception as e:
        print(e)

class CreateEmailConfiguration(graphene.Mutation):
    class Arguments:
        smtp_server = graphene.String()
        smtp_port = graphene.Int()
        incoming_server = graphene.String()
        incoming_port = graphene.Int()
        incoming_type = graphene.String()
        incoming_ssl = graphene.Boolean()
        incoming_tls = graphene.Boolean()
    email_configuration = graphene.Field(EmailConfigurationType)

    def mutate(self, info, smtp_server, smtp_port,
              incoming_server, incoming_port, incoming_type, 
              incoming_ssl, incoming_tls):
        email_config = EmailConfiguration(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            incoming_server=incoming_server,
            incoming_port=incoming_port,
            incoming_type=incoming_type,
            incoming_ssl=incoming_ssl,
            incoming_tls=incoming_tls,
        )
        email_config.save()
        return CreateEmailConfiguration(email_configuration=email_config)


