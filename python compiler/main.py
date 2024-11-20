header_block = """const int bit0 = 2;
const int bit1 = 3;
const int bit2 = 4;
const int bit3 = 5;
const int bit4 = 6;
const int bit5 = 7;
const int bit6 = 8;
const int bit7 = 9;
const int clk = 10;

int data[] = {"""

data_block = """
"""

footer_block = """};

int program_length = sizeof(data) / sizeof(data[0]);

void setup() {

	pinMode (bit0, OUTPUT);
	pinMode (bit1, OUTPUT);
	pinMode (bit2, OUTPUT);
	pinMode (bit3, OUTPUT);
	pinMode (bit4, OUTPUT);
	pinMode (bit5, OUTPUT);
	pinMode (bit6, OUTPUT);
	pinMode (bit7, OUTPUT);
	pinMode (clk, OUTPUT);
	pinMode (11, INPUT);

}

void loop() {

	// store program in SRAM 
	for (int y = 0; y < program_length; y++) {

		// initialize all bits as LOW
		digitalWrite(bit0, LOW);
		digitalWrite(bit1, LOW);
		digitalWrite(bit2, LOW);
		digitalWrite(bit3, LOW);
		digitalWrite(bit4, LOW);
		digitalWrite(bit5, LOW);
		digitalWrite(bit6, LOW);
		digitalWrite(bit7, LOW);
		digitalWrite(clk, LOW);
		digitalWrite(11, LOW);

		// write HIGH for the appropriate bits
		if(bitRead(data[y], 0) == 1) {digitalWrite(bit0, HIGH);}
		if(bitRead(data[y], 1) == 1) {digitalWrite(bit1, HIGH);}
		if(bitRead(data[y], 2) == 1) {digitalWrite(bit2, HIGH);}
		if(bitRead(data[y], 3) == 1) {digitalWrite(bit3, HIGH);}
		if(bitRead(data[y], 4) == 1) {digitalWrite(bit4, HIGH);}
		if(bitRead(data[y], 5) == 1) {digitalWrite(bit5, HIGH);}
		if(bitRead(data[y], 6) == 1) {digitalWrite(bit6, HIGH);}
		if(bitRead(data[y], 7) == 1) {digitalWrite(bit7, HIGH);}

		// pulse the clock
		//digitalWrite(clk, HIGH);
		//delay(200);
		//digitalWrite(clk, LOW);
		//delay(200);
		
		// wait for manual clock
        while (digitalRead(11) == LOW) {}

		// pulse the clock
		digitalWrite(13, HIGH);
		delay(1000);
	}

	// stop loop() after the for loop is done
	while(1);
}
"""

instruction_codes = {
    "input_enable": "1010",
    "output_enable": "1011",
    "jump": "1100",
    "return": "1101",
    "skip_if_zero": "1110",
    "halt": "1111",
    "no_change": "0000",
    "load": "0001",
    "loadc": "0010",
    "store": "1000",
    "storec": "1001",
    "and": "0011",
    "andc": "0100",
    "or": "0101",
    "orc": "0110",
    "xnor": "0111"
}





# compile the input file
input_file_name = "input.txt"

# keeps track of the number of lines so that you are warned not to exceed the storage of the SRAM
maxlines = 256
linecount = 0

with open(input_file_name, "r") as file:

    for line in file:

        words = line.strip().split()

        # ignore comments and empty lines
        if len(words) > 0:
            if words[0] != "//":

                instruction, chip_select, address = words

                # convert words from code to binary
                instruction_bin = instruction_codes[instruction]

                chip_select_bin = 1
                if chip_select == "scr":
                    chip_select_bin = 0

                address_bin = format(int(address), '03b')

                # put together with binary specifier and comma
                processed_line = "0b" + instruction_bin + str(chip_select_bin) + str(address_bin) + "," + "\n"

                # add the processed_line to the data_block
                data_block += processed_line
                # increment the instruction line count
                linecount += 1

    # remove the comma after the last instruction in the array
    data_block = data_block[:-2]

print(f"Program uses {linecount} instructions, out of {maxlines} available.")

if linecount > maxlines:
    print(f"WARNING: number of maximum instructions exceeded.")





# write compiled code to output
output_file_name = "output.ino"

with open(output_file_name, "w") as file:
    file.write(header_block + "\n")
    file.write(data_block + "\n\n")
    file.write(footer_block)

print(f"Finished compiling {output_file_name}.")