'''


https://stackoverflow.com/questions/2046663/record-output-sound-in-python


'''



# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
from datetime import time


def read_sound_device_output():
    import pyaudio, wave, sys

    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = sys.argv[1]

    p = pyaudio.PyAudio()
    channel_map = (0, 1)

    stream_info = pyaudio.PaMacCoreStreamInfo(
        flags = pyaudio.PaMacCoreStreamInfo.paMacCorePlayNice,
        channel_map = channel_map)

    stream = p.open(format = FORMAT,
                    rate = RATE,
                    input = True,
                    input_host_api_specific_stream_info = stream_info,
                    channels = CHANNELS)

    all = []
    for i in range(0, RATE / chunk * RECORD_SECONDS):
            data = stream.read(chunk)
            all.append(data)
    stream.close()
    p.terminate()

    data = ''.join(all)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()






def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da
def esta_dentro_do_horario_limite(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.datetime.now().time()
    return check_time >= begin_time or check_time <= end_time

dentro_do_horario_limite = esta_dentro_do_horario_limite(time(14,00), time(19,00))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hoje = datetime.datetime.today().isoweekday() # "Return day of the week, where Monday == 1 ... Sunday == 7."
    print(hoje)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
