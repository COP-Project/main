import cv2
import readPlate

# runs an infinite loop until escape is pressed
def start_stream():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        # transform frame into jpg byte array so alpr can read it
        frame = cv2.imencode('.jpg', frame)[1].tostring()
        readPlate.read_plate_from_stream(frame, 'us')
        if not ret:
            break

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            endStream(cam, alpr)
            break



def end_stream(cam):
    cam.release()
    cv2.destroyAllWindows()


# def main():
#     startStream()
# if __name__ == "__main__":
#     main()
