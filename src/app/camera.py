import cv2

def startStream():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            endStream(cam)
            break
            # code for saving frames
        # elif k%256 == 32:
        #     # SPACE pressed
        #     img_name = "opencv_frame_{}.png".format(img_counter)
        #     cv2.imwrite(img_name, frame)
        #     print("{} written!".format(img_name))
        #     img_counter += 1


def endStream(cam):
    cam.release()
    cv2.destroyAllWindows()


# def main():
#     startStream()
# if __name__ == "__main__":
#     main()
