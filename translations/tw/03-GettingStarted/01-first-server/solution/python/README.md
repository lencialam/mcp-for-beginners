<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d26f746e21775c30b4d7ed97962b24df",
  "translation_date": "2025-08-11T09:50:20+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "tw"
}
-->
# 執行此範例

建議安裝 `uv`，但不是必須，請參閱[說明](https://docs.astral.sh/uv/#highlights)

## -0- 建立虛擬環境

```bash
python -m venv venv
```

## -1- 啟用虛擬環境

```bash
venv\Scripts\activate
```

## -2- 安裝依賴項

```bash
pip install "mcp[cli]"
```

## -3- 執行範例

```bash
mcp run server.py
```

## -4- 測試範例

在一個終端中啟動伺服器後，打開另一個終端並執行以下指令：

```bash
mcp dev server.py
```

這將啟動一個具有視覺介面的網頁伺服器，讓您可以測試範例。

伺服器連接後：

- 嘗試列出工具並執行 `add`，使用參數 2 和 4，您應該在結果中看到 6。

- 前往資源和資源模板，呼叫 `get_greeting`，輸入一個名字，您應該會看到包含您提供名字的問候語。

### 在 CLI 模式下測試

您啟動的檢查器實際上是一個 Node.js 應用程式，而 `mcp dev` 是其外層包裝。

您可以直接以 CLI 模式啟動，執行以下指令：

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

這將列出伺服器中所有可用的工具。您應該會看到以下輸出：

```text
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      }
    }
  ]
}
```

要調用工具，請輸入：

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

您應該會看到以下輸出：

```text
{
  "content": [
    {
      "type": "text",
      "text": "3"
    }
  ],
  "isError": false
}
```

> [!TIP]  
> 在 CLI 模式下執行檢查器通常比在瀏覽器中快得多。  
> 在[此處](https://github.com/modelcontextprotocol/inspector)了解更多有關檢查器的資訊。

**免責聲明**：  
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。儘管我們努力確保翻譯的準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於關鍵信息，建議使用專業人工翻譯。我們對因使用此翻譯而引起的任何誤解或錯誤解釋不承擔責任。