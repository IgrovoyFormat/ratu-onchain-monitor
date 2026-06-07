# main_worker.py
import schedule, time, os
from src.onchain_monitor.ankr_client import AnkrClient
from src.onchain_monitor.snapshot import build_snapshot

CONTRACT = os.environ["CONTRACT_ADDRESS"]
CHAIN    = os.environ.get("CHAIN", "bsc")
DISCORD  = os.environ["DISCORD_WEBHOOK_URL"]

def job():
    client = AnkrClient()
    holders = client.get_top_holders(CONTRACT, CHAIN, limit=20)
    # форматируй и шли в Discord через requests.post(DISCORD, ...)

schedule.every(1).hours.do(job)
while True:
    schedule.run_pending()
    time.sleep(60)
