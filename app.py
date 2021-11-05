import re
from collections import defaultdict, deque

from flask import Flask, Markup, render_template, request
from qiskit import IBMQ, BasicAer

from code import *


from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import base64
import io

backend = BasicAer.get_backend("qasm_simulator")


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route("/")
def index():
    return render_template("index.html")

preset_user_categories = ["USER_TEXT"]

@app.route("/preset", methods=["GET", "POST"])
def preset():
    if request.method != "POST":
        user_categories = preset_user_categories
        return render_template(
            "preset_generator.html", categories=user_categories, answered=False,
        )
    else:
        user_categories = preset_user_categories
        user_replies = [request.form.get(category) for category in user_categories]
        
        # Generate six possibilities: Ideal, 0.01, 0.05, etc.
        
        ### Ideal
        Art1 = QuantumArt(text=user_replies[0])
        
        buffer_image = Art1.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_ideal_img_data = base64.b64encode(data.getvalue())
        
        ### 0.01
        Art1.noise_art(custom_noise_vals=[0.01,0.01],fig_identifier='1')
        
        buffer_image = Art1.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_noise_img1_data = base64.b64encode(data.getvalue())
        
        ### 0.05
        Art1.noise_art(custom_noise_vals=[0.05,0.05],fig_identifier='2')
        
        buffer_image = Art1.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_noise_img2_data = base64.b64encode(data.getvalue())
        
        ### 0.1
        Art1.noise_art(custom_noise_vals=[0.1,0.1],fig_identifier='3')
        
        buffer_image = Art1.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_noise_img3_data = base64.b64encode(data.getvalue())
        
        ### 0.2
        Art1.noise_art(custom_noise_vals=[0.2,0.2],fig_identifier='4')
        
        buffer_image = Art1.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_noise_img4_data = base64.b64encode(data.getvalue())
        
        ### 0.5
        Art1.noise_art(custom_noise_vals=[0.5,0.5],fig_identifier='5')
        
        buffer_image = Art1.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_noise_img5_data = base64.b64encode(data.getvalue())
        
        
        
        return render_template(
            "preset_generator.html",
            ideal_img = encoded_ideal_img_data.decode('utf-8'),
            noise_img1 = encoded_noise_img1_data.decode('utf-8'),
            noise_img2 = encoded_noise_img2_data.decode('utf-8'),
            noise_img3 = encoded_noise_img3_data.decode('utf-8'),
            noise_img4 = encoded_noise_img4_data.decode('utf-8'),
            noise_img5 = encoded_noise_img5_data.decode('utf-8'),
            text = user_replies[0],
            answered=True,
        )

custom_user_categories = ["text", "p_meas", "p_gate1"]

@app.route("/custom", methods=["GET", "POST"])
def custom():
    if request.method != "POST":        
        return render_template(
            "custom_generator.html", categories=custom_user_categories, answered=False,
        )
    else:

        user_categories = custom_user_categories
        user_replies = [request.form.get(category) for category in user_categories]
        
        Art2 = QuantumArt(text=user_replies[0])
        Art2.noise_art(custom_noise_vals=[float(user_replies[1]),float(user_replies[2])],fig_identifier='3')
        
        buffer_image = Art2.get_buffer_image()
        im = Image.open(buffer_image)
        
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_img_data_with_noise1 = base64.b64encode(data.getvalue())

        return render_template(
            "custom_generator.html",
            noise_img = encoded_img_data_with_noise1.decode('utf-8'),
            text = user_replies[0],
            p_meas=user_replies[1],
            p_gate1=user_replies[2],
            answered=True,
        )
        
    

if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    
