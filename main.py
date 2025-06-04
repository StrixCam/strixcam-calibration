from src.feed_calibration import calibrate

def main():
    calibrate(0, "data/calibration_cam0.npz")
    calibrate(1, "data/calibration_cam1.npz")

if __name__ == "__main__":
    main()
