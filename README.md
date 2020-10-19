# galaxy.py
A simple tidal interaction code in Python (for educational use)

This is a Python implementation of a simple galaxy interaction code,
based on the original paper by Toomre & Toomre (1972). It runs a
simple N-body integration of interacting galaxies, which is then
plotted on-the-fly using matplotlib's animation functionality.

A code with similar functionality is provided in the Appendix to Carroll & Ostlie, Introduction to Modern Astrophysics, but as a 32-bit Windows binary executable.
The present code is designed to replace this, with the code in a language that modern Astronomy students are familiar with.

## Example
![galaxies](https://user-images.githubusercontent.com/12252103/96248767-ccaa8c80-0ff7-11eb-85f1-94e5b751b8f3.gif)

## Running the code
```
python3 galaxy.py
```

### Requirements
A standard Python 3 installation that includes numpy and matplotlib. The code can be run in any Python environment.

### Changing parameters
The code is short enough that students should be able to comprehend most of the source code, and hence delve into it. 
The relevant runtime parameters are given in the first few lines of the file.

In the current version the idea is to edit the first few lines of the script and re-run it to produce different simulations.
