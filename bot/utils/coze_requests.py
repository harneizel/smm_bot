import requests
import json
import asyncio
import aiohttp

from bot.utils.config import COZE_URL as url, COZE_TOKEN as token, COZE_BOT_ID as coze_id

#coze взаимодействия
# все делается асинхронно чтобы не втыкали
async def coze_request(tg_id, query, history, conversation_id):
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': f"Bearer {token}",
                   'Content-Type': 'application/json',
                   'Accept': '*/*',
                   'Host':'api.coze.com',
                   'Connection':'keep-alive'}
        data = {'bot_id': str(coze_id),
                'conversation_id':str(conversation_id),
                'user': str(tg_id),
                'query': query,
                'stream': False,
                'chat_history': history}
        async with await session.post(url=url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                data = (json.loads(await response.text()))
                print(f"ОТВЕТ НЕЙРОНКИ БЕЗ ОБРАБОТКИ: {data}")
                if data['code']==0 and data['msg']=='success':
                    data = data["messages"]
                    for message in data:
                        if message['role']=='assistant' and message['type']=='answer':
                            print(f"ответ нейронки {message}")
                            return message
                    return "unknow_error" # если до этого дошло то сообщения нет
                elif len(data)==2 and data['msg']=="Your Token quota has been used up. Please visit https://www.coze.com/token to top up your tokens. If you have any questions, please contact coze support.":
                    print("ЗАКОНЧИЛИСЬ ТОКЕНЫ")
                    return "end_tokens" # токены закончились


