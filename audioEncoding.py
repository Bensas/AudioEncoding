import sounddevice as sd
from scipy.io.wavfile import write

import pydub
from pydub import AudioSegment

#Recording constants
DEFAULT_SAMPLE_RATE = 44100

#Encoding constants
CHUNK_LENGTH = 50

def record_audio_segment(length):
	sampleRate = DEFAULT_SAMPLE_RATE
	myrecording = sd.rec(int(length * sampleRate), samplerate=sampleRate, channels=2)
	sd.wait()  # Wait until recording is finished
	write('temp.wav', sampleRate, myrecording)  # Save as WAV file 
	audioSegment = AudioSegment.from_file("temp.wav", format="wav")
	return audioSegment

def reverse_encode_audio_segment(audioSegment):
	slices = list(originalSound[::CHUNK_LENGTH])

	if (len(slices[ len(slices)-1 ]) != CHUNK_LENGTH):
		del slices[ len(slices)-1 ]
	appendedSounds = slices[len(slices)-1]

	for i in range(len(slices)-1):
		appendedSounds += slices[len(slices) - 2 - i]

	return appendedSounds

def simple_encode_audio_segment(audioSegment, nonce):
	slices = list(originalSound[::CHUNK_LENGTH])

	if (len(slices[ len(slices)-1 ]) != CHUNK_LENGTH):
		del slices[ len(slices)-1 ]

#The "tail" of a sliced audio segment is the last chunk if it's shorter than
#the default chunk length
def slice_audio_and_trim_tail()

#Encoding a sound using the reverse method
originalSound = AudioSegment.from_file("original.wav", format="wav")
appendedSounds = reverse_encode_audio_segment(originalSound)
result = appendedSounds.export("reverse_encoded.wav", format="wav")

