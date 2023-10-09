#!/usr/bin/env python3

import wave
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel
import json


def write_dict_to_json(data, file_path):
    """
    Write a dictionary to a JSON file.

    Args:
        data (dict): The dictionary to be written.
        file_path (str): The path to the JSON file where data will be saved.
    """
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)  # Indent for pretty formatting


def generate_transcript(audio_file_path):
    # You can set log level to -1 to disable debug messages
    SetLogLevel(0)

    wf = wave.open(audio_file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    # model_path = os.path.join(os.getcwd(), 'models/vosk-model-small-en-us-0.15')
    model = Model(lang="en-us")

    # You can also init model by name or with a folder path
    # model = Model(model_name="vosk-model-en-us-0.21")
    # model = Model("models/en")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    rwlu = dict()
    pwlu = dict()

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            words = result["result"]
            start_time = words[0]["start"]
            end_time = words[-1]["end"]
            rwlu[start_time] = words
        else:
            partial_res = json.loads(rec.PartialResult())
            if not partial_res["partial"]:
                continue
            words = partial_res["partial_result"]
            start_time = words[0]["start"]
            end_time = words[-1]["end"]
            pwlu[start_time] = words

    lookup_map = dict()

    def map_words_to_time_stamps(items: list, ts_lookup: dict):
        for item in items:
            key = f"{item['start']}|{item['end']}"
            if key in ts_lookup.keys():
                curr = ts_lookup[key]
                if curr["conf"] < item["conf"]:
                    ts_lookup[key] = item
            else:
                ts_lookup[key] = item
        return

    partial_word_sets = pwlu.values()
    real_word_sets = rwlu.values()

    for word_set in partial_word_sets:
        map_words_to_time_stamps(word_set, lookup_map)

    for word_set in real_word_sets:
        map_words_to_time_stamps(word_set, lookup_map)

    transcript_words = list(lookup_map.values())
    transcript = sorted(transcript_words, key=lambda x: (x["start"], x["end"]))
    write_dict_to_json(transcript, "transcript.json")
    return transcript
