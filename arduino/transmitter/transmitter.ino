#include <VirtualWire.h>

int ledPin = 13;  // pin with led on it

char incoming_byte;   // a buffer to store the incoming messages
char input_data[12];  // the size of the message
int input_size = 0;  // counter, just counter

void setup() {
	// setup led pin
	pinMode(ledPin, OUTPUT);
	digitalWrite(ledPin, LOW);

	// initialize serial (9600 bps)
	Serial.begin(9600);
	Serial.println("Ready for achtung");

	// initialize the IO and ISR
	vw_set_ptt_inverted(true);  // required for DR3100
	vw_setup(1200); // bits per sec
}

void loop() {
	while (Serial.available() > 0) {
		incoming_byte = Serial.read();  // read the incoming byte

		if (incoming_byte == '\n') {
			input_data[input_size++] = 0;
			if (strncmp(input_data, "Achtung ON", 10) == 0 || strncmp(input_data, "Achtung OFF", 11) == 0) {
				digitalWrite(ledPin, HIGH);
				vw_send((uint8_t *)input_data, input_size);
				vw_wait_tx();  // wait until the whole message is gone
				digitalWrite(ledPin, LOW);

				Serial.println("OK");
			} else {
				Serial.println("FAIL");
			}
			while (input_size-- >= 0) {
				input_data[input_size] = 0;
			}
			input_size = 0;  // reset counter
		} else {
			if (input_size <= 11) {
				input_data[input_size] = incoming_byte;
			}
			input_size++;
		}
	}
}
