from objects import (
	Characters, AudioCollection, StatsOrdering #Classes
)
from classes import (
	TRANSITION_NONE, TRANSITION_FADE, TRANSITION_ZOOM_IN, TRANSITION_ZOOM_OUT, TRANSITION_ROTATE, #Constantes
	FRAME_COUNT, FRAME_DURATION,
	FullVideo, #Classes
	os #Bibliotecas
)

#Diretórios
imagesPath = os.path.join(os.getcwd(), 'images')
gifsPath = os.path.join(os.getcwd(), 'gifs')
audiosPath = os.path.join(os.getcwd(), 'audios')
outputPath = os.path.join(os.getcwd(), 'videos')
textPath = os.path.join(os.getcwd(), 'texts')

ch = Characters()
aud = AudioCollection()
stats = StatsOrdering()

vid = FullVideo(
    ch.BesouroMahoraga(),ch.HamoodHabibi(), #Personagens
    aud.WeLive(), #Áudio
    stats.Combat(), #Tipo de Status
    True, #Status Aleatórios (False -> pré-configurados, True -> aleatórios)
	TRANSITION_ROTATE #Tipo de transição entre cenas
)
result, directory = vid.createVideo()
result.write_videofile(directory,fps=FRAME_COUNT)