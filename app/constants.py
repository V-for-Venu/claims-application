from datetime import datetime, timedelta, timezone

expiry_in_seconds = 1800
token_expiry_time = datetime.now(tz=timezone.utc) + timedelta(seconds=expiry_in_seconds)
