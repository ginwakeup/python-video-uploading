import os
import asyncio

from vidgear.gears.asyncio import NetGear_Async


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(__file__))
    INPUT = "test_video.mp4"
    server = NetGear_Async(
        source=INPUT,
        address="192.168.201.5",
        port="8081",
        protocol="tcp",
        pattern=1,
        logging=True,
    ).launch()

    asyncio.set_event_loop(server.loop)
    try:
        server.loop.run_until_complete(server.task)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        server.close()
        