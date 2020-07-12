import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return what


async def main():
    print(f'started at {time.strftime("%X")}')

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f'finished at {time.strftime("%X")}')


async def main2():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f'started at {time.strftime("%X")}')
    await task1
    await task2
    if task1.done():
        print(task1.result())
    print(f'ended at {time.strftime("%X")}')


async def nested():
    return 42


async def main3():
    task = asyncio.create_task(nested())

    await task


async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print(f'Task {name}: Compute factorial({i}...')
        await asyncio.sleep(1)
        f *= i
    print(f'Task {name}: factorial({number} = {f}')


async def main5():
    await asyncio.gather(
        factorial('A', 2),
        factorial('B', 3),
        factorial('C', 4)
    )


async def eternity():
    await asyncio.sleep(3600)
    print('ok!')


async def main6():
    try:
        await asyncio.wait_for(eternity(), timeout=1)
    except asyncio.TimeoutError:
        print('timeout!')


async def foo():
    return 42


async def main7():
    task = asyncio.create_task(foo())
    done, pending = await asyncio.wait({task})

    if task in done:
        print('finished')


async def set_after(fut: asyncio.Future, delay, value):
    await asyncio.sleep(delay)

    fut.set_result(value)


async def main8():
    loop = asyncio.get_running_loop()

    fut = loop.create_future()
    loop.call_later(10, lambda x: print(f'Hello {x}'), 'NONONO')

    loop.create_task(set_after(fut, 1, '...world'))
    print('hello...')

    print(await fut)


if __name__ == '__main__':
    asyncio.run(main8())
