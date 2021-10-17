
'''
https://stackoverflow.com/questions/4247248/record-streaming-and-saving-internet-radio-in-python
https://askubuntu.com/questions/60837/record-a-programs-output-with-pulseaudio
https://www.svnlabs.com/blogs/record-live-streaming-radio-to-mp3/
https://stackoverflow.com/questions/4247248/record-streaming-and-saving-internet-radio-in-python
https://www.svnlabs.com/blogs/record-live-streaming-radio-to-mp3/
http://manpages.ubuntu.com/manpages/impish/en/man1/streamripper.1.html

'''
import datetime
import os.path

URL_REQUEST_89FM = 'https://21933.live.streamtheworld.com/RADIO_89FM_ADP.aac?dist=site-89fm'

agora = datetime.datetime.now()
hora_formatada = agora.strftime('%d_%m_%Y_%H_hs_%M_min_%S_seg')

arquivo_mp3 = os.path.join(os.path.dirname(__file__), '/streams/89FM_{}.mp3'.format(hora_formatada))

comando_curl = 'curl -sS -o {} –max-time 1800 {}'.format(arquivo_mp3, URL_REQUEST_89FM)
comando_streamripper = 'streamripper {} -d ./streams -l 10800 -a {}'.format(URL_REQUEST_89FM, arquivo_mp3)

os.system('sudo apt-get install streamripper')

os.system(comando_streamripper)
