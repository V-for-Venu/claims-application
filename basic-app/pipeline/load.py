from datetime import datetime, timezone
from pathlib import Path

watermark_file = "watermark.txt"
GOLD_PATH = "data/gold"


def load_claim_data(results):

    # Generate Timestamp for Files and Folder
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M")

    # Generate Runtime Folder
    run_path = Path(GOLD_PATH) / timestamp
    run_path.mkdir(parents=True, exist_ok=True)

    for key, df in results.items():
        output_path = run_path / f"{key}.parquet"

        df.to_parquet(output_path, index=False)


def update_watermark(df):
    if not len(df):
        return

    latest_timestamp = df["ClaimAuditTime"].max()
    with open(watermark_file, "w") as file:
        file.write(str(latest_timestamp))
