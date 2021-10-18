#!/bin/bash

DIRETORIO_STREAM_RECORDER=/home/$USER/SINAPSES/playback_recorder

gnome-terminal --tab -t "GRAVANDO-89FM" -e "bash -c '$DIRETORIO_STREAM_RECORDER/venv/bin/python $DIRETORIO_STREAM_RECORDER/record_internet_radio_streaming.py --horario_livre=True'"


