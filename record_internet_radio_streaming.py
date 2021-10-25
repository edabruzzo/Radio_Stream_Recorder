
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


http://streamripper.sourceforge.net/tutorialconsole.php
http://streamripper.sourceforge.net/

'''
import datetime
import sys
from datetime import time
import time as dormir
import os.path
import schedule
from multiprocessing_parallelization.multiprocessamento import Multiprocessamento

diretorio_projeto = os.path.dirname(__file__)

sys.path
arquivo_multiprocessamento = os.path.join(diretorio_projeto, 'multiprocessing_parallelization/multiprocessamento.py')
sys.path.append(arquivo_multiprocessamento)


diretorio_streams_completos = os.path.join(diretorio_projeto, 'streams/Streamripper_rips')
diretorio_musicas_baixadas = os.path.join(diretorio_projeto, 'musicas_baixadas')
diretorio_relatorios = os.path.join(diretorio_projeto, 'relatorios')
diretorio_streams_incompletos = os.path.join(diretorio_streams_completos, 'incomplete')

tempo_espera_global=240 # Delay for 4 minutes (240 seconds).
paralelizar = False



def manipular_arquivos_audio(finalizacao=False):

    comando_ffmpeg = 'for f in *.aac; do ffmpeg -i "$f" -acodec libmp3lame -ab 256k "$f.mp3"; done'
    os.system("""cd {} && rm 89\ FM\ -\ SÃ£o\ Paulo*""".format(diretorio_streams_completos))
    os.system('cd {} && {}'.format(diretorio_streams_completos, comando_ffmpeg))
    os.system('cd {} && rm *.aac && rm *.cue'.format(diretorio_streams_completos))
    if finalizacao:
        os.system('cd {} && rm *.aac && rm *.cue'.format(diretorio_streams_incompletos))
    os.system('mv {}/*.mp3 {}'.format(diretorio_streams_completos, diretorio_musicas_baixadas))


def converter_musicas_completas_por_tempo_espera(tempo_espera=tempo_espera_global):

    while True:
        print('Iniciando conversão da próxima música completa pelo tempo médio de 4 minutos')
        manipular_arquivos_audio()
        print('Aguardando próxima música completa pelo tempo médio de 4 minutos')
        dormir.sleep(tempo_espera)



def executa_gravador_streaming(URL_REQUEST, tempo_limite_segundos=14400, **kwargs):
    '''

    tempo_limite_segundos=14400
    Gravação por 4 horas = 4 h x 60 min x 60 seg = 14400 segundos

    '''
    agora = datetime.datetime.now()
    hora_formatada = agora.strftime('%d_%m_%Y_%H_hs_%M_min_%S_seg')


    arquivo_mp3 = '{}/streams/Streamripper_rips/incomplete/PROGRAMACAO_LOCUTOR_COMERCIAIS_{}'\
                    .format(diretorio_projeto, hora_formatada)

    comando_curl = 'curl -sS -o {} –max-time 1800 {}'.format(arquivo_mp3, URL_REQUEST)
    if tempo_limite_segundos is not None:
        timeout = f'-l {tempo_limite_segundos}'
        horas_restantes = (tempo_limite_segundos / 60)/60
        hora_exata_termino = datetime.datetime.now() + datetime.timedelta(hours=horas_restantes)


        print(f'Esta gravação terminará em {horas_restantes}')
        print(f'Esta gravação terminará às {hora_exata_termino.strftime("%H:%M")}')
        print('A menos que a gravação de stremas seja interrompida')

    comando_streamripper = 'streamripper {} -d {}/streams {} -a {}'.format(URL_REQUEST, diretorio_projeto, timeout, arquivo_mp3)

    try:
        RELATORIO = '{}/streams/Streamripper_rips/incomplete/RELATORIO_{}.txt'.format(diretorio_projeto, hora_formatada)
        os.system(comando_streamripper + ' >> {}'.format(RELATORIO))

    except Exception as erro:
        print(erro)
        exit()
        #os.system('sudo apt-get install streamripper')


    finally:

        try:

            arquivos_ripped_repetidos = [arquivo_aac for arquivo_aac in os.listdir(diretorio_streams_completos)
                                         if arquivo_aac in os.listdir(diretorio_musicas_baixadas)]

            for arquivo in arquivos_ripped_repetidos:
                os.remove(os.path.join(diretorio_streams_completos, arquivo))

            manipular_arquivos_audio(finalizacao=True)

            arquivos_estranhos = [arquivo for arquivo in os.listdir(diretorio_musicas_baixadas) 
                                  if (' -  (' in arquivo and  ').mp3' in arquivo)
                                        or (' - .mp3' in arquivo)
                                      or (('89 FM - S') in arquivo)]

            for arquivo_estranho in arquivos_estranhos:
                os.remove(os.path.join(diretorio_musicas_baixadas, arquivo_estranho))

        except Exception as erro:
            print(erro)

        os.system('mv {}/RELATORIO_* {}'.format(diretorio_streams_incompletos, diretorio_relatorios))
        os.system(f'{diretorio_projeto}/venv/bin/python {__file__}')

def esta_dentro_do_horario_limite(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.datetime.now().time()
    return check_time >= begin_time and check_time <= end_time


def argumentos_linha_comando():
    '''https://cadernodelaboratorio.com.br/python-3-processando-argumentos-da-linha-de-comando/'''
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Determina se há restrição de dia e horário')

    parser.add_argument('--horario_livre', type=bool, default=False,
                        help="""
                            Permite a execução em qualquer horário
                         
                                """)

    parser.add_argument('--job', type=bool, default=False,
                        help="""
                                Permite a execução com agendamento

                                    """)

    parser.add_argument('--tardes_domingo', type=bool, default=False,
                        help="""
                                 Execução apenas domingo
                            """)

    args = parser.parse_args()

    TARDES_DOMINGO = args.tardes_domingo
    HORARIO_LIVRE = args.horario_livre
    JOB = args.job

    return TARDES_DOMINGO, HORARIO_LIVRE, JOB


