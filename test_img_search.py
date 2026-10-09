import urllib.request
import urllib.parse
import json
import re

def search_online_images(query, count=4):
    search_q = urllib.parse.quote(query + " plumbing construction")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://duckduckgo.com/"
    }
    
    # Get token vqd
    req1 = urllib.request.Request("https://duckduckgo.com/?q=" + search_q, headers=headers)
    resp1 = urllib.request.urlopen(req1, timeout=6).read().decode("utf-8")
    m = re.search(r'vqd=([\d-]+)', resp1) or re.search(r'vqd="([^"]+)"', resp1)
    if not m:
        return []
    
    vqd = m.group(1)
    api_url = f"https://duckduckgo.com/i.js?q={search_q}&o=json&vqd={vqd}"
    req2 = urllib.request.Request(api_url, headers=headers)
    resp2 = urllib.request.urlopen(req2, timeout=6).read().decode("utf-8")
    data = json.loads(resp2)
    results = []
    for r in data.get("results", [])[:count]:
        img_url = r.get("image") or r.get("thumbnail")
        if img_url:
            results.append({
                "title": r.get("title", ""),
                "url": img_url,
                "thumb": r.get("thumbnail", img_url)
            })
    return results

if __name__ == "__main__":
    imgs = search_online_images("1 UPVC ELBOW")
    print(f"Found {len(imgs)} images:")
    for im in imgs:
        print(im)
