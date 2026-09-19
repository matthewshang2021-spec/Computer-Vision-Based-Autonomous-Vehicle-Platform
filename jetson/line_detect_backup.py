import cv2
import numpy as np


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, "
        "format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=true"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


cap = cv2.VideoCapture(
    gstreamer_pipeline(),
    cv2.CAP_GSTREAMER
)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()

print("Camera opened.")
print("Press q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read frame.")
        break

    height, width = frame.shape[:2]

    # -------------------------------------------------
    # 1. Use only the lower part of the image
    # -------------------------------------------------
    roi_top = int(height * 0.55)
    roi_bottom = int(height * 0.95)

    roi = frame[roi_top:roi_bottom, :]

    # -------------------------------------------------
    # 2. Convert ROI to grayscale
    # -------------------------------------------------
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Small blur helps remove camera noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # -------------------------------------------------
    # 3. Convert dark line into WHITE pixels
    # -------------------------------------------------
    threshold_value, mask = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # -------------------------------------------------
    # 4. Find black-line regions
    # -------------------------------------------------
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    line_found = False

    if contours:
        # Find the largest dark region
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        # Ignore tiny dark spots/noise
        if area > 500:
            moments = cv2.moments(largest)

            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

                image_center = width // 2

                # Positive error means line is to the RIGHT
                # Negative error means line is to the LEFT
                error = cx - image_center

                if error < -20:
                    direction = "LEFT"
                elif error > 20:
                    direction = "RIGHT"
                else:
                    direction = "CENTER"

                line_found = True

                # Draw detected contour in ROI
                cv2.drawContours(roi, [largest], -1, (0, 255, 0), 2)

                # Blue dot = detected center of black line
                cv2.circle(
                    roi,
                    (cx, cy),
                    8,
                    (255, 0, 0),
                    -1
                )

                # Red line = image center
                cv2.line(
                    roi,
                    (image_center, 0),
                    (image_center, roi.shape[0]),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "error = %d" % error,
                    (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    direction,
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                   (0, 255, 255),
                   2
                )

                print(
                    "line_center=%d  image_center=%d  error=%d  area=%d"
                    % (cx, image_center, error, area)
                )

    if not line_found:
        cv2.putText(
            frame,
            "LINE NOT FOUND",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # Draw ROI boundaries on original image
    cv2.line(
        frame,
        (0, roi_top),
        (width, roi_top),
        (255, 255, 0),
        2
    )

    cv2.line(
        frame,
        (0, roi_bottom),
        (width, roi_bottom),
        (255, 255, 0),
        2
    )

    cv2.imshow("Camera", frame)
    cv2.imshow("Black Line Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()