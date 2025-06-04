from picamera2.picamera2 import Picamera2


def get_camera(camera_id: int, resolution=(1920, 1080)) -> Picamera2:
    cam = Picamera2(camera_num=camera_id)
    config = cam.create_still_configuration(main={"size": resolution})
    cam.configure(config)
    cam.start()
    return cam
