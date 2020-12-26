from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send
from io import StringIO
import io
import base64
from PIL import Image
import cv2
import numpy as np
import imutils
from videoStreaming import predictXception

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("image")
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    frame = predictXception(frame)
    if frame is None:
        emit("response_back", None)
        return

    imgencode = cv2.imencode(".jpg", frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode("utf-8")
    b64_src = "data:image/jpg;base64,"
    stringData = b64_src + stringData

    # emit the frame back
    emit("response_back", stringData)


if __name__ == "__main__":
    # print("app is  running")
    # socketio.run(app, host='0.0.0.0', port=3000)
    # socketio.run(app, port=3000)
    socketio.run(debug = True)
