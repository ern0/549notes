	#define FREQ 8000
	#define VOLUME_MUL 50

	#include "main.cpp"


	uint32_t playerCounter;
	uint32_t playerValue;


	void playerInit() {

		playerCounter = 0;
		playerValue = 0;

	} // playerInit()


	uint32_t playerTick() {

		playerCounter++;
		if (playerCounter < 100) return playerValue;
		playerCounter = 0;

		playerValue = playerValue ^ 0xFF;

		return playerValue;
	} // playerTick()