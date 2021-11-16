# The Quantum Art Generator
Bubble art as a creative visualization of quantum noise

<img src="https://github.com/quantum-kittens/quantum-art-generator/blob/master/static/app_banner.jpg" width="100%"  />

## Overview
This app generates bubble art based on a textual input that is a visual representation of quantum noise.

##  How to Use The Quantum Art Generator

An online version is provided at [qartgen.herokuapp.com](https://qartgen.herokuapp.com/). 

### Navigating The Quantum Art Generator
There are two ways art can be generated:
- 'Preset Noise' generates a slideshow of artworks with strategically preset levels of noise so that you can observe the journey as noise levels increase.
- 'Custom Noise' generates a single piece of artwork from your own specified noise levels - this is where you can play with the probabilities associated with the two types of errors! Remember that probabilities need to be specified between 0.0 and 1.0.

Here's something for you to try: in the Custom Noise mode, set both P(meas) and P(gate) to 0.5 and see what you get! Think about why the resulting artwork looks the way it does.

### How to Run The Quantum Writing Prompt Generator Locally

If you want to run it on a actual quantum device, or just have a local copy of this follow the following step:

1. Clone the git repository from [Github](https://github.com/quantum-kittens/quantum-prompt-generator).
2. `cd` into the git repository.
3. Execute `pip install -r requirements.txt`.
4. Execute `export FLASK_APP=app.py`
5. Execute `flask run`

The app will available at `127.0.0.1:5000/`. You can direct your browser to that location to access it. 

##  How The Quantum Art Generator Works

If you're interested in how the art generation works, and what P(meas) and P(gate) mean, take a look at the corresponding article [How I Use Quantum Computing to Create Bubble Art](https://github.com/quantum-kittens/quantum-art-generator)



## Resources

#### Quantum Error Correction and Noise
- [Qiskit Documentation: Building Noise Models](https://qiskit.org/documentation/tutorials/simulators/3_building_noise_models.html)
- [Make use of noisy hardware: Building a noisy quantum random number generator](https://fullstackquantumcomputation.tech/blog/post-quantum-ugly-duckling/)
- [Here’s How to Test Error Correction on an IBM Quantum Computer](https://medium.com/qiskit/heres-how-to-test-error-correction-on-an-ibm-quantum-computer-ecb086606e7)
- [Loading a game from a quantum computer](https://www.youtube.com/watch?v=R_8Tq3MehL8&ab_channel=JamesWootton)
- [Benchmarking near-term devices with quantum error correction](https://iopscience.iop.org/article/10.1088/2058-9565/aba038)
- [Introduction to Quantum Error Correction](https://arxiv.org/pdf/quant-ph/0207170.pdf)

#### Generic Quantum Resources: 
- [Qiskit Textbook](https://qiskit.org/textbook/content/ch-ex/)
- [The Quantum Catalog](http://quantumcatalog.com/)

## Credits
#### Created by:
- Radha Pyari Sandhir (Github: [quantum-kittens](https://github.com/quantum-kittens), Twitter: [RadhaPyari](https://twitter.com/RadhaPyari))
- James Wootton (Github: [quantumjim](https://github.com/quantumjim), Twitter: [decodoku](https://twitter.com/decodoku))

#### Thanks to:
- [Soham Pal](https://twitter.com/dragonbornmonk) for initial concept discussions
- [Burak Şenol](https://buraksenol.medium.com/) for valuable input on the handling images in the cloud

#### Art:
- Cover photo by [Julian Hochgesang on Unsplash](https://unsplash.com/@julianhochgesang).
- Loading icon by [Poonam on smallenvelop](https://smallenvelop.com/display-loading-icon-page-loads-completely/)
- Python bubble art by [codesharedot on dev.to](https://dev.to/codesharedot/computer-generated-art-with-python-3ala)


