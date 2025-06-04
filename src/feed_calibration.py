import cv2
import numpy as np
import os
from .feed_receiver import get_camera


def calibrate(camera_id: int, output_path: str, board_size=(9, 6)) -> None:
    if os.path.exists(output_path):
        print(f"📂 Calibration for camera {camera_id} already exists at: {output_path}")
        return

    cam = get_camera(camera_id)
    objpoints, imgpoints = [], []

    objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)

    print(f"🎯 Calibrating camera {camera_id}. Press ESC to stop.")

    while True:
        frame = cam.capture_array(wait=True)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, board_size)

        if ret:
            imgpoints.append(corners)
            objpoints.append(objp)
            cv2.drawChessboardCorners(frame, board_size, corners, ret)

        cv2.imshow(f"Calibration - Camera {camera_id}", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) == 27:
            break

    cam.stop()
    cv2.destroyAllWindows()

    if len(objpoints) >= 5:
        _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        np.savez(output_path, mtx=mtx, dist=dist)
        print(f"✅ Calibration saved: {output_path}")
    else:
        print("❌ Not enough valid captures for calibration.")
