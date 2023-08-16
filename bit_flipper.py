"""
Nick Belsten
Flips bits in files
Created for SpaceGPT Project
"""
from numpy import random
import argparse

#Todo: refine these and add citations
#Typical flips per year
JUPITER_RATE = 1e-5
LEO_RATE = 1e-7

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as binary_file:
            binary_data = binary_file.read()
            return binary_data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def write_binary_file(file_path, binary_data):
    try:
        with open(file_path, 'wb') as binary_file:
            binary_file.write(binary_data)
            print(f"Binary data written to '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
def duplicate_file(input_path, output_path):
    try:
        with open(input_path, 'rb') as input_file:
            with open(output_path, 'wb') as output_file:
                byte = input_file.read(1)
                while byte:
                    output_file.write(byte)
                    byte = input_file.read(1)
                print(f"Binary file duplicated from '{input_path}' to '{output_path}'.")
    except FileNotFoundError:
        print(f"Input file '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
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
                    if random.random()<flip_chance:
                        byte=flip_random_bit(byte)
                    output_file.write(byte)
                    byte = input_file.read(1)
                print(f"Binary file from '{input_path}' mutated and written to '{output_path}'.")
    except FileNotFoundError:
        print(f"Input file '{input_path}' not found.")
        
        
def cmd_interface_func(input_file,output_file,flip_p, location, years):
    if location=="JUPITER":
        flip_p = JUPITER_RATE * years
    elif location=="LEO":
        flip_p = LEO_RATE * years
        
    bit_flip_duplicate(input_file,output_file,flip_p)

def main():
    parser = argparse.ArgumentParser(description="Bit flipper")
    
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    
    parser.add_argument("--flip_probability", type=float, default=0.5, help="Probability of flipping")
    
    location_group = parser.add_argument_group(title="Location Options")
    location_group.add_argument("--location", choices=["LEO", "JUPITER"], help="Location option")
    location_group.add_argument("--years", type=float, help="Number of years")

    args = parser.parse_args()

    if args.location and args.years is None:
        parser.error("When specifying a location, you must also provide the number of years in orbit")
    
    cmd_interface_func(args.input_file, args.output_file, args.flip_probability, args.location, args.years)

if __name__ == "__main__":
    main()



#Example
#python3 bit_flipper.py simple_test.txt output.txt --location JUPITER --years 10000