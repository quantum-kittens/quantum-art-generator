import re
from collections import defaultdict, deque

from flask import Flask, Markup, render_template, request
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy

#from codes import *
from quantum_art import QuantumArt

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import base64
import io

###############################################################################
# To run this on an actual quantum device, uncomment the following lines, and
# comment out `backend = BasicAer.get_backend("qasm_simulator")`. Then
# uncomment the lines in the `get class` section of the character generator
# as described further down.
###############################################################################

# IBMQ.save_account("ibmq-token-goes-here")
# provider = IBMQ.load_account()
# backend = least_busy(
#     provider.backends(
#         filters=lambda x: x.configuration().n_qubits >= 5
#         and not x.configuration().simulator
#         and x.status().operational == True
#     )
# )

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
        
        # Generate all possibilities: Ideal, 0.01, 0.05, etc.
        Art1 = QuantumArt(text=user_replies[0])
        fig_name_noiseless=Art1.get_fname()

        Art1.noise_art(custom_noise_vals=[0.01,0.01],fig_identifier='1')
        fig_name_noise1=Art1.get_fname()

        Art1.noise_art(custom_noise_vals=[0.05,0.05],fig_identifier='2')
        fig_name_noise2=Art1.get_fname()
        
        # Encoding image data to pass through; allows for dynamic images
        ### Noiseless
        #im = Image.open("static/noiseless.png")
        #data = io.BytesIO()
        #im.save(data, "PNG")
        #encoded_img_data_noiseless = base64.b64encode(data.getvalue())
        
        ### Noise 1
        #im = Image.open("static/with_noise1.png")
        #data = io.BytesIO()
        #im.save(data, "PNG")
        #encoded_img_data_with_noise1 = base64.b64encode(data.getvalue())
        
        
        
        return render_template(
            "preset_generator.html",
            #noiseless_img_data=encoded_img_data_noiseless.decode('utf-8'),
            #with_noise1_img_data=encoded_img_data_with_noise1.decode('utf-8'),
            fname_noiseless = fig_name_noiseless + ".png",
            fname_noise1 = fig_name_noise1 + ".png",
            fname_noise2 = fig_name_noise2 + ".png",
            
            
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
        fig_name=Art2.get_fname()

        return render_template(
            "custom_generator.html",
            fname = fig_name + ".png",
            text = user_replies[0],
            p_meas=user_replies[1],
            p_gate1=user_replies[2],
            answered=True,
        )
        
        


## No caching at all for API endpoints.
#@app.after_request
#def add_header(response):
#    # response.cache_control.no_store = True
#    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#    response.headers['Pragma'] = 'no-cache'
#    response.headers['Expires'] = '-1'
#    return response



if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    