import asyncio
import aiomysql
from flask import Flask, request, jsonify
import json


login = ""
password = ""

with open('mindsdb.json', 'r') as mindsdb:
    json_data = json.load(mindsdb)
    login = json_data["login"]
    passw = json_data["password"]
print(login, passw)

app = Flask(__name__)

async def get_response(prompt, context, model, personality):
    async with aiomysql.create_pool(
        host="cloud.mindsdb.com",
        port=3306,
        user=login,
        password=passw,
        db='mindsdb'
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT response FROM {model} WHERE personality='{personality}' AND context='{context}' AND text='{prompt}';"
                await cur.execute(query)
                result = await cur.fetchone()
                if result:
                    response = result[0]
                    context = f"\n{context}\nUser: {prompt}\n You: {response}"
                    return response, context
                else:
                    return "I'm sorry, I don't understand. Can you please rephrase?", context

@app.route('/chat35t', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data['prompt']
    context = data['context']
    personality = data['personality']
    model = "gpt35tclone"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
      response, context = loop.run_until_complete(get_response(prompt, context, model, personality))
      return jsonify({'response': response, 'context': context})
    except:
      print("Error!")
      return jsonify({'response': "Произошла ошибка! Попробуйте еще раз или очистите контекст!", 'context': context})

@app.route('/chat4', methods=['POST'])
def chat4():
    data = request.get_json()
    prompt = data['prompt']
    context = data['context']
    personality = data['personality']
    model = "gpt4clone"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
      response, context = loop.run_until_complete(get_response(prompt, context, model, personality))
      return jsonify({'response': response, 'context': context})
    except:
      print("Error!")
      return jsonify({'response': "Произошла ошибка! Попробуйте еще раз или очистите контекст!", 'context': context})
     

@app.route('/')
def home():
    return "Сервер запущен."

@app.after_request
def add_cors_headers(response):
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  return response
  
if __name__ == '__main__':
    input()
    app.run(host='0.0.0.0', port=1010)
