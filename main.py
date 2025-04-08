from tools import fetch_website_content, get_travel_info
import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()  # 自動讀取 .env 檔

open_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=open_api_key)

# 定義 function schema（讓模型知道可以用這個功能）
functions = [
    {
        "name": "fetch_website_content",
        "description": "Fetch the raw text content of a website using Selenium.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "要抓取的網址"
                }
            },
            "required": ["url"],
        },
    },
   {
    "name": "get_travel_info",
    "description": "查詢兩地之間的交通資訊。若搭乘捷運、公車，請將 mode 設為 'transit'。",
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "出發地，例如 '台北車站'"
            },
            "destination": {
                "type": "string",
                "description": "目的地，例如 '台北101'"
            },
            "mode": {
                "type": "string",
                "description": "交通方式，可選 'driving'（開車）、'transit'（大眾運輸：捷運、公車）、'walking'（步行）、'bicycling'（腳踏車）",
                "enum": ["driving", "transit", "walking", "bicycling"]
            }
        },
        "required": ["origin", "destination", "mode"],
    }
}

]

# 讓使用者輸入想問的內容
user_query = input("請輸入你的問題（例如：幫我抓取 https://example.com，或是 查從台北車站到台北101的捷運時間）：\n")

# 設計 prompt，強制引導模型使用 function
messages = [
    {
        "role": "user",
        "content": f"請使用適合的 function call 完成以下需求：{user_query}。"
    }
]

# 第一次請求，問 GPT 要不要用 function call
response = client.chat.completions.create(
    model="gpt-4o-mini",  
    messages=messages,
    functions=functions,
    function_call="auto"
)

# 取出 GPT 的回應
message = response.choices[0].message

# 看 GPT 有沒有決定呼叫 function
if message.function_call:
    function_name = message.function_call.name
    arguments = json.loads(message.function_call.arguments)

    # 根據呼叫的 function name，執行對應的 function
    if function_name == "fetch_website_content":
        function_response_content = fetch_website_content(arguments["url"])
    elif function_name == "get_travel_info":
        function_response_content = get_travel_info(
            arguments["origin"],
            arguments["destination"],
            arguments.get("mode", "driving")
        )
    else:
        function_response_content = "未知的 function call。"

    # 把 function 回傳的資料送回 GPT
    second_response = client.chat.completions.create(
        model="gpt-4o-mini",  # ✅ 這裡也用 gpt-4o-mini
        messages=[
            *messages,
            {
                "role": "assistant",
                "function_call": {
                    "name": function_name,
                    "arguments": json.dumps(arguments)
                }
            },
            {
                "role": "function",
                "name": function_name,
                "content": function_response_content
            }
        ]
    )

    # 印出 GPT 根據結果給你的最終回答
    print("\n🔵 GPT 回應：")
    print(second_response.choices[0].message.content)

else:
    # 如果 GPT 沒有使用 function
    print("\n⚠️ GPT 沒有使用 function，直接回應：")
    print(message.content)
