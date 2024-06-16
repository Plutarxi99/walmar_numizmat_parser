import asyncio
import time

from get_info_lot_bids.async_src.get import gather_data

start_time = time.time()


# Затраченное на работу скрипта время: 425.98178791999817 (на 1 аукцион 1985)
def main():
    asyncio.run(gather_data())
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    main()
