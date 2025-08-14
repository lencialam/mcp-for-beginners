<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d26f746e21775c30b4d7ed97962b24df",
  "translation_date": "2025-08-11T11:22:36+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "fa"
}
-->
# اجرای این نمونه

توصیه می‌شود `uv` نصب کنید، اما ضروری نیست. برای اطلاعات بیشتر به [دستورالعمل‌ها](https://docs.astral.sh/uv/#highlights) مراجعه کنید.

## -0- ایجاد یک محیط مجازی

```bash
python -m venv venv
```

## -1- فعال‌سازی محیط مجازی

```bash
venv\Scripts\activate
```

## -2- نصب وابستگی‌ها

```bash
pip install "mcp[cli]"
```

## -3- اجرای نمونه

```bash
mcp run server.py
```

## -4- آزمایش نمونه

با اجرای سرور در یک ترمینال، یک ترمینال دیگر باز کنید و دستور زیر را اجرا کنید:

```bash
mcp dev server.py
```

این باید یک سرور وب با رابط بصری راه‌اندازی کند که به شما امکان آزمایش نمونه را می‌دهد.

پس از اتصال سرور:

- ابزارها را لیست کنید و `add` را اجرا کنید، با آرگومان‌های ۲ و ۴، باید نتیجه ۶ را مشاهده کنید.

- به منابع و قالب منابع بروید و `get_greeting` را فراخوانی کنید، یک نام وارد کنید و باید یک پیام خوش‌آمدگویی با نامی که وارد کرده‌اید مشاهده کنید.

### آزمایش در حالت CLI

بازرس که اجرا کردید در واقع یک اپلیکیشن Node.js است و `mcp dev` یک پوشش برای آن است.

می‌توانید آن را مستقیماً در حالت CLI با اجرای دستور زیر راه‌اندازی کنید:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

این تمام ابزارهای موجود در سرور را لیست خواهد کرد. باید خروجی زیر را مشاهده کنید:

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

برای فراخوانی یک ابزار تایپ کنید:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

باید خروجی زیر را مشاهده کنید:

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

> ![!TIP]
> معمولاً اجرای بازرس در حالت CLI بسیار سریع‌تر از اجرا در مرورگر است.
> اطلاعات بیشتر درباره بازرس را [اینجا](https://github.com/modelcontextprotocol/inspector) بخوانید.

**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما تلاش می‌کنیم دقت را حفظ کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌ها باشند. سند اصلی به زبان اصلی آن باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، توصیه می‌شود از ترجمه انسانی حرفه‌ای استفاده کنید. ما مسئولیتی در قبال سوء تفاهم‌ها یا تفسیرهای نادرست ناشی از استفاده از این ترجمه نداریم.