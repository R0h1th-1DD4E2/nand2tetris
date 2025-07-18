#!/usr/bin/env python3
"""
Hack Assembler for nand2tetris
Converts Hack assembly (.asm) files to machine code (.hack)
"""

import sys
import os
import re

class HackAssembler:
    def __init__(self):
        # Predefined symbols
        self.symbol_table = {
            'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5,
            'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
            'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
            'SCREEN': 16384, 'KBD': 24576
        }
        
        # Computation codes
        self.comp_codes = {
            '0': '0101010', '1': '0111111', '-1': '0111010',
            'D': '0001100', 'A': '0110000', '!D': '0001101',
            '!A': '0110001', '-D': '0001111', '-A': '0110011',
            'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
            'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
            'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
            'M': '1110000', '!M': '1110001', '-M': '1110011',
            'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
            'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
            'D|M': '1010101'
        }
        
        # Destination codes
        self.dest_codes = {
            '': '000', 'M': '001', 'D': '010', 'MD': '011',
            'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
        }
        
        # Jump codes
        self.jump_codes = {
            '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
            'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
        }
        
        self.next_var_address = 16
    
    def clean_line(self, line):
        """Remove comments and whitespace from a line"""
        # Remove comments
        comment_pos = line.find('//')
        if comment_pos != -1:
            line = line[:comment_pos]
        
        # Remove whitespace
        return line.strip()
    
    def is_a_instruction(self, line):
        """Check if line is an A-instruction"""
        return line.startswith('@')
    
    def is_c_instruction(self, line):
        """Check if line is a C-instruction"""
        return not line.startswith('@') and not line.startswith('(')
    
    def is_label(self, line):
        """Check if line is a label declaration"""
        return line.startswith('(') and line.endswith(')')
    
    def parse_a_instruction(self, line):
        """Parse A-instruction and return binary code"""
        symbol = line[1:]  # Remove @
        
        # Check if it's a number
        if symbol.isdigit():
            value = int(symbol)
        else:
            # It's a symbol
            if symbol not in self.symbol_table:
                # New variable, assign next available address
                self.symbol_table[symbol] = self.next_var_address
                self.next_var_address += 1
            value = self.symbol_table[symbol]
        
        # Convert to 16-bit binary
        return format(value, '016b')
    
    def parse_c_instruction(self, line):
        """Parse C-instruction and return binary code"""
        dest = ''
        comp = ''
        jump = ''
        
        # Check for jump
        if ';' in line:
            parts = line.split(';')
            line = parts[0]
            jump = parts[1]
        
        # Check for destination
        if '=' in line:
            parts = line.split('=')
            dest = parts[0]
            comp = parts[1]
        else:
            comp = line
        
        # Build binary instruction: 111accccccdddjjj
        try:
            comp_bits = self.comp_codes[comp]
            dest_bits = self.dest_codes[dest]
            jump_bits = self.jump_codes[jump]
            
            return '111' + comp_bits + dest_bits + jump_bits
        except KeyError as e:
            raise ValueError(f"Invalid instruction component: {e}")
    
    def first_pass(self, lines):
        """First pass: collect labels and their addresses"""
        rom_address = 0
        
        for line in lines:
            cleaned = self.clean_line(line)
            
            if not cleaned:  # Empty line
                continue
                
            if self.is_label(cleaned):
                # Extract label name (remove parentheses)
                label = cleaned[1:-1]
                self.symbol_table[label] = rom_address
            else:
                # It's an instruction, increment ROM address
                rom_address += 1
    
    def second_pass(self, lines):
        """Second pass: translate instructions to machine code"""
        machine_code = []
        
        for line in lines:
            cleaned = self.clean_line(line)
            
            if not cleaned or self.is_label(cleaned):
                continue
                
            if self.is_a_instruction(cleaned):
                machine_code.append(self.parse_a_instruction(cleaned))
            elif self.is_c_instruction(cleaned):
                machine_code.append(self.parse_c_instruction(cleaned))
        
        return machine_code
    
    def assemble(self, input_file, output_file=None):
        """Main assembly function"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = base_name + '.hack'
        
        # Read input file
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        # Two-pass assembly
        self.first_pass(lines)
        machine_code = self.second_pass(lines)
        
        # Write output file
        with open(output_file, 'w') as f:
            for instruction in machine_code:
                f.write(instruction + '\n')
        
        print(f"Assembly complete: {input_file} -> {output_file}")
        print(f"Generated {len(machine_code)} instructions")
        
        return machine_code

def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <input.asm> [output.hack]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        assembler = HackAssembler()
        assembler.assemble(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
