from django.views.generic.base import TemplateView
import json
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings

class ChatterBotViewMixin(object):
    """
    Subclass this mixin for access to the 'chatterbot' attribute.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def validate(self, data):
        """
        Validate the data recieved from the client.
        * The data should contain a text attribute.
        """
        from django.core.exceptions import ValidationError

        if 'text' not in data:
            raise ValidationError('The attribute "text" is required.')

    def get_conversation(self, request):
        """
        Return the conversation for the session if one exists.
        Create a new conversation if one does not exist.
        """
        from chatterbot.ext.django_chatterbot.models import Conversation, Response

        class Obj(object):
            def __init__(self):
                self.id = None
                self.statements = []

        conversation = Obj()

        conversation.id = request.session.get('conversation_id', 0)
        existing_conversation = False
        try:
            Conversation.objects.get(id=conversation.id)
            existing_conversation = True

        except Conversation.DoesNotExist:
            conversation_id = self.chatterbot.storage.create_conversation()
            request.session['conversation_id'] = conversation_id
            conversation.id = conversation_id

        if existing_conversation:
            responses = Response.objects.filter(
                conversations__id=conversation.id
            )

            for response in responses:
                conversation.statements.append(response.statement.serialize())
                conversation.statements.append(response.response.serialize())

        return conversation

class ChatterBotView(TemplateView):
    print('ncc')
    template_name = "app.html"
session={}
class ChatterBotAppView(ChatterBotViewMixin, TemplateView):
    template_name = "app.html"
    """
    Provide an API endpoint to interact with ChatterBot.
    """
    def validate(self, data):
        """
        Validate the data recieved from the client.
        * The data should contain a text attribute.
        """
        from django.core.exceptions import ValidationError
        if 'text' not in data:
            raise ValidationError('The attribute "text" is required.')

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        """
        input_data = json.loads(request.read().decode('utf-8'))

        self.validate(input_data)

        conversation = self.get_conversation(request)

        try:
            u_session=session[conversation.id]
        except:
            u_session=session[conversation.id]='init'
        input_data['session']=[u_session,conversation.id]
        response = self.chatterbot.get_response(json.dumps(input_data))
        response_data = response.serialize()
        # session[conversation.id]=
        # print(response_data)
        session[conversation.id]=response_data['extra_data']['conversation_id'][0]
        if(session[conversation.id]=='done'):
            session[conversation.id]='init'
        print('\nresponse: '+str(response))
        # print('\nresponse data: '+str(response_data))
        print(session)
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        conversation = self.get_conversation(request)

        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': self.chatterbot.name,
            'conversation': conversation.statements
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def patch(self, request, *args, **kwargs):
        """
        The patch method is not allowed for this endpoint.
        """
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def delete(self, request, *args, **kwargs):
        """
        The delete method is not allowed for this endpoint.
        """
        data = {
            'detail': 'You should make a POST request to this endpoint.'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)
