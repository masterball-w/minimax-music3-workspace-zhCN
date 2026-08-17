"""稳健分片下载器:requests + Range 断点续传 + 自动重试。"""

import json
import os
import sys
import time

import requests

REPO = "MiniMaxAI/MiniMax-Music3"
ROOT = r"d:\program\misc\make-music\models\MiniMax-Music3"
BASE = f"https://huggingface.co/{REPO}/resolve/main"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def target_files():
    files = []
    for comp in ["language_model"]:
        d = os.path.join(ROOT, comp)
        idx = os.path.join(d, "model.safetensors.index.json")
        with open(idx) as f:
            shards = sorted(set(json.load(f)["weight_map"].values()))
        files += [f"{comp}/{s}" for s in shards]
    return files


def remote_size(path, session):
    r = session.head(f"{BASE}/{path}", allow_redirects=True, timeout=60)
    r.raise_for_status()
    return int(r.headers["Content-Length"])


def download(path, session, max_retries=50):
    dest = os.path.join(ROOT, path.replace("/", os.sep))
    tmp = dest + ".part"
    url = f"{BASE}/{path}"
    for attempt in range(max_retries):
        try:
            total = remote_size(path, session)
            have = os.path.getsize(tmp) if os.path.exists(tmp) else 0
            if have >= total:
                break
            headers = {"Range": f"bytes={have}-"}
            with session.get(url, headers=headers, stream=True, timeout=(20, 120)) as r:
                if r.status_code not in (200, 206):
                    raise RuntimeError(f"HTTP {r.status_code}")
                mode = "ab" if r.status_code == 206 else "wb"
                with open(tmp, mode) as f:
                    for chunk in r.iter_content(chunk_size=4 * 1024 * 1024):
                        f.write(chunk)
            if os.path.getsize(tmp) >= total:
                break
        except Exception as e:
            print(f"[{path}] attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(min(2 + attempt, 15))
    else:
        raise RuntimeError(f"{path}: 下载失败,重试耗尽")

    os.replace(tmp, dest)
    print(f"[OK] {path} ({os.path.getsize(dest)/1024**3:.2f} GB)", flush=True)


def main():
    use_proxy = "--proxy" in sys.argv
    session = requests.Session()
    session.proxies = PROXIES if use_proxy else None
    files = target_files()
    print(f"待下载 {len(files)} 个文件", flush=True)
    for p in files:
        download(p, session)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
