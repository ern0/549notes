#include <stdio.h>
#include <stdint.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_audio.h>
	
	#define u32 uint32_t

	void playerInit();
	uint32_t playerTick();
	void noteTick();
	void freqTick();
	uint32_t playerMix();


	uint32_t audioSample = 0;	
	uint32_t lastSample = 0;
	uint32_t lastResult = 0;
	void audioCallback(void* userdata,unsigned char* stream,int len);


	int main(int argc,char* argv[]) {

		SDL_AudioSpec want;
		SDL_AudioSpec have;
		SDL_AudioDeviceID dev;

		SDL_Init(SDL_INIT_AUDIO);

		SDL_zero(want);
		want.freq = 44100;
		want.format = AUDIO_S16SYS;
		want.channels = 1;
		want.samples = 4096;
		want.callback = audioCallback;
		want.userdata = (void*)&audioSample;
		dev = SDL_OpenAudioDevice(NULL,0,&want,&have,0);

		if (dev == 0) {
	    SDL_Log("Failed to open audio: %s",SDL_GetError());
	    return 2;
		}

		fprintf(stderr,"playing... ");
		SDL_PauseAudioDevice(dev,0);
		playerInit();
		SDL_Delay(55000);

		fprintf(stderr,"\n");
		SDL_PauseAudioDevice(dev,1);
		SDL_CloseAudioDevice(dev);

		return 0;
	} // main()


	void audioCallback(void* userdata,unsigned char* stream,int len) {
		uint32_t* samplePtr = (uint32_t*)userdata;

		for (int i = 0; i < len; i += 2) {

			uint32_t sample = *samplePtr / (44100 / FREQ);
			uint32_t result;

			if (sample == lastSample) {
				result = lastResult;
			} else {
				result = ( playerTick() & 0xFF ) * VOLUME_MUL;
				lastSample = sample;
				lastResult = result;
			}

			uint16_t* store = (uint16_t*)&stream[i];
			*store = result;

			(*samplePtr)++;

		} // for stream

	} // audioCallback()
