import graphene
from apps.emailing.queries import (QueryEmailConfiguration, FetchEmails,
)
from apps.emailing.mutations import (AssignEmailConfigurationToUser, SendingEmail, CreateEmailConfiguration, )

class Query(
    QueryEmailConfiguration,
    FetchEmails):
    pass

class Mutation(graphene.ObjectType):
    create_email_configuration = CreateEmailConfiguration.Field()
    assignEmailConfigurationToUser = AssignEmailConfigurationToUser.Field()
    sendingEmail = SendingEmail.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)#
