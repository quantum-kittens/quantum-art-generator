# The D&D μStarter Kit
powered by quantum computing and ad-libs

<img src="https://www.radhapyarisandhir.com/wp-content/uploads/2020/10/dnd_cover-scaled.jpg" width="80%"  />

## Overview
This is a helper tool for players of Dungeons and Dragons. Roll dice, generate a character with an ad-libbed one-line backstory, or play a complete ad-libbed D&D scene! The D&D μStarter Kit makes use of quantum computing for randomness and ad-libs, alongside user inputs. This generator is based on the D&D 5E Player’s Handbook.

## Functionalities

- A character generator that provides a race, class, name, and a one-line ad-libbed backstory  
- A dice roller to determine ability scores or to use during gameplay
- An ad-libbed D&D scene 


##  How to Use The D&D μStarter Kit

An online version is provided at [qdnd](https://qdnd.herokuapps.com). This version runs only on the QASM simulator so that the server is not overloaded.

### How to Run The D&D μStarter Kit Locally

If you want to run it on a actual quantum device, or just have a local copy of this follow the following step:

1. Clone the git repository from [Github](https://github.com/quantum-kittens/dnd-mustarter-kit).
2. `cd` into the git repository.
3. Execute `pip install -r requirements.txt`.
4. Execute `export FLASK_APP=app.py`
5. Execute `flask run`

The app will available at `127.0.0.1:5000/`. You can direct your browser to that location to access it. To run this on an actual quantum device, open `app.py` and edit it as mentioned in the comments in the file, before executing `flask run`.

### Navigating The D&D μStarter Kit

<img src="https://www.radhapyarisandhir.com/wp-content/uploads/2020/10/home.png" width="80%"  />

Click on ‘Dice Roller’ to use the dice. You will be taken to a screen that allows you to select the type of dice, number of dice, and modifier. Click ‘Roll’ to get your result.

<img src="https://www.radhapyarisandhir.com/wp-content/uploads/2020/10/dice_roller.png" width="80%"  />

Click on ‘Character Generator’ to generate a character. An ad-lib prompt will appear. Enter a word according to the prompt and then click ‘Submit’. You will be provided with a name, race, class, and one-line back story.  User selected words are highlighted in orange, and quantum computer selected words are highlighted in blue.

<img src="https://www.radhapyarisandhir.com/wp-content/uploads/2020/10/char_gen.png" width="80%"  />

Click on ‘D&D Scene’ to play an ad-libbed scene. You will be provided with a number of ad-libbed prompts. Enter words according to the prompts and then click ‘Submit’. Your customized scene will appear! User selected words are highlighted in orange, and quantum computer selected words are highlighted in blue.

<img src="https://www.radhapyarisandhir.com/wp-content/uploads/2020/10/dnd_scene.png" width="80%"  />

##  How The D&D μStarter Kit Works
### Quantum Computing
Quantum computing is used anywhere randomness is required. For instance, the dice are rolled assigning equal probabilities to all of the possible numbers by generating quantum circuits with an appropriate number of qubits in superposition via Hadamard gates.

A similar method is applied during the random selection of letters for the name generator, the backstory from the story bank, and the words selected for the quantum computers contribution to the ad-libbed parts.

For instance, if a choice needs to be made from among eight word options, then a circuit of three qubits is prepared. A Hadamard is applied on each qubit, placing them in a superposition of all eight possible states from |000⟩ to |001⟩ and so on to |111⟩. Upon measurement, one of the eight states is obtained, which corresponds to one of the eight word options.

All circuits are simulated with the QASM simulator from IBM’s open source SDK, Qiskit. However if you would rather user IBM's quantum devices then you can do so, as discussed earlier.

### Race Selection
A race is randomly selected through quantum computing. The race options per the D&D 5E Player’s Handbook are: Dragonborn, Hill Dwarf, Mountain Dwarf, Dark Elf, High Elf, Wood Elf, Deep Gnome, Forest Gnome, Rock Gnome, Half-Elf, Lightfoot Halfling, Stout Halfling, Half-Orc, Variant Human, Human, Tiefling.

### Class Selection
Once a race is selected, a class is randomly selected. However, all classes are not given equal probabilities of being selected, as certain races are more synergetic with certain classes.

<img src="https://www.radhapyarisandhir.com/wp-content/uploads/2020/10/synergy-table.png" width="80%"  />

We make use of this synergy table by Taron Pounds as a basis for a simple probability mapping that applies rotations in the quantum circuit such that the probability of a class that is more synergetic with a race is larger than that of a class that is less synergetic with a certain race.

The SPSA optimizer from Qiskit Aqua aides in the selection of the final class. However, the probabilities have been initialized such that there is a non-zero (though very small) chance of a less synergetic class being chosen. We don’t want to eliminate class possibilities altogether! For the online version we have pre-computed the optimal parameters using SPSA, so as to not load the server.

The class options per the D&D 5E Player’s Handbook are: barbarian, bard, cleric, druid, fighter (dex), fighter (str), fighter (eldritch knight), monk, paladin, ranger (dex), ranger (str), rogue, rogue (arcane trickster), sorcerer, warlock, and wizard.

### Name Generation
Names are generated in four stages of randomness:

- The number of syllables, 1 to 4 is randomly selected
- The letter type for a single syllable is randomly selected (consonant or vowel)
- The number of letters for single type is randomly selected (1 or 2)
- The letters are randomly selected.

Letters have equal probability of being chosen. However, if two consonants are selected to appear one after the other, how synergetic they are together is taken into account.

For instance, if the letter type is ‘consonant’, and the number of letters is 2, then “Sb” would not work, but “St” would.

The names follow the pattern consonant (c) -> vowel (v) -> c -> v -> c (or vice versa). Each stage adds either 1 or 2 letters--this is also randomly chosen.


### Rolling Dice
There are 6 dice available: d4, d6, d8, d10, d12, d20. For dN, a number between 1 and N is randomly selected through a measurement on a quantum circuit as described above. The number of qubits selected is such that the number of possible states is greater than or equal to N, since for n qubits there are 2<sup>n</sup> possible states. If the number of states is larger, the rice keeps ‘rolling’ until a number less than N+1 is obtained. In this way all numbers are still equally likely to be picked.

Example: for d10 the number of qubits is 4. There are 2<sup>4</sup>, that is, 16 possible states. However, since we only need 10, the dice is rolled until the outcome is between 1 and 10.

If you want to roll a d100, we recommend you roll two d10’s, one for the tens digit and one for the ones digit. For instance, if you obtain 9 and 6 from two d10 rolls, then your outcome is 96, and if you get 10 and 10 on both the rolls, then your outcome is 100.

### Ad-libs

The ad-libbed aspect of the backstories and the D&D scene is a joint effort by the user and the quantum computer. The improvised words are generated both by user inputs as well as randomly selected by a quantum computer from word banks. User selected words are highlighted in orange, and quantum computer selected words are highlighted in blue.

## Credits
#### Created by:
- Radha Pyari Sandhir (Github: [quantum-kittens](https://github.com/quantum-kittens), Twitter: [RadhaPyari](https://twitter.com/RadhaPyari))
- Soham Pal (Github: [e-eight](https://github.com/e-eight), Twitter: [dragonbornmonk](https://twitter.com/dragonbornmonk))

#### Special thanks to:

- Emily (creator of [fantasynamegenerators.com](https://www.fantasynamegenerators.com/))
- Protim Bhaumik (professional DM)

for insightful comments, remarks and advice.

#### D&D Resource Links:

- [D&D Beyond](https://www.dndbeyond.com) 
- [D&D Wiki](https://www.dandwiki.com/)
- [Synergy Table by Taron Pounds](https://www.reddit.com/r/DnD/comments/8788on/5e_race_class_synergy_analysis_v5/)

#### Other Resources: 
- [The Quantum Catalog](http://quantumcatalog.com/)
- [Qiskit](https://qiskit.org/)


Cover photo by [Clint Bustrillos on Unsplash](https://unsplash.com/@clintbustrillos).