def agendar_execucao(url):

    if dentro_do_horario_limite or HORARIO_LIVRE:

        horario_dois_da_tarde = '14:00:00'
        horario_ramona_89 = '12:00:00'
        horario_cadu = '06:00:00'
        maratona_rock_n_roll = '14:00:00'
        maratona_rock_n_roll_2 = '18:00:00'
        diariamente_boas_musicas_1 = '21:00:00'
        horario_esquenta = '22:00:00'

        schedule.every().sunday.at(maratona_rock_n_roll).do(executa_gravador_streamin(url, limite_horas=4))
        schedule.every().sunday.at(maratona_rock_n_roll_2).do(executa_gravador_streamin(url, limite_horas=3))

        week = datetime.datetime.today().weekday()
        if week < 6:
            schedule.every().day.at(horario_cadu).do(executa_gravador_streamin(url, limite_horas=3))
            schedule.every().day.at(horario_ramona_89).do(executa_gravador_streamin(url, limite_horas=3))
            schedule.every().day.at(horario_dois_da_tarde).do(executa_gravador_streamin(url, limite_horas=5))
            schedule.every().day.at(diariamente_boas_musicas_1).do(executa_gravador_streamin(url, limite_horas=3))


if __name__ == "__main__":

    LIMITAR_A_TARDES_DOMINGO, HORARIO_LIVRE, JOB = argumentos_linha_comando()

    '''
    Atençaõ ! 
    
    A URL muda de tempos em tempos
    
    Necessário dar F12 na rádio online para descobrir a URL do streaming
    https://www.radiorock.com.br/player/
    
    https://21933.live.streamtheworld.com/RADIO_89FM_ADP.aac?dist=site-89fm
    'https://24963.live.streamtheworld.com/RADIO_89FM_ADP.aac?dist=site-89fm'
    https://20833.live.streamtheworld.com/RADIO_89FM_ADP.aac?dist=site-89fm
    'https://playerservices.streamtheworld.com/api/livestream-redirect/RADIO_89FM_ADP.aac?dist=site-89fm'

    ERRO
    Time to stop is here, bailing
    shutting down
    
    
    '''
    URL_REQUEST_89FM = 'https://21933.live.streamtheworld.com/RADIO_89FM_ADP.aac?dist=site-89fm' \


    if JOB:
        agendar_execucao(URL_REQUEST_89FM)

    # "Return day of the week, where Monday == 1 ... Sunday == 7."
    hoje = datetime.datetime.today().isoweekday()
    if hoje != 7 and LIMITAR_A_TARDES_DOMINGO:
        print('Gravação de streaming limitada aos domingos')
        exit()
    else:
        if HORARIO_LIVRE:
            print('Aguardando interrupção manual do programa')

            if paralelizar:
                Multiprocessamento().paralelizar_execucao_processo(converter_musicas_completas_por_tempo_espera)
                Multiprocessamento().paralelizar_execucao_processo(executa_gravador_streaming,
                                                                   {'URL_REQUEST': URL_REQUEST_89FM})

            else:
                executa_gravador_streaming(URL_REQUEST=URL_REQUEST_89FM)

        else:
            while True:

                horario_do_quem_nao_faz_toma = esta_dentro_do_horario_limite(begin_time=time(19, 00), end_time=time(20, 00))
                horario_do_balacobaco = esta_dentro_do_horario_limite(begin_time=time(10, 00), end_time=time(12, 00))
                horario_do_rock_bola = esta_dentro_do_horario_limite(begin_time=time(20, 00), end_time=time(21, 00))

                hoje = datetime.datetime.today().isoweekday()
                work_days = [1,2,3,4,5] # Segunda=1, Domingo=7

                dentro_do_horario_limite = not (((horario_do_quem_nao_faz_toma or horario_do_balacobaco )
                                                and (hoje in work_days) )
                                                or (horario_do_rock_bola and hoje==1))

                if dentro_do_horario_limite:

                    if paralelizar:
                        Multiprocessamento().paralelizar_execucao_processo(converter_musicas_completas_por_tempo_espera)
                        Multiprocessamento().paralelizar_execucao_processo(executa_gravador_streaming,{'URL_REQUEST':URL_REQUEST_89FM})

                    else:
                        executa_gravador_streaming(URL_REQUEST=URL_REQUEST_89FM)

                else:
                    print('Fora do horário permitido para gravação de streaming')
                    import time as t
                    t.sleep(300) # 5 minutos
                    os.system(f'{diretorio_projeto}/venv/bin/python {__file__}')


