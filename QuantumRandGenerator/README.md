# Quantum Random Number Generator
Randomness exists in the heart of quantum mechanics. Quantum computation, which seeks to take advantage of the fundamental laws of quantum physics,
can provide us with a true random number generator circuit which can give us a random number at will.

# Installation
Before running the simulator, run the following command to install dependencies first: <br>
`pip install -r requirements.txt`

# Usage
`python main.py -lo LOWER_BOUND -hi HIGHER_BOUND` <br>
Random number generator will return a random number in the range: `LOWER_BOUND <= x <= HIGHER_BOUND`
