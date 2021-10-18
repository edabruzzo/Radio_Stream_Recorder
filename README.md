
# Configurando um alias no ~/.bashrc

vim /home/$USER/.bashrc

DIRETORIO_STREAM_RECORDER=/home/$USER/playback_recorder
alias gravar89FM = "$DIRETORIO_STREAM_RECORDER/venv/bin/python $DIRETORIO_STREAM_RECORDER/record_internet_radio_streaming.py --horario_livre=True"

:x

Após basta chamar da linha de comando:

usuario@computer:~$  gravar89FM


# Radio_Stream_Recorder

Se preferir, basta configurar um job no crontab

If you want to, you can schedule a job on crontab

 1. Entry: Minute when the process will be started [0-60]
 2. Entry: Hour when the process will be started [0-23]
 3. Entry: Day of the month when the process will be started [1-28/29/30/31]
 4. Entry: Month of the year when the process will be started [1-12]
 5. Entry: Weekday when the process will be started [0-6] [0 is Sunday]

 every each x minute = */x    

 So according to this spec 0 14 * * 0  would run 14:00 every Sunday.

![Screenshot from 2021-10-17 18-06-03](https://user-images.githubusercontent.com/18289389/137645043-8813a42c-e7e1-4dda-83e2-500a00d44385.png)
![Screenshot from 2021-10-17 21-47-34](https://user-images.githubusercontent.com/18289389/137651473-f0faa2e3-8085-4ab9-b2ba-965406a3f9cb.png)
![Screenshot from 2021-10-17 21-47-05](https://user-images.githubusercontent.com/18289389/137651475-c3ab2ba4-de1f-4a6c-8a73-69ddd30a9c4f.png)
![Screenshot from 2021-10-17 21-43-51](https://user-images.githubusercontent.com/18289389/137651476-8c07df2e-a30b-44bc-a3b2-06a1d505f478.png)
![Screenshot from 2021-10-17 21-41-08](https://user-images.githubusercontent.com/18289389/137651478-c2169a35-a9a8-46c7-8d28-fce8aa4c2ac4.png)


# Connecting...
# stream: Streamripper_rips
# server name: MediaGateway 5.6.1-0390.el6
# declared bitrate: 128
# meta interval: 16000

# [skipping...   ]  -  [    1kb]
# [ripping...    ] 89 FM - SÃ£o Paulo [  564kb]
# [ripping...    ] NO DOUBT - DON'T SPEAK [  3,86M]
# [ripping...    ] SANTANA/STEVEN TYLER - JUST FEEL BETTER [  3,72M]
# [ripping...    ] PLANET HEMP - CONTEXTO [  3,28M]
# [ripping...    ] U 2 - STILL HAVEN'T FOUND WHAT I'M LOOKING FOR [  4,03M]
# [ripping...    ] KINGS OF LEON - FAMILY TREE [  3,54M]
# [ripping...    ] LED ZEPPELIN - ROCK AND ROLL [  3,34M]
# [ripping...    ] THE ROLLING STONES - DON'T STOP [  3,60M]
# [ripping...    ] RUMBORA - O MAPA DA MINA [  3,10M]

