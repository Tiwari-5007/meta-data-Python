from pydub import AudioSegment
from logsHandler import logw

def mix_audio_files(in_file, out_file, result_file):
  try:
    in_audio = AudioSegment.from_file(in_file)
    out_audio = AudioSegment.from_file(out_file)

    min_length = min(len(in_audio), len(out_audio))
    in_audio = in_audio[:min_length]
    out_audio = out_audio[:min_length]

    result_audio = in_audio + out_audio

    result_audio.export(result_file, format="wav")
    print(f"Audio files mixed and saved to {result_file}")
    return result_file
  except Exception as e:
    print(e);
    return False
