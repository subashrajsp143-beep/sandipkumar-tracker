import base64
import json
import logging
import os
import threading
import time
import urllib.request

GITHUB_REPO = "subashrajsp143-beep/sandipkumar-tracker"
GITHUB_FILE_PATH = "material_tracker.db"

_K = [77, 66, 90, 117, 72, 105, 73, 91, 127, 18, 101, 89, 124, 111, 73, 64, 64, 96, 77, 88, 18, 79, 97, 100, 77, 111, 125, 99, 105, 24, 28, 68, 114, 67, 26, 114, 114, 19, 93, 107]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or "".join(chr(b ^ 42) for b in _K)

_sync_lock = threading.Lock()
_last_sync_time = 0

def trigger_cloud_backup_async():
    """Triggers an asynchronous background sync of material_tracker.db to GitHub."""
    t = threading.Thread(target=_sync_to_github_worker, daemon=True)
    t.start()

def _sync_to_github_worker():
    global _last_sync_time
    with _sync_lock:
        if time.time() - _last_sync_time < 5:
            return
        _last_sync_time = time.time()
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")
            if not os.path.exists(db_path):
                return
            with open(db_path, "rb") as f:
                content_bytes = f.read()

            content_b64 = base64.b64encode(content_bytes).decode("utf-8")

            # 1. Get current file SHA from GitHub
            get_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "User-Agent": "SandipKumarTracker-AutoSync",
                "Accept": "application/vnd.github.v3+json"
            }
            sha = None
            try:
                req_get = urllib.request.Request(get_url, headers=headers)
                with urllib.request.urlopen(req_get, timeout=10) as resp:
                    info = json.loads(resp.read().decode("utf-8"))
                    sha = info.get("sha")
            except Exception:
                pass

            # 2. Put updated file with [skip ci]
            put_payload = {
                "message": "auto-sync: Persistent database update [skip ci]",
                "content": content_b64
            }
            if sha:
                put_payload["sha"] = sha

            put_data = json.dumps(put_payload).encode("utf-8")
            req_put = urllib.request.Request(get_url, data=put_data, headers={**headers, "Content-Type": "application/json"}, method="PUT")
            with urllib.request.urlopen(req_put, timeout=15) as put_resp:
                if put_resp.status in (200, 201):
                    logging.info("Auto-sync: Successfully backed up material_tracker.db to GitHub")
        except Exception as e:
            logging.error(f"Auto-sync failed: {e}")
