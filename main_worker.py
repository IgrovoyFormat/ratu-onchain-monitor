import time, os, json, sys, urllib.request
from datetime import datetime

sys.path.insert(0, "/app/src")

from onchain_monitor.ankr_client import AnkrClient

CONTRACT = os.environ.get("CONTRACT_ADDRESS", "")
CHAIN    = os.environ.get("CHAIN", "bsc")
INTERVAL = int(os.environ.get("INTERVAL_MINUTES", "60"))
DISCORD  = os.environ.get("DISCORD_WEBHOOK_URL", "")

def run_job():
    print(f"[{datetime.utcnow()}] Scanning {CONTRACT} on {CHAIN}", flush=True)
    try:
        client = AnkrClient()
        meta = client.get_token_metadata(CONTRACT, CHAIN)
        print(json.dumps(meta, indent=2), flush=True)

        if DISCORD:
            msg = (
                f"**{meta.get('name')} ({meta.get('symbol')})**\n"
                f"Price: ${meta.get('usdPrice', 'N/A')}\n"
                f"Holders: {meta.get('holdersCount', 'N/A')}"
            )
            data = json.dumps({"content": msg}).encode()
            req = urllib.request.Request(
                DISCORD, data=data,
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req)
            print("Discord alert sent", flush=True)
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)

print(f"Worker started. Interval: {INTERVAL} min", flush=True)
while True:
    run_job()
    time.sleep(INTERVAL * 60)
