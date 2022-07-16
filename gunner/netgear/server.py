import os
import asyncio

from vidgear.gears.asyncio import NetGear_Async


<<<<<<< Updated upstream:gunner/netgear/server.py
if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(__file__))
    INPUT = "test_video.mp4"
    server = NetGear_Async(
        source=INPUT,
        address="192.168.201.5",
=======
def start_netgear_server(video_to_send:str):
    """In this example, the server sends the video to the client.
    This method starts the server and starts sending the video to a connected client on the specified address."""
    server = NetGear_Async(
        source=video_to_send,
        address="localhost",  # Replace this with your IP.
>>>>>>> Stashed changes:gunner/vidgear/server.py
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
<<<<<<< Updated upstream:gunner/netgear/server.py
        
=======


if __name__ == "__main__":
    start_netgear_server()
>>>>>>> Stashed changes:gunner/vidgear/server.py
