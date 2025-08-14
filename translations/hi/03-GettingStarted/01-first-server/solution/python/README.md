<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "d26f746e21775c30b4d7ed97962b24df",
  "translation_date": "2025-08-11T11:52:09+00:00",
  "source_file": "03-GettingStarted/01-first-server/solution/python/README.md",
  "language_code": "hi"
}
-->
# इस सैंपल को चलाना

आपको `uv` इंस्टॉल करने की सलाह दी जाती है, लेकिन यह अनिवार्य नहीं है। अधिक जानकारी के लिए देखें [निर्देश](https://docs.astral.sh/uv/#highlights)

## -0- एक वर्चुअल एनवायरनमेंट बनाएं

```bash
python -m venv venv
```

## -1- वर्चुअल एनवायरनमेंट को सक्रिय करें

```bash
venv\Scripts\activate
```

## -2- डिपेंडेंसीज़ इंस्टॉल करें

```bash
pip install "mcp[cli]"
```

## -3- सैंपल को चलाएं

```bash
mcp run server.py
```

## -4- सैंपल का परीक्षण करें

सर्वर को एक टर्मिनल में चलाते हुए, दूसरा टर्मिनल खोलें और निम्नलिखित कमांड चलाएं:

```bash
mcp dev server.py
```

यह एक वेब सर्वर शुरू करेगा जिसमें एक विज़ुअल इंटरफ़ेस होगा, जिससे आप सैंपल का परीक्षण कर सकते हैं।

सर्वर कनेक्ट होने के बाद:

- टूल्स की सूची देखने की कोशिश करें और `add` चलाएं, आर्ग्युमेंट्स 2 और 4 के साथ। आपको परिणाम में 6 दिखना चाहिए।

- रिसोर्सेज़ और रिसोर्स टेम्पलेट पर जाएं और `get_greeting` को कॉल करें। एक नाम टाइप करें और आपको उस नाम के साथ एक ग्रीटिंग दिखेगी जो आपने प्रदान किया है।

### CLI मोड में परीक्षण करना

जो इंस्पेक्टर आपने चलाया है, वह वास्तव में एक Node.js ऐप है और `mcp dev` इसका एक रैपर है।

आप इसे CLI मोड में सीधे निम्नलिखित कमांड चलाकर लॉन्च कर सकते हैं:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

यह सर्वर में उपलब्ध सभी टूल्स की सूची दिखाएगा। आपको निम्नलिखित आउटपुट दिखना चाहिए:

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

किसी टूल को इनवोक करने के लिए टाइप करें:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
```

आपको निम्नलिखित आउटपुट दिखना चाहिए:

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
> आमतौर पर CLI मोड में इंस्पेक्टर को चलाना ब्राउज़र की तुलना में बहुत तेज़ होता है। इंस्पेक्टर के बारे में और पढ़ें [यहां](https://github.com/modelcontextprotocol/inspector)।

**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता सुनिश्चित करने का प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या अशुद्धियां हो सकती हैं। मूल भाषा में उपलब्ध मूल दस्तावेज़ को आधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।