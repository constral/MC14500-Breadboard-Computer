const int bit0 = 2;
const int bit1 = 3;
const int bit2 = 4;
const int bit3 = 5;
const int bit4 = 6;
const int bit5 = 7;
const int bit6 = 8;
const int bit7 = 9;
const int clk = 10;

int data[] = {

0b01101000,
0b10101000,
0b10111000,
0b00010111,
0b01111001,
0b01110000,
0b10000110,
0b00011001,
0b01010000,
0b00110111,
0b10000111,
0b00011001,
0b00110000,
0b01010111,
0b10000111,
0b00010110,
0b10000000,
0b00001000,
0b00010111,
0b01111010,
0b01110001,
0b10000110,
0b00011010,
0b01010001,
0b00110111,
0b10000111,
0b00011010,
0b00110001,
0b01010111,
0b10000111,
0b00010110,
0b10000001,
0b00001000,
0b00010111,
0b01111011,
0b01110010,
0b10000110,
0b00011011,
0b01010010,
0b00110111,
0b10000111,
0b00011011,
0b00110010,
0b01010111,
0b10000111,
0b00010110,
0b10000010,
0b00001000,
0b00010111,
0b01111100,
0b01110011,
0b10000110,
0b00011100,
0b01010011,
0b00110111,
0b10000111,
0b00011100,
0b00110011,
0b01010111,
0b10000111,
0b00010110,
0b10000011,
0b00001000,
0b00010111,
0b01111101,
0b01110100,
0b10000110,
0b00011101,
0b01010100,
0b00110111,
0b10000111,
0b00011101,
0b00110100,
0b01010111,
0b10000111,
0b00010110,
0b10000100,
0b00001000,
0b00010111,
0b01111110,
0b01110101,
0b10000110,
0b00011110,
0b01010101,
0b00110111,
0b10000111,
0b00011110,
0b00110101,
0b01010111,
0b10000111,
0b00010110,
0b10000101,
0b00010111,
0b10000110,
0b01001000,
0b10000111,
0b11111000

};

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
