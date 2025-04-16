### Terminal 1:
```bash
ngrok http 8000  # Get forwarding link
```

### Terminal 2:
```
Invoke-RestMethod -Uri "https://api.telegram.org/bot<ngrok_auth_token>/setWebhook" `
    -Method POST `
    -Body @{ url = "<forwardinglink>/webhook" }
```

### Terminal 3:
```
$env:PYTHONPATH = "src"
uvicorn src.main:app --reload
```
