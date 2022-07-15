from vidgear.gears.asyncio import NetGear_Async
from vidgear.gears import WriteGear

import cv2
import asyncio

client = NetGear_Async(
    address="192.168.201.5",
    port="8081",
    protocol="tcp",
    pattern=1,
    receive_mode=True,
    logging=True,
).launch()


# retrieve framerate from CamGear Stream and pass it as `-input_framerate` parameter
output_params = {"-pix_fmt": "yuv420p"}
writer = WriteGear(output_filename="Output.mp4", logging=True, **output_params)


async def main():
    async for frame in client.recv_generator():
        writer.write(frame)
        #cv2.imshow("Output Frame", frame)
        #key = cv2.waitKey(1) & 0xFF
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
