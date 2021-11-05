from qiskit import *
from qiskit import IBMQ, QuantumRegister, ClassicalRegister, QuantumCircuit, assemble
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import string
import uuid
import io

from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error, depolarizing_error
from qiskit.providers.aer import AerSimulator


class QuantumArt:
    def __init__(self, text = '',  n = 5, art_type = 'bubble', dpi = 3000, shots = 1024, fig_identifier = '0'):
        self.n = n # number of qubits on device
        self.art_type = art_type
        self.dpi = dpi # default 1200, recommend 3000 for high resolution
        self.shots = shots
        
        self.text = self.get_text(text) # linguistic input from user
        self.bit_string = self.text2bits() # bit string of text
        self.bit_string_length = len(self.bit_string)
        self.bits_split = self.split_bits() 
        self.circuits = self.build_circuits(self.bits_split)

        self.ideal_bubble_area = []
        self.ideal_color_list = []
        
        self.noisy_ideal_count_outcomes = []
        self.noise_float_list = []
        self.noise_bubble_area = []
        self.noise_color_list = []
        
        self.fig_identifier = fig_identifier #utilize to save a number of different figures
        
        self.fig_name = ''
        

        ## build ideal art:
        noise = 0
        self.ideal_list_counts = self.run_ideal_model()
        self.ideal_bin_outcomes, self.ideal_count_outcomes = self.divide_outcomes(noise, self.ideal_list_counts) # outcomes of simulating the circuits
                        
        self.ideal_float_list = self.bin2float(self.ideal_bin_outcomes)
        self.ideal_hex_numbers = self.float2hexcode(self.ideal_float_list)
        self.ideal_color_list, self.ideal_bubble_area = self.bubble_info(noise, self.ideal_hex_numbers, self.ideal_count_outcomes)
        self.ideal_x, self.ideal_y = self.generate_coords(num_bubbles = len(self.ideal_color_list))
        bubble_area = self.ideal_bubble_area
        color_list = self.ideal_color_list
        x = self.ideal_x
        y = self.ideal_y
                

        self.artwork = self.build_art(noise, bubble_area, color_list, x, y)

    def noise_art(self, custom_noise_vals, fig_identifier):
        noise = 1
        self.p_meas, self.p_gate1 = self.set_noise(custom_noise_vals)
        self.noise_list_counts = self.run_noise_model()
        self.noise_bin_outcomes, self.noise_count_outcomes = self.divide_outcomes(noise, self.noise_list_counts) # outcomes of simulating the circuits                
                        
        self.noise_float_list = self.bin2float(self.noise_bin_outcomes)
        self.noise_hex_numbers = self.float2hexcode(self.noise_float_list)
        self.noise_color_list, self.noise_bubble_area = self.bubble_info(noise, self.noise_hex_numbers, self.noise_count_outcomes)
        self.noise_x, self.noise_y = self.generate_coords(num_bubbles = len(self.noise_color_list))
            
        bubble_area = self.noise_bubble_area 
        color_list = self.noise_color_list 
        x = self.noise_x 
        y = self.noise_y 
        
        
        self.fig_identifier = fig_identifier
        self.artwork = self.build_art(noise, bubble_area, color_list, x, y)
    
    def get_text(self, text):
        # Linguistic input from user, either passed through or taken during initialization

        if text == '':
            word = input("Please enter text : " )
        else:
            word = text

        valid_input = all(c in string.printable for c in word)

        if not valid_input:   
            raise Exception("Not a a valid input. Please use ASCII.")

        return word
    
    def print_text(self):
        print(self.text)
        
    def text2bits(self):
        # Change text to bit string
        bit_string = ''
        for char in self.text:
            bit_string += bin(ord(char))[2:].zfill(8)
        print("Number of bits is: ", len(bit_string))
        return bit_string
    
    def split_bits(self):
        # Split the bit string into groups of 5 (assuming the devices we use have only 5 qubits)
        bits_split = [self.bit_string[j:j+self.n] for j in range(0,self.bit_string_length,self.n)]
        return bits_split
    
    
    def build_circuits(self, bits_split):
        circuits = []

        for bits in bits_split:
            num_qubits = len(bits)
            qc = QuantumCircuit(self.n)

    
            for i, bit in enumerate(bits):
                if bit == '1':
                    qc.x(self.n-1-i)
        
            qc.measure_all()
            circuits.append(qc)
        print("Number of circuits is: ", len(circuits))
        return circuits
    
    def set_noise(self, custom_noise_vals):
        
        p_meas = custom_noise_vals[0]
        p_gate1 = custom_noise_vals[1]
        return p_meas, p_gate1
        
    def run_noise_model(self):
        # Runs more realistic scenario governed by a noise model
        #p_reset = self.p_reset
        p_meas = self.p_meas
        p_gate1 = self.p_gate1

        # QuantumError objects
        error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
        error_gate1 = depolarizing_error(p_gate1,1)
        


        # Add errors to noise model
        noise_bit_flip = NoiseModel()
        noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
        noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
            
        print(noise_bit_flip)
        list_counts = []
        for qc in self.circuits:
            # Create noisy simulator backend
            sim_noise = AerSimulator(noise_model=noise_bit_flip)

            # Transpile circuit for noisy basis gates
            circ_tnoise = transpile(qc, sim_noise)

            # Run and get counts
            result_bit_flip = sim_noise.run(circ_tnoise).result()
            counts_bit_flip = result_bit_flip.get_counts(0)
            list_counts.append(counts_bit_flip)

        return list_counts
    
    def run_ideal_model(self):
        # Runs ideal noiseless scenario on a simulator  
        sim = Aer.get_backend('qasm_simulator')
        shots = self.shots
        qobj = assemble(self.circuits, shots = shots)
        job = sim.run(qobj)
        list_counts = []
        for qc in self.circuits:
            counts = job.result().get_counts(qc)
            list_counts.append(counts)

        return list_counts
    
    
    def divide_outcomes(self, noise, list_counts):
        # Makes two lists out of count data:
        bin_outcomes = [] # binary outcomes of running the circuits that will later be turned into hex colors
        count_outcomes = [] # counts related to each of the binary outcomes, which will be used as bubble areas
        
        for lst in list_counts:
            bin_keys = lst.keys()
            vals = lst.values()
            for bin_num in bin_keys:
                bin_outcomes.append(bin_num)   
            for val in vals:
                count_outcomes.append(val)
        if not noise:
            self.ideal_bin_outcomes = bin_outcomes
            self.ideal_count_outcomes = count_outcomes
            
        return bin_outcomes, count_outcomes
    
    
    
    def bin2float(self, bin_outcomes):
        # Converts binary string to float to be later converted to a color hex code
        float_list = []
        for num in bin_outcomes:
            dec_num = int(num,2) #binary to decimal
            if dec_num > len(num): 
                float_list.append(len(num)/int(num,2))
            else: 
                float_list.append(int(num,2)/len(num))
        return float_list
    
                
        
    def float2hexcode(self, float_list):
        # create list of hex codes from list of floats
        hex_numbers = []
        for num in float_list:
            multiplier = 10000000
            hex_number = str(hex(int(num*multiplier)))
            hex_number ='#'+ hex_number[2:]
            if len(hex_number) == 6: # needs to be 7 in length with the #, but some come out 6 in length
                hex_numbers.append(hex_number+'0')
            else:
                hex_numbers.append(hex_number)
        return hex_numbers
    
    def eliminate_ideal(self): #eliminates the ideal bin_outcomes & ideal count_outcomes from the noise outcomes
        for bin_val in self.ideal_bin_outcomes:
            ind = self.bin_outcomes.index(bin_val)
            self.noisy_ideal_count_outcomes.append(self.count_outcomes[ind])
            self.bin_outcomes.pop(ind)
            self.count_outcomes.pop(ind)
            
        
    def bubble_info(self, noise, hex_numbers, count_outcomes):
        # Creates a color list and corresponding bubble area (ie size) list
        color_list = []
        bubble_area = []

        for i in range(len(hex_numbers)):
            hex_num = hex_numbers[i]  #must check that hex num is 6 digits, ie 7 in length including #
            if len(hex_num) == 7:
                color_list.append(hex_num)
                bubble_area.append(count_outcomes[i])
        print("Number of colors is: ", len(color_list))
        
        return color_list, bubble_area
    
    def generate_coords(self, num_bubbles): #generate coordinates
        x = np.zeros(num_bubbles)
        y = np.zeros(num_bubbles)
        for i in range(num_bubbles): #random coordinates
            x[i] = np.random.rand()
            y[i] = np.random.rand()
        return list(x), list(y)
    
    
    def build_art(self, noise, bubble_area, color_list, x, y):
        # A4 size proportions
        xpixels = math.floor(self.dpi * 14032/1200) #canvas_width default is dpi 1200, width 14032
        ypixels = math.floor(self.dpi * 9922/1200) #canvas_height default is dpi 1200, height 9922

        # get the size in inches
        xinch = xpixels /self.dpi 
        yinch = ypixels /self.dpi 

        # plot and save in the same size as the original
        fig = plt.figure(figsize=(xinch,yinch))

        ax = fig.add_subplot(111)
        ax.scatter(x, y, s=bubble_area, c = color_list, alpha=0.4) #alpha is transparency
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.axis('off')

        
        buffer_image = io.BytesIO()
        self.buffer_image = buffer_image
        
        fig.savefig(buffer_image, format ="png")
        buffer_image.seek(0)
         
        return fig
    
    
    def get_buffer_image(self): #return the name of the figure
        return self.buffer_image