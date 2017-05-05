	#include "main.cpp"

	int waveLength[CHANNELS];
	int waveCounter[CHANNELS];
	int waveValue[CHANNELS];

	int notePtr;
	int noteCounter;


	void playerInit() {

		for (int i = 0; i < CHANNELS; i++) waveCounter[i] = 1;
		for (int i = 0; i < CHANNELS; i++) waveValue[i] = 0;
		for (int i = 0; i < CHANNELS; i++) waveLength[i] = 0;
		notePtr = 0;
		noteCounter = 1;

	} // playerInit()


	uint32_t playerTick() {

		noteTick();
		freqTick();
		return playerMix();

	} // playerTick()


	void noteTick() {

		--noteCounter;
		if (noteCounter > 0) return;
		noteCounter = FREQ / (BPM/60);

		for (int i = 0; i < CHANNELS; i++) {

			int note = notes[notePtr];
			notePtr++;
			if (notePtr == sizeof(notes)) {
				notePtr = 0;
			}

			if (note < 0) {
				waveLength[i] = 0;
			} else {
				waveLength[i] = scale[note];
			}

		} // foreach channels
	} // noteTick()


	void freqTick() {
		for (int i = 0; i < CHANNELS; i++) {

			if (waveLength[i] == 0) continue;

			--waveCounter[i];
			if (waveCounter[i] > 0) continue;
			waveCounter[i] = waveLength[i];

			waveValue[i] ^= 0xFF;

		} // foreach channels
	} // freqTick()


	uint32_t playerMix() {
		uint32_t value = 0;

		for (int i = 0; i < CHANNELS; i++) {
			value += waveValue[i];
		}

		return value / CHANNELS;
	} // playerTick()
