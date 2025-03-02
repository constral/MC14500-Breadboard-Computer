# MC14500 Minimal ICU Unit

<image src="picture.jpg" width="800px"/>

This project involved the physical implementation of the "Minimal ICU Unit" system described in the Motorola MC14500 logic processor handbook, using modern hardware equivalents on breadboards. This involved dealing with several digital system components, including a clock system, program memory, and I/O interfacing. The hands-on implementation gave me a deeper understanding of how digital systems as well as their components operate.

## Overview
On the software side, programming can be done manually via DIP switches and assembly code added inside the program memory, but it can also be performed via electrical signals sent from an Arduino development board. Eventually, several software implements were created to aid with programming the computer, such as the C++ assembler for writing binary code to the memory of the computer, as well as a Python script that compiles the code to be forwarded to the assembler. Seeing as the MC14500 only contains a logic unit, it is only possible for it to perform arithmetic operations via emulating the logic gates of an arithmetic unit by code; I also explored this aspect of the machine, by implementing algorithms that used logic functions to perform addition and multiplication.

## Block Diagram
The system is split into several key sections:

- Clock System: Provides manual or automatic pulses to drive the system.
- Controls: Buttons for halting, resuming, and resetting the system.
- Program Counter & Memory: Tracks program execution and stores instructions.
- Processor: The MC14500 itself, with custom handling for unreliable I/O behavior.
- Input/Output: Handles interaction with external data via DIP switches and LEDs.
- Scratch Register: Temporary storage for intermediate computation results.

<image src="original_schematic.jpg" width="600px"/>



## System Details
1. Clock
The clock provides two modes: manual i.e. one pulse per button press, or automatic pulses from the 555 timer circuit.
The clock frequency can be adjusted using a potentiometer. The 555 is used both as a debounce circuit (manual mode) and an oscillator (automatic mode).

2. Controls
Three primary control buttons:

- HALT: Stops execution.
- RESUME: Resumes execution.
- RESET: Resets the program counter and registers.
The halting system works by using an S-R flip-flop which stores the value of whether the system is halted or not.

3. Program Counter & Memory
Program Counter
* Built from two 74HC163 4-bit counters to form an 8-bit counter.
* Increments every clock pulse, allowing access to up to 256 instructions.

Memory
* AS6C62256 SRAM. The data bus holds 8-bit instructions split into:
	- 4-bit opcode (the actual instruction).
	- 1-bit chip select (choosing between I/O and scratch).
	- 3-bit address for the value (selecting an I/O port).
* Memory must be reprogrammed after power loss.
* Only 256 addresses are actively used, but the chip can hold much more (64Kb).
* The address line on pin 4 was damaged by ESD and was replaced by remapping to pin 12 which would've otherwise been left unused (more memory than the PC can count).

Programming
* Programs can be entered manually via DIP switches or automatically using an Arduino-based programmer.
* A custom Python assembler (see repository) can be run on a computer to convert human-readable assembly-like code into binary instructions. These can then be sent to an Arduino for programming the device automatically.

4. Processor
The MC14500
* Executes 1-bit logical instructions.
* Takes 4-bit opcode and 1-bit data input.
* Outputs to a single Result Register LED.

Data Signal Fix
* The MC14500's data pin requires more current than the input logic chips can provide.
* A 2N2222 transistor amplifier boosts the signal.

Control Signals
* External clock fed into the processor.
* Four flag outputs for program flow (e.g., HALT triggered by instruction 1111).
* Write signal activates data output when writing to memory.

5. Input/Output Registers
Input
* Managed by a 74HC4051 multiplexer.
* Selects one of 8 input sources (7 DIP switches + 1 Result Register feedback).
* Data passed to MC14500 via the transistor amplifier.

Output
* Managed by a 74HC259 addressable latch.
* Stores 1-bit results into 8 possible output addresses.
* Write operations are controlled by:
	- The write pin (active during store instructions).
	- The chip select pin, determining if we write to I/O or the scratch register.
	- Due to unreliable MC14500 output behavior, a custom XOR gate (diode-transistor logic) was added to conditionally invert the result during store complement instructions.

Scratch Register
* A combination of input and output registers. Can be used much like a RAM.



## Programming Model
Despite the fact that the processor only has a logic unit, its logic functions can be used to implement binary addition with carry-ins and carry-outs, and binary multiplication with left-shifts and right-shifts. This is however an arduous process, which I have simplified by writing a Python assembler in which I could just write code as normal. It outputs C++ code that can then be uploaded on an Arduino, which can write directly to the program memory of the breadboard computer.

Programs (see repository):
1. An addition/incrementation program, which is inspired by but not directly copied from the one in the mc14500 handbook. Overall, the algorithm works like this: It parses through 6 digits of the input I/O as well as 6 digits of the scratch register, and adds each digit together. Because of the manipulation of variables that has to be done in order to perform computations, two bits in the scratch register are set aside in order to store the result of the summation and the carry. After the summation of the 6-th digits, however, if there is a carry-out resulting from it, this is counted as the 7-th digit of the result, and thus our algorithm is a 6-digit + 6-digit = 7-digit summation.
2. A binary multiplication program, in which I simulated left-shift and right-shift operations performed on two numbers which are written to the input. The algorithm has some caveats: along the entire process, we'll need to know the multiplicand A's digits, the multiplier B's digits, as well as keep track of what is being added to inside an acumulator, implemented in the scratch register. Also, being based on binary addition, it means that the largest number one can obtain is a 7-digit one. Luckily, the values for a 3-digit x 4-digit = 7-digit multiplication arrange perfectly for this purpose, as the maximum values would be 111 x 1111 = 0110 1001.



## Challenges & Lessons Learned
* ESD damage caused loss of an address line. Fortunately I was able to fix it by simply connecting an otherwise unused spare line.
* I might've bought a counterfeit MC14500 since, for certain instructions and pins, it was not behaving as intended:
	- the data pin requires around 40mA for a HIGH input, but the 74hc40-51 demultiplexers give around 10mA for a HIGH input. 10mA is, however, enough to turn on a 2N2222 NPN transistor, which in turn forwards a strong enough current from the power rails if it receives the 10mA.
	- the data pin also has problems with outputting things. Store instructions seem to behave semi-randomly, sometimes they output the correct value, sometimes they don't. By hardcoding an XOR circuit to filter the problematic instructions, they now function as expected.



### Potential Future Improvements
Replace damaged components.
Explore faster clock speeds.
Add better display for debugging (7-segment display or serial monitor).

### Acknowledgements
David from Usagi Electric for inspiring me to do this project and for designing his implementation of the Minimal ICU Unit.