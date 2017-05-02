	#define FREQ 8000
	#define VOLUME_MUL 10

	#include "main.cpp"


	uint32_t freqCounter;
	uint32_t value;


	void playerInit() {

		freqCounter = 0;
		value = 0;

	} // playerInit()


	uint32_t playerTick() {

		freqCounter++;
		if (freqCounter < 12) return value;
		freqCounter = 0;

		value = value ^ 0xFF;

		return value;
	} // playerTick()