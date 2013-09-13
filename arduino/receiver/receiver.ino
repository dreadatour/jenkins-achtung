#include <VirtualWire.h>

int ledPin = 13;  // pin with led on it
int relayPin = 3;  // pin with relay on it

byte input_data[VW_MAX_MESSAGE_LEN];  // a buffer to store the incoming messages
byte input_size = VW_MAX_MESSAGE_LEN;  // the size of the message

void setup() {
	// setup led pin
	pinMode(ledPin, OUTPUT);
	digitalWrite(ledPin, LOW);

	// setup relay pin
	pinMode(relayPin, OUTPUT);
	digitalWrite(relayPin, HIGH);

	// initialize the IO and ISR
	vw_set_ptt_inverted(true);  // required for DR3100
	vw_setup(1200); // bits per sec
	vw_rx_start(); // start the receiver
}

void loop() {
	// check if we have some data to process
	if (vw_get_message(input_data, &input_size)) {
		digitalWrite(ledPin, HIGH);
		if (strncmp((char*) input_data, "Achtung ON", 10) == 0) {
			digitalWrite(relayPin, LOW);  // achtung! turn relay on
		} else if (strncmp((char*) input_data, "Achtung OFF", 11) == 0) {
			digitalWrite(relayPin, HIGH);  // turn relay off
		} else {
			delay(1000);
		}
		digitalWrite(ledPin, LOW);
	}
}
