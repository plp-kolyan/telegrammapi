from rest_framework.response import Response
from rest_framework.decorators import api_view
from g4f.client import Client
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



@api_view(['POST'])
def ai_chat(request):

    if request.data.get('model') and request.data.get('messages'):
        client = Client()
        response = client.chat.completions.create(
            model=request.data['model'],
            messages=request.data['messages'],


        )
        return Response({"content": response.choices[0].message.content})
