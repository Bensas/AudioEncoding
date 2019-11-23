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

#The "tail" of a sliced audio segment is the last chunk, 
# only if it's shorter than the default chunk length.
def slice_audio_and_trim_tail(audioSegment):
	slices = list(audioSegment[::CHUNK_LENGTH]) 
	if (len(slices[ len(slices)-1 ]) != CHUNK_LENGTH):
		del slices[ len(slices)-1 ]
	return slices

def reverse_encode_audio_segment(audioSegment):
	chunks = slice_audio_and_trim_tail(audioSegment)

	appendedSounds = chunks[len(chunks)-1]

	for i in range(len(chunks)-1):
		appendedSounds += chunks[len(chunks) - 2 - i]

	return appendedSounds

def simple_encode_audio_segment(audioSegment, nonce):
	chunks = slice_audio_and_trim_tail(audioSegment)
	assignedChunks = 0
	newChunkPositions = [None] * len(chunks)
	assignIndex = 0
	#We first generate the order in which the chunks will be appended
	#by assigning each chunk an index
	while assignedChunks < len(chunks):
		for i in range (nonce):
			assignIndex += 1
			if assignIndex >= len(chunks):
				assignIndex = 0;
		while newChunkPositions[assignIndex] is not None:
			assignIndex += 1
			if assignIndex >= len(chunks):
				assignIndex = 0;
		newChunkPositions[assignIndex] = assignedChunks
		assignedChunks += 1;

	for i in range(len(newChunkPositions)):
		print(newChunkPositions[i])

	#We then append all the chunks in the order given by our array
	appendedSounds = chunks[newChunkPositions[0]]
	for i in range(len(chunks)-1):
		appendedSounds += chunks[newChunkPositions[i+1]]
	return appendedSounds;

#Encoding a sound using the simple encode method
originalSound = AudioSegment.from_file("original.wav", format="wav")
encodedSound = simple_encode_audio_segment(originalSound, 4)
result = encodedSound.export("simple_encoded.wav", format="wav")


#Encoding a sound using the reverse method
# originalSound = AudioSegment.from_file("original.wav", format="wav")
# appendedSounds = reverse_encode_audio_segment(originalSound)
# result = appendedSounds.export("reverse_encoded.wav", format="wav")

