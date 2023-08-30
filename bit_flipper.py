"""
Nick Belsten
Flips bits in files
Created for SpaceGPT Project
"""
from numpy import random
import argparse

#Todo: refine these and add citations
#Typical flips per year
#Add Mars
# Add Asteroid
#Add Venus
#Jupiter

#Per bit cross section
HIGH_CROSS_SECTION = 1e-10 #https://ieeexplore-ieee-org.libproxy.mit.edu/stamp/stamp.jsp?tp=&arnumber=8540420
MEDIUM_CROSS_SECTION = 1e-12 #https://doi.org/10.1016/j.nima.2020.164064
LOW_CROSS_SECTION = 1e-15 #Same as medium

#Now lets use 10 MeV for integral flux. Protons below about this energy will be stopped by a few mm of aluminum
#https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=2934&context=smallsat

#LEO_RATE = 1e-7 #10.1109/REDW51883.2020.9325842 for a few typical microprocessors

#Fluxes in cm^-2 s^-1
LEO_FLUX = 10 #https://www.researchgate.net/publication/334075796_Impact_of_proton-induced_transmutation_doping_in_semiconductors_for_space_applications#fullTextFileContent
VAN_ALLEN_FLUX = 10**5 #https://www.researchgate.net/publication/324210214_Comparative_Analysis_of_Sub_GTO_GTO_and_Super_GTO_in_Orbit_Raising_for_All_Electric_Satellites#fullTextFileContent
MARS_FLUX = 0.1 #https://www.frontiersin.org/articles/10.3389/fspas.2022.833144/full
EUROPA_FLUX = 10**5 #https://www.researchgate.net/publication/268556022_Launch_Period_Development_for_the_Juno_Mission_to_Jupiter
JUPTER_RADIATION_BELT_FLUX = 10**7 #same as above

SECONDS_IN_YEAR = 60*60*24*365       
        
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def flip_random_bit(byte):
    bit_position = random.randint(0, 7)  # Randomly select a bit position to flip
    mask = (1 << bit_position)       # Create a mask with the selected bit set
    mask = mask.to_bytes(1,'big')
    flipped_byte = byte_xor(byte,mask)          # XOR operation to flip the selected bit
    return flipped_byte

        
def bit_flip_duplicate(input_path, output_path, flip_chance):
    try:
        with open(input_path, 'rb') as input_file:
            with open(output_path, 'wb') as output_file:
                byte = input_file.read(1)
                while byte:
                    if random.random()<(flip_chance*8): #Note we are assuming no more than one bit error per byte. Reasonable for low rates
                        byte=flip_random_bit(byte)
                    output_file.write(byte)
                    byte = input_file.read(1)
                print(f"Binary file from '{input_path}' mutated and written to '{output_path}'.")
    except FileNotFoundError:
        print(f"Input file '{input_path}' not found.")
        
        
def cmd_interface_func(input_file, output_file, flip_probability, flux, cross_section, years):
    if not flip_probability:
        if flux:
            if flux == "JUPITER_BELT":
                flux_value = JUPITER_RADIATION_BELT_FLUX
            elif flux == "LEO":
                flux_value = LEO_FLUX
            elif flux == "VAN_ALLEN":
                flux_value = VAN_ALLEN_FLUX
            elif flux == "MARS":
                flux_value = MARS_FLUX
            elif flux == "EUROPA":
                flux_value = EUROPA_FLUX
            else:
                raise ValueError("Invalid flux option.")
        
        if cross_section:
            if cross_section == "HIGH":
                cross_section_value = HIGH_CROSS_SECTION
            elif cross_section == "MEDIUM":
                cross_section_value = MEDIUM_CROSS_SECTION
            elif cross_section == "LOW":
                cross_section_value = LOW_CROSS_SECTION
            else:
                raise ValueError("Invalid cross section option.")
        
        flip_probability = flux_value * cross_section_value * years * SECONDS_IN_YEAR
    print("Using flip probability ", flip_probability)

    bit_flip_duplicate(input_file, output_file, flip_probability)


def main():
    parser = argparse.ArgumentParser(description="Bit flipper")
    
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    
    parser.add_argument("--flip_probability", type=float, help="Probability of flipping")
    
    flux_choices = ["LEO", "VAN_ALLEN", "MARS", "EUROPA", "JUPITER_BELT"]
    parser.add_argument("--flux", choices=flux_choices, help="Predefined flux")
    
    cross_section_choices = ["HIGH", "MEDIUM", "LOW"]
    parser.add_argument("--cross_section", choices=cross_section_choices, help="Predefined cross section")
    
    parser.add_argument("--years", type=float, help="Number of years in orbit")
    
    args = parser.parse_args()

    if not args.flip_probability and (not args.flux or not args.cross_section or args.years is None):
        parser.error("You must either provide a flip probability or both a flux, a cross section, and a number of years.")
    
    if args.flip_probability and (args.flux or args.cross_section):
        parser.error("You cannot provide both a flip probability and specify flux/cross section options.")
    
    if args.flux and args.flux not in flux_choices:
        parser.error("Invalid flux option. Choose from LEO, VAN_ALLEN, MARS, EUROPA, JUPITER_BELT.")
    
    if args.cross_section and args.cross_section not in cross_section_choices:
        parser.error("Invalid cross section option. Choose from HIGH, MEDIUM, LOW.")
    
    cmd_interface_func(args.input_file, args.output_file, args.flip_probability, args.flux, args.cross_section, args.years)


if __name__ == "__main__":
    main()


#Example
#python3 bit_flipper.py simple_test.txt output.txt --flux LEO --cross_section MEDIUM --years 100

#python3 bit_flipper.py simple_test.txt output.txt --flip_probability 0.1
