from datetime import UTC, datetime, timedelta

expiry_in_seconds = 1800
token_expiry_time = datetime.now(tz=UTC) + timedelta(seconds=expiry_in_seconds)
