# 這是一個function call的範例

##運行步驟

1. pip install -r requirements.txt（安裝所需套件）

2.（如果你有使用API）設定API，我在這份專案裡面是使用dotenv來設定，步驟如下
    (1).手動新增一份text file 並命名為.env
    (2).將你所有需要的API寫入 e.g. OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
    (3).儲存

3.你可以自行在tools.py裡面添加你想要的工具e.g.一個以arxiv搜尋論文的程式碼
    （若有增加工具，請務必修正main.py中的function schema以及後續的判斷式，讓模型知道你有什麼工具可以用）

