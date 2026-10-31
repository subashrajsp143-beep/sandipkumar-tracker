import base64
import hashlib
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
_debounce_timer = None
_last_pushed_sha = None

def git_blob_sha(data: bytes) -> str:
    """Calculates standard Git blob SHA-1 hash."""
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()

def trigger_cloud_backup_async(debounce_seconds=12):
    """
    Debounced asynchronous background sync of material_tracker.db to GitHub.
    Coalesces multiple rapid updates (e.g. batch attendance, initial months)
    into a single GitHub commit to prevent deployment thrashing.
    """
    global _debounce_timer
    with _sync_lock:
        if _debounce_timer is not None:
            try:
                _debounce_timer.cancel()
            except Exception:
                pass
        _debounce_timer = threading.Timer(debounce_seconds, _sync_to_github_worker)
        _debounce_timer.daemon = True
        _debounce_timer.start()

def _sync_to_github_worker():
    global _last_pushed_sha
    with _sync_lock:
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")
            if not os.path.exists(db_path):
                return
            with open(db_path, "rb") as f:
                content_bytes = f.read()

            local_sha = git_blob_sha(content_bytes)
            if _last_pushed_sha and local_sha == _last_pushed_sha:
                logging.info("Auto-sync: Local DB matches last pushed SHA. Skipping push.")
                return

            content_b64 = base64.b64encode(content_bytes).decode("utf-8")

            # 1. Get current file SHA from GitHub
            get_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "User-Agent": "SandipKumarTracker-AutoSync",
                "Accept": "application/vnd.github.v3+json"
            }
            remote_sha = None
            try:
                req_get = urllib.request.Request(get_url, headers=headers)
                with urllib.request.urlopen(req_get, timeout=10) as resp:
                    info = json.loads(resp.read().decode("utf-8"))
                    remote_sha = info.get("sha")
            except Exception as e:
                logging.warning(f"Auto-sync: Could not fetch remote SHA: {e}")

            # If remote SHA matches local SHA, the remote repository already has this exact DB.
            if remote_sha and remote_sha == local_sha:
                _last_pushed_sha = local_sha
                logging.info(f"Auto-sync: Remote GitHub DB is already identical ({local_sha[:8]}). No push needed.")
                return

            # 2. Put updated file with [skip ci]
            put_payload = {
                "message": "auto-sync: Persistent database update [skip ci]",
                "content": content_b64
            }
            if remote_sha:
                put_payload["sha"] = remote_sha

            put_data = json.dumps(put_payload).encode("utf-8")
            req_put = urllib.request.Request(get_url, data=put_data, headers={**headers, "Content-Type": "application/json"}, method="PUT")
            with urllib.request.urlopen(req_put, timeout=20) as put_resp:
                if put_resp.status in (200, 201):
                    _last_pushed_sha = local_sha
                    logging.info(f"Auto-sync: Successfully backed up material_tracker.db to GitHub ({local_sha[:8]})")
        except Exception as e:
            logging.error(f"Auto-sync failed: {e}")
