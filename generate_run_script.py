from Helpers.Container import Container
import sys

run_scripts_path = '/home/phys/20172002/NTUA/run_tpi_semicrystalline_298K'
basepath = '/Users/stanvk/Projects/NTUA/systems/pe_configurations_298K/'
relative_outputpath = 'Analysis/Widom/'

config = Container(basepath, relative_outputpath).load(filename=sys.argv[1])

title = sys.argv[2]

f = open(run_scripts_path+str(title)+'.run', 'w+')
f.write("#!/usr/bin/bash \n")
f.write("#SBATCH --nodes=1 \n")
f.write("#SBATCH --ntasks=64 \n")
f.write("#SBATCH --partition=phys.default.q \n")
f.write("#SBATCH --output="+str(title)+".out \n")
f.write("#SBATCH --time=4:00:00 \n")
f.write('#SBATCH --constraint="amd&rome" \n')
f.write("#SBATCH --mail-type=all \n")
f.write("#SBATCH --mail-user=s.a.t.v.kraaij@student.tue.nl \n")
f.write("source ~/venv/fic/bin/activate \n")
f.write(" \n")
f.write("python3 ../TPI/run_dioxygen_tpi.py /home/phys/20172002/NTUA/systems/amorphous_pe/ Analysis/Widom/ config_15_02_2024_110536 64 \n")