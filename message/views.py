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


@api_view(['GET'])
def get_numbers(request):
    numbers = [1, 2, 3, 4, 5, 6, 7]
    start = request.query_params.get("start")
    end = request.query_params.get("end")
    if (start or end) is None:
        return Response({"numbers": numbers[0:2]})

    if start.isdigit() and end.isdigit():
        return Response({"numbers": numbers[int(start):int(end)]})

    else:
        return Response({"numbers": numbers[0:2]})







