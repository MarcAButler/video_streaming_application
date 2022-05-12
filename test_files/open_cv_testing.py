#[SOURCES]
#https://stackoverflow.com/questions/40928205/python-opencv-image-to-byte-string-for-json-transfer

import cv2

# Define a video capture object
vid = cv2.VideoCapture(0)

while(True):
    # Caputure the video frame by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('Junk', frame)

    # The 'q' button is set as the quitting button you may use any desired button of your choice
    if cv2.waitKey(1) & (0xFF == ord('q')):
        break

# After the loop release the cap
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

####################################
####################################

# import cv2
# import base64

# import random
# import string

# cap = cv2.VideoCapture(0)
# retval, image = cap.read()
# cap.release()

# # Convert captured image to JPG
# retval, buffer = cv2.imencode('.jpg', image)

# # Convert to base64 encoding and show start of data
# jpg_as_text = base64.b64encode(buffer)
# print(jpg_as_text[:80])

# # Convert back to binary
# jpg_original = base64.b64decode(jpg_as_text)

# # GENERATES A RANDOM STRING WITH SIZE N
# def generate_string(size=28, chars=string.ascii_letters + string.digits):
#     return    ''.join(random.choice(chars) for _ in range(size))

# # Write to a file to show conversion worked
# with open(f'temp/{generate_string()}.jpg', 'wb') as f_output:
#     f_output.write(jpg_original)



