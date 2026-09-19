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
    """Create a GStreamer pipeline for the Jetson Nano CSI camera."""
    return (
        "nvarguscamerasrc sensor-id=0 ! "
        f"video/x-raw(memory:NVMM), width=(int){capture_width}, "
        f"height=(int){capture_height}, format=(string)NV12, "
        f"framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){display_width}, "
        f"height=(int){display_height}, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
        "appsink drop=true max-buffers=1 sync=false"
    )


def region_of_interest(edges):
    """
    Keep only a trapezoid in the lower portion of the image.

    This removes edges from walls, ceilings, furniture, and other
    objects that are less likely to be lane markings.
    """
    height, width = edges.shape

    polygon = np.array(
        [[
            (0, height),
            (int(width * 0.38), int(height * 0.55)),
            (int(width * 0.62), int(height * 0.55)),
            (width, height),
        ]],
        dtype=np.int32,
    )

    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, polygon, 255)

    return cv2.bitwise_and(edges, mask)


def make_line_points(image, slope, intercept):
    """Convert a slope/intercept line into two display points."""
    height, width = image.shape[:2]

    y1 = height
    y2 = int(height * 0.58)

    # Protect against a nearly horizontal line.
    if abs(slope) < 0.001:
        return None

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    # Prevent extremely large coordinates.
    x1 = max(-width, min(width * 2, x1))
    x2 = max(-width, min(width * 2, x2))

    return x1, y1, x2, y2


def average_lane_lines(image, line_segments):
    """
    Separate line segments into left and right groups and average them.
    """
    if line_segments is None:
        return []

    left_fits = []
    right_fits = []

    height, width = image.shape[:2]
    image_center = width / 2

    for segment in line_segments:
        x1, y1, x2, y2 = segment.reshape(4)

        if x1 == x2:
            continue

        slope, intercept = np.polyfit((x1, x2), (y1, y2), 1)

        # Ignore nearly horizontal lines.
        if abs(slope) < 0.35:
            continue

        if slope < 0 and x1 < image_center and x2 < image_center:
            left_fits.append((slope, intercept))
        elif slope > 0 and x1 > image_center and x2 > image_center:
            right_fits.append((slope, intercept))

    lane_lines = []

    if left_fits:
        left_average = np.mean(left_fits, axis=0)
        points = make_line_points(
            image,
            left_average[0],
            left_average[1],
        )
        if points:
            lane_lines.append(points)

    if right_fits:
        right_average = np.mean(right_fits, axis=0)
        points = make_line_points(
            image,
            right_average[0],
            right_average[1],
        )
        if points:
            lane_lines.append(points)

    return lane_lines


def draw_lane_lines(image, lane_lines):
    """Draw detected lane lines on a blank image."""
    line_image = np.zeros_like(image)

    for x1, y1, x2, y2 in lane_lines:
        cv2.line(
            line_image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            6,
        )

    return cv2.addWeighted(image, 0.8, line_image, 1.0, 0)


def main():
    pipeline = gstreamer_pipeline()

    print("Opening CSI camera...")
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("ERROR: Could not open CSI camera.")
        return

    print("Camera opened.")
    print("Press q in a camera window to quit.")

    try:
        while True:
            success, frame = cap.read()

            if not success:
                print("ERROR: Could not read camera frame.")
                break

            # Stage 1: grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Reduce small amounts of image noise.
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Stage 2: edge detection
            edges = cv2.Canny(
                blurred,
                threshold1=50,
                threshold2=150,
            )

            # Stage 3: keep only likely road/lane area
            cropped_edges = region_of_interest(edges)

            # Detect line segments.
            segments = cv2.HoughLinesP(
                cropped_edges,
                rho=2,
                theta=np.pi / 180,
                threshold=35,
                minLineLength=30,
                maxLineGap=50,
            )

            lane_lines = average_lane_lines(frame, segments)
            lane_overlay = draw_lane_lines(frame, lane_lines)

            # Show the region being searched in yellow.
            height, width = frame.shape[:2]
            roi_points = np.array(
                [
                    (0, height),
                    (int(width * 0.38), int(height * 0.55)),
                    (int(width * 0.62), int(height * 0.55)),
                    (width, height),
                ],
                dtype=np.int32,
            )

            cv2.polylines(
                lane_overlay,
                [roi_points],
                isClosed=True,
                color=(0, 255, 255),
                thickness=2,
            )

            status = f"Detected lane lines: {len(lane_lines)}"
            cv2.putText(
                lane_overlay,
                status,
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.imshow("1 - Original", frame)
            cv2.imshow("2 - Grayscale", gray)
            cv2.imshow("3 - Canny Edges", cropped_edges)
            cv2.imshow("4 - Lane Detection", lane_overlay)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")


if __name__ == "__main__":
    main()