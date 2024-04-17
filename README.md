## Necessary Libraries  
pip install PyQt5  
pip install pwntools  
pip install ansi2html  
  
## Necessary Files  
logo.png (provided)  
  
## Test Files  
chal1.bin (provided)    
chal2.bin (provided)  
  
## Installation  
$ git clone https://github.com/tylerdionne/pwndbgGUI.git  
$ cd pwndbgGUI  

## To start  
$ python3 main.py  

## Usage  
  
“Enter binary name”   
The filename of the binary to be debugged.   

“Enter function name” 
The function name in the binary to either set a breakpoint at or disassemble.

“Enter payload” 
User input that can be sent to the program.

“Enter payload” 
User input that can be sent to the program.

“Start pwndbg”
Initializes pwndbg with the provided binary filename.
$ pwndbg ./{filename}

“Set breakpoint”
Sets a breakpoint at the provided function name.
pwndbg> break {functionname}

“Disassemble
Disassembles the provided function name.
pwndbg> disassemble {functionname}

“Run”
Runs the provided binary file.
pwndbg> r 

“Continue”
Returns to normal execution and is used to navigate breakpoints in the binary.
pwndbg> c

“Send Payload”
Sends the provided user input to the program.



