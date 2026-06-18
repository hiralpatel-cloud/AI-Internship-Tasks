import cv2
import time

cap = cv2.VideoCapture(0)  

prev_time = 0

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Webcam', frame)
    
    out.write(frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        cv2.imwrite(f'photo_{frame_count}.jpg', frame)
        print(f"Photo saved: photo_{frame_count}.jpg")
        frame_count += 1
    
    elif key == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
