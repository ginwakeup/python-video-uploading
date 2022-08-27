import cv2
import asyncio

from vidgear.gears.asyncio import NetGear_Async
from vidgear.gears import WriteGear


client = NetGear_Async(
    address="192.168.0.12",  # Replace this with your IP.
    port="8081",
    protocol="tcp",
    pattern=1,
    receive_mode=True,
    logging=True,
).launch()


# The following output_params are needed to play the video in "dumb players" as defined on ffmpeg docs.
# https://trac.ffmpeg.org/wiki/Encode/H.264#Encodingfordumbplayers
output_params = {"-pix_fmt": "yuv420p"}
writer = WriteGear(output_filename="Output.mp4", logging=True, **output_params)


async def main():
    async for frame in client.recv_generator():
        writer.write(frame)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.set_event_loop(client.loop)
    try:
        client.loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass

    cv2.destroyAllWindows()
    client.close()
    writer.close()
