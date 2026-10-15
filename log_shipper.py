#!/usr/bin/env python3
"""APEX Log Shipper — tails apex.log and POSTs new lines to the dashboard."""
import time, os, requests, hashlib

URL   = "https://apex-crypto.abacusai.app/api/ingest"
LOG   = os.path.expanduser("~/trading-agent/apex.log")

def read_token():
    tok = os.environ.get("INGEST_TOKEN", "")
    try:
        with open(os.path.expanduser("~/trading-agent/.env")) as f:
            for line in f:
                if line.startswith("INGEST_TOKEN="):
                    tok = line.split("=", 1)[1].strip().strip('"')
    except Exception:
        pass
    return tok

TOKEN = read_token()
BATCH = 30  # seconds between sends

def tail(path, pos=0):
    try:
        with open(path, 'r') as f:
            f.seek(pos)
            lines = f.readlines()
            return lines, f.tell()
    except FileNotFoundError:
        return [], pos

def ship(lines):
    if not lines:
        return
    try:
        r = requests.post(URL, json={"lines": lines},
                         headers={"Authorization": f"Bearer {TOKEN}"},
                         timeout=15)
        if r.status_code == 200:
            data = r.json()
            print(f"Shipped {len(lines)} lines, inserted {data.get('inserted',0)}")
        else:
            print(f"Ship error: {r.status_code}")
    except Exception as e:
        print(f"Ship error: {e}")

if __name__ == '__main__':
    print("APEX Log Shipper starting...")
    print(f"URL: {URL}")
    print(f"Log: {LOG}")
    pos = 0
    # Start from end of file
    try:
        pos = os.path.getsize(LOG)
    except:
        pass
    while True:
        lines, pos = tail(LOG, pos)
        stripped = [l.strip() for l in lines if l.strip()]
        ship(stripped)
        time.sleep(BATCH)
