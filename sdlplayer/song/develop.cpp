#define FREQ 11025
#define VOLUME_MUL 20
#define CHANNELS 1
#define BPM 580

static int scale[] = {
	
	(int)(FREQ / 61.74),
	(int)(FREQ / 65.41),
	(int)(FREQ / 69.30),	
	(int)(FREQ / 73.42),
	(int)(FREQ / 77.78),
	(int)(FREQ / 82.41),
	(int)(FREQ / 87.31),
	(int)(FREQ / 92.50),
	(int)(FREQ / 98.00),
	(int)(FREQ / 103.83),
	(int)(FREQ / 110.00),
	(int)(FREQ / 116.54),
	(int)(FREQ / 123.47),	
	(int)(FREQ / 130.81),	
	(int)(FREQ / 138.59),	
	(int)(FREQ / 146.83),	
	(int)(FREQ / 155.56),
	(int)(FREQ / 164.81),
	(int)(FREQ / 174.61),
	(int)(FREQ / 185.00),
	(int)(FREQ / 196.00),
	(int)(FREQ / 207.65),
	(int)(FREQ / 220.00),
	(int)(FREQ / 233.08),
	(int)(FREQ / 246.94),
	(int)(FREQ / 261.63),
	(int)(FREQ / 277.18),
	(int)(FREQ / 293.66),
	(int)(FREQ / 311.13),
	(int)(FREQ / 329.63),
	(int)(FREQ / 349.23),
	(int)(FREQ / 369.99),
	(int)(FREQ / 392.00),
	(int)(FREQ / 415.30),
	(int)(FREQ / 440.00),
	(int)(FREQ / 466.16),
	(int)(FREQ / 493.88),
	(int)(FREQ / 523.25),
	(int)(FREQ / 554.37),
	(int)(FREQ / 587.33),
	(int)(FREQ / 622.25),
	(int)(FREQ / 659.25),
	(int)(FREQ / 698.46),
	(int)(FREQ / 739.99),
	(int)(FREQ / 783.99),
	(int)(FREQ / 830.61)
};

static char notes[] = {

	13,
	-1,
	-1,

	13,
	-1,
	-1,

	13,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	16,
	-1,
	-1,

	16,
	-1,
	-1,

	16,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	21,
	-1,
	-1,

	21,
	-1,
	-1,

	21,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	15,
	-1,
	-1,

	15,
	-1,
	-1,

	8,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1,

	-1,
	-1,
	-1

};

#include "../player.cpp"