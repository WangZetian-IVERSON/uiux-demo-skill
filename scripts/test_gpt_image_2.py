"""Quick capability test for newapi.pockgo.com gpt-image-2."""
import json
import os
import sys
import urllib.request

API = "https://newapi.pockgo.com/v1/images/generations"
KEY = "sk-Im00sXabBsZqWVB5ZwcQ2bKhmX5b44s6bVkKO9kb5410mY0W"

payload = {
    "model": "gpt-image-2",
    "prompt": "a small red apple on a clean white background, studio product photo, soft light",
    "size": "1024x1024",
    "n": 1,
}

req = urllib.request.Request(
    API,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KEY}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = resp.read().decode("utf-8")
        data = json.loads(body)
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode("utf-8", "replace")[:1500])
    sys.exit(1)
except Exception as e:
    print("ERR:", type(e).__name__, e)
    sys.exit(1)

print("TOP_KEYS:", list(data.keys()))
if "error" in data:
    print("ERROR:", json.dumps(data["error"], ensure_ascii=False)[:600])
items = data.get("data", [])
print("N_IMAGES:", len(items))
if items:
    item = items[0]
    print("ITEM_FIELDS:", list(item.keys()))
    print("HAS_URL:", bool(item.get("url")))
    print("HAS_B64:", bool(item.get("b64_json")))
    if item.get("url"):
        print("URL_PREVIEW:", item["url"][:120])
    if item.get("b64_json"):
        out = os.path.join(os.path.dirname(__file__), "..", "generated-images", "_capability_test_apple.png")
        out = os.path.abspath(out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        import base64
        with open(out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
        print("SAVED:", out, os.path.getsize(out), "bytes")
print("USAGE:", data.get("usage"))
