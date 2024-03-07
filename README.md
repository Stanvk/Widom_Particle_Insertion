# Widom: A Python Package for Test-Particle Insertion
This Python project provides a means of running parallelized Widom's Test Particle Insertion Method [1] on all sorts of configurations drawn from
molecular-dynamics or monte-carlo simulations. This package relies partly on MDAnalysis such that a large array of trajectory files are supported, such as GROMACS's .trr file and LAMPS's .data file.

**If you use this softwork in your work, please cite it as**

"_van Kraaij, S.A.T. (2024). Widom: A Python Package for Test-Particle Insertion (Version 1.1.0) [Computer software]. https://github.com/stanvk/widom_"

## Requirements
The MDAnalysis package (https://www.mdanalysis.org/) is needed, which can be installed via
```
pip install MDAnalysis
```

MDAnalysis will include Numpy, which is also required when using Widom.

## Usage

First of all, the ```MDAnalysis``` package is required to load the configuration files. Apart from MDAnalysis, we also include ```Widom.Widom``` and the test-particle, which will be oxygen; ```Widom.Dioxygen```.

```python
import MDAnalysis as md
from Widom.Widom import Widom
from Widom.Dioxygen import Dioxygen
```
After importing the required packages a ```MDAnalysis.Universe``` object needs to be initiated:

```python
sample = md.Universe(path_to_topology_file, path_to_coordinate_file)
```
The ```path_to_topology_file``` and ```path_to_coordinate_file``` variables respectively contain the path to the topology and coordinate file. Let's assume that we load a polyethylene (PE) configuration consisting of CH2 and CH3 united atoms.
Next, the Widom class can be initiated. The Widom constructor requires the test-particle class and the number of processes that will be used. The number of processes can in-fact be higher than the number of available CPU's.

```python
tpi = Widom(Dioxygen(), processes=8)
```
The ```sample``` needs to be passed to the ```Widom``` instance. The second argument in the ```Widom.set_sample()``` method requires the Lennard-Jones parameters of the atoms in the sample.
```python
tpi.set_sample(sample, {'CH2': [epsilon_CH2, sigma_CH2],'CH3': [epsilon_CH3, sigma_CH3]})
```
Before running the test-particle insertion (TPI) the number of insertions needs to be defined and the frame in the trajectory file on which the TPI measurement will be run.
```python
tpi.prepare(frame=0, number_of_insertions=1000000)
```
Lastly, the TPI measurement can be run by ```Widom.run()```. The insertion locations can be saved by ```Widom.save_insertion_locations()``` and the insertion energy difference by ```Widom.save_insertion_energies()```.
```python
if __name__ == '__main__':
    tpi.run()

    tpi.save_insertion_energies(output_path, 'energies.txt')
    tpi.save_insertion_locations(output_path, 'locations.txt')

```
Here, ```output_path``` contains the output path of the energies and locations files.

## References
[1] Widom, B. (1963). Some topics in the theory of fluids. The Journal of Chemical Physics, 39(11), 2808-2812.
