import asyncio

from vidgear.gears.asyncio import NetGear_Async


def start_netgear_server(video_to_send:str):
    """In this example, the server sends the video to the client.
    This method starts the server and starts sending the video to a connected client on the specified address."""
    server = NetGear_Async(
        source=video_to_send,
        address="192.168.0.12",  # Replace this with your IP.
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


if __name__ == "__main__":
    import os

    test_video = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test_video.mp4")
    start_netgear_server(test_video)
