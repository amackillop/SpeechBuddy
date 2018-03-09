import io


#use operating system dependant functionality
import os


#Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave

def googleApiCall(path):

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = path #'/home/sanghs3/Capstone/umm.flac'


    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='en-US',
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    response = formatResponse(response)
    return response

def formatResponse(response):
    stringData="{";
    for result in response.results:
        alternative = result.alternatives[0]
        stringData = stringData + '"Transcript":"' + str(alternative.transcript.encode('ascii')) + '",'
        stringData = stringData + '"Confidence":' + str(alternative.confidence) + '}'
        movingWindow=[]

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))
                

        indexS = 4
        indexE = 0
        for index in range(indexS,len(alternative.words)):
            startFrame = alternative.words[indexE].start_time.seconds + alternative.words[indexE].start_time.nanos * 1e-9
            endFrame = alternative.words[indexS].end_time.seconds + alternative.words[indexS].end_time.nanos * 1e-9
            wpm = round(endFrame - startFrame,1)
            movingWindow.append(wpm)
            indexE = indexE + 1
            indexS = indexS + 1
        #print movingWindow
    return [alternative.transcript.encode('ascii'),alternative.confidence, movingWindow]
