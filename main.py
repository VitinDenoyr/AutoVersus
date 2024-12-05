from objects import (
	Characters, AudioCollection, StatsOrdering #Classes
)
from classes import (
	TRANSITION_RANDOM, TRANSITION_NONE, TRANSITION_FADE, TRANSITION_ZOOM_IN, TRANSITION_ZOOM_OUT,
	TRANSITION_ROTATE_L, TRANSITION_ROTATE_R, #Constantes
	TRANSITION_SLIDE_L, TRANSITION_SLIDE_R, TRANSITION_SLIDE_U, TRANSITION_SLIDE_D,
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
    ch.BesouroMahoraga(), ch.Ragna(), #Personagens
    aud.DontLike(), #Áudio
    stats.Combat(), #Tipo de Status
    True, #Status Aleatórios (False -> pré-configurados, True -> aleatórios)
	TRANSITION_RANDOM #Tipo de transição entre cenas
)
result, directory = vid.createVideo()
result.write_videofile(directory,fps=FRAME_COUNT)