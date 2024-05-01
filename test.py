import asyncio
import time

async def main():
    start = time.perf_counter()
    await asyncio.sleep(1)  # Intended sleep for 1 second
    elapsed = time.perf_counter() - start
    print(f"Sleep was intended for 1 second. Actual time elapsed: {elapsed:.2f} seconds.")

asyncio.run(main())
