import random

from prefect import flow, task


@task
def get_customer_ids():
    # Returning Customer Id's
    return [f"customer_id-{random.randint(1, 100)}" for _ in range(10)]


@task
def process_customer(customer_id: str):
    # Processing customer Id
    return f"Processed {customer_id}"


@flow(log_prints=True)
def main():
    customers = get_customer_ids()
    print("Fetched Customers Successfully...")

    # Process the Customers
    results = process_customer.map(customers)
    print("Processed Customers Data Successfully...")
    return results


@flow(log_prints=True)
def explain_flows():
    print("This is Python Code:")
    print("This is to show how the Flow is working")


if __name__ == "__main__":
    explain_flows()
    main()
