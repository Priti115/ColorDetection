from flask import Flask, request, jsonify, send_file
import cv2 as cv
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load color data from CSV
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Calculate closest color
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Routes
@app.route('/')
def home():
    return send_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Read the image using OpenCV
    img = cv.imread(file_path)

    # Check if image is read successfully
    if img is None:
        return jsonify({"error": "Failed to read image with OpenCV"})

    # Variables
    clicked = False
    r = g = b = x_pos = y_pos = 0

    # Function to handle double-click and capture color
    def draw_function(event, x, y, flags, param):
        nonlocal clicked, b, g, r, x_pos, y_pos
        if event == cv.EVENT_LBUTTONDBLCLK:
            clicked = True
            x_pos, y_pos = x, y
            b, g, r = img[y, x]
            b, g, r = int(b), int(g), int(r)

    # Set up the OpenCV window with default size
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.setMouseCallback('image', draw_function)

    while True:
        cv.imshow('image', img)

        if clicked:
            # Draw a larger rectangle for better visibility
            cv.rectangle(img, (20, 20), (800, 80), (b, g, r), -1)
            text = f"{get_color_name(r, g, b)} R={r} G={g} B={b}"

            # Display text in black or white depending on brightness
            color = (0, 0, 0) if (r + g + b >= 600) else (255, 255, 255)
            cv.putText(img, text, (30, 60), 2, 1, color, 2, cv.LINE_AA)
            clicked = False

        # Exit using ESC key
        if cv.waitKey(20) & 0xFF == 27:
            break

    cv.destroyAllWindows()

    return jsonify({"message": "Image displayed using OpenCV. Close the window to proceed."})

if __name__ == '__main__':
    app.run(debug=True)