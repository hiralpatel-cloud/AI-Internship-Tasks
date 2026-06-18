import cv2

img = cv2.imread("image.jpg")


resized = cv2.resize(img, (500, 500))
cv2.imshow("Resized Image", resized)
cv2.imwrite("resized.jpg", resized)

cropped = img[50:300, 50:300]
cv2.imshow("Cropped Image", cropped)
cv2.imwrite("cropped.jpg", cropped)

rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imshow("Rotated Image", rotated)
cv2.imwrite("rotated.jpg",rotated)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image", gray)
cv2.imwrite("gray.jpg", gray)

blur = cv2.GaussianBlur(gray, (15, 15), 0)
cv2.imshow("Blurred Image", blur)
cv2.imwrite("blur.jpg", blur)

edges = cv2.Canny(gray, 100, 200)
cv2.imshow("Edge Detection", edges)
cv2.imwrite("edges.jpg", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
