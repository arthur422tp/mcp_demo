import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

with open('google_api.txt', 'r') as f:
    google_map_api_key = f.read().strip()

def get_travel_info(origin: str, destination: str, mode: str = "driving") -> str:
    """查詢 Google Map 上兩地之間的交通資訊，支援不同交通工具"""
    
    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,  # 可以是 driving, transit, walking, bicycling
        "key": google_map_api_key,
        "language": "zh-TW"  # 設成繁體中文
    }
    
    response = requests.get(endpoint, params=params)
    data = response.json()
    
    if data["status"] == "OK":
        route = data["routes"][0]["legs"][0]
        duration = route["duration"]["text"]
        distance = route["distance"]["text"]
        return f"從 {origin} 到 {destination} 的距離是 {distance}，預估 {mode} 模式下的時間是 {duration}。"
    else:
        return f"查詢失敗：{data['status']}"
    

def fetch_website_content(url: str) -> str:
    """使用 Selenium 抓取網頁主要文字內容"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 無頭
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    html = driver.page_source
    driver.quit()

    # 用 BeautifulSoup 清理掉 HTML 標籤，只留下文字
    soup = BeautifulSoup(html, "html.parser")

    # 只取 body 的文字
    text = soup.body.get_text(separator="\n", strip=True)
    return text
