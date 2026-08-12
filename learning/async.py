# Demonstration of Async using Coffee and Toast Example
# Making cofee takes 5 seconds making toast takes 3 seconds
# Version:1 - Using Synchronous Programming
# Version:2 - Using Asynchronous Programming
import asyncio
import time


async def make_coffee():
    print("Starting Coffee Machine")
    await asyncio.sleep(5)
    print("Coffee Completed...!!!")
    return "Coffee Done"


async def make_toast():
    print("Starting Toast Machine")
    await asyncio.sleep(3)
    print("Toast Completed...!!!")
    return "Toast Done"


async def start_cafe():
    print("~~~~~ Opening Cafe ~~~~~")

    # Version::1
    start = time.perf_counter()

    # Synchronous Programming
    # for i in range(3):
    #     await make_coffee()
    #     await make_toast()

    # Implementing Asynchronous Programming

    preparations = []

    for _ in range(3):
        preparations.append(asyncio.create_task(make_coffee()))
        preparations.append(asyncio.create_task(make_toast()))

    done, _ = await asyncio.wait(preparations)

    end = time.perf_counter()

    for task in done:
        print("Result:- ", task.result())

    print(f"Total Time to Complete Orders: {round(end - start, 2)}")

    # Version::2
    start = time.perf_counter()
    results = await asyncio.gather(
        make_coffee(),
        make_toast(),
        make_coffee(),
        make_toast(),
        make_coffee(),
        make_toast(),
    )
    end = time.perf_counter()
    print(f"Total Time to Complete Order: {round(end - start, 2)}")
    print(f"Results List - {results}")


if __name__ == "__main__":
    asyncio.run(start_cafe())
