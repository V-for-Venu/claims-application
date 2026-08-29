from extract import extract_claims
from load import load_claim_data, update_watermark
from prefect import flow, task
from transform import transform_claims


@task
def extract_task():
    return extract_claims()


@task
def transform_task(df):
    return transform_claims(df)


@task
def load_task(result):
    return load_claim_data(result)


@task
def update_watermark_task(df):
    return update_watermark(df)


@flow(name="Claims_ETL_Pipeline", log_prints=True)
def claims_pipeline():
    df = extract_task()
    print("===:: Data Extracted Successfully ::===")
    if df.empty:
        return "No New Claims Found"

    result = transform_task(df)
    print("===:: Data Transformed Successfully ::===")
    load_task(result)
    print("===:: Data Loaded Successfully ::===")

    update_watermark_task(df)
    print("===:: Watermark Updated Successfully ::===")

    print(f"===:: Processed {len(df)} Records Successfully ::===")


if __name__ == "__main__":
    claims_pipeline.serve(name="claims-pipeline", cron="*/5 * * * *")
