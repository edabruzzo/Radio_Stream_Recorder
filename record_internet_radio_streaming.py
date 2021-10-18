
'''
https://stackoverflow.com/questions/4247248/record-streaming-and-saving-internet-radio-in-python
https://askubuntu.com/questions/60837/record-a-programs-output-with-pulseaudio
https://www.svnlabs.com/blogs/record-live-streaming-radio-to-mp3/
https://stackoverflow.com/questions/4247248/record-streaming-and-saving-internet-radio-in-python
https://www.svnlabs.com/blogs/record-live-streaming-radio-to-mp3/
http://manpages.ubuntu.com/manpages/impish/en/man1/streamripper.1.html
https://stackoverflow.com/questions/16717930/how-to-run-crontab-job-every-week-on-sunday


https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da
https://docs.python.org/pt-br/3/library/datetime.html

https://www.py4u.net/discuss/169119
'''
import datetime
from datetime import time
import os.path

def executa_gravador_streamin(LIMITAR_TARDES_DOMINGO=True):

    URL_REQUEST_89FM = 'https://21933.live.streamtheworld.com/RADIO_89FM_ADP.aac?dist=site-89fm'

    agora = datetime.datetime.now()
    hora_formatada = agora.strftime('%d_%m_%Y_%H_hs_%M_min_%S_seg')

    diretorio_projeto = os.path.dirname(__file__)
    arquivo_mp3 = '{}/streams/Streamripper_rips/incomplete/89FM_{}.mp3'\
                    .format(diretorio_projeto, hora_formatada)

    comando_curl = 'curl -sS -o {} –max-time 1800 {}'.format(arquivo_mp3, URL_REQUEST_89FM)
    comando_streamripper = 'streamripper {} -d ./streams -l 10800 -a {}'.format(URL_REQUEST_89FM, arquivo_mp3)

    if LIMITAR_TARDES_DOMINGO:
        hoje = datetime.datetime.today().isoweekday()  # "Return day of the week, where Monday == 1 ... Sunday == 7."
        if hoje == 7:
            try:
                RELATORIO = '{}/streams/Streamripper_rips/incomplete/RELATORIO_{}.txt'.format(diretorio_projeto, hora_formatada)
                os.system(comando_streamripper + ' >> {}'.format(RELATORIO))
            except:
                os.system('sudo apt-get install streamripper')

            finally:
                diretorio_streams_completos = os.path.join(diretorio_projeto, 'streams/Streamripper_rips')
                diretorio_musicas_baixadas = os.path.join(diretorio_projeto, 'musicas_baixadas')
                os.system('mv {}/*.acc {}'.format(diretorio_streams_completos, diretorio_musicas_baixadas))
                os.system('mv {}/RELATORIO_* {}'.format(diretorio_streams_completos, diretorio_musicas_baixadas))

def esta_dentro_do_horario_limite(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.now().time()
    return check_time >= begin_time or check_time <= end_time


def argumentos_linha_comando():
    '''https://cadernodelaboratorio.com.br/python-3-processando-argumentos-da-linha-de-comando/'''
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Determina se há restrição de dia e horário')

    parser.add_argument('--horario_livre', type=bool, default=False,
                        help="""
                            Permite a execução em qualquer horário
                         
                                """)
    parser.add_argument('--tardes_domingo', type=bool, default=False,
                        help="""
                                 Execução apenas domingo
                            """)

    args = parser.parse_args()

    TARDES_DOMINGO = args.tardes_domingo
    HORARIO_LIVRE = args.horario_livre

    return TARDES_DOMINGO, HORARIO_LIVRE


if __name__ == "__main__":

    LIMITAR_A_TARDES_DOMINGO, HORARIO_LIVRE = argumentos_linha_comando()

    if HORARIO_LIVRE:
        print('Aguardando interrupção manual do programa')
        executa_gravador_streamin()


    else:

        while True:

            dentro_do_horario_limite = esta_dentro_do_horario_limite(time(14, 00), time(20, 35))

            if dentro_do_horario_limite:
                executa_gravador_streamin()
            else:
                exit()
