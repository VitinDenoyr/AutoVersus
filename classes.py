import moviepy.editor as MED
from PIL import Image
import cv2 as OpenCV
import numpy as NP
import subprocess
import random
import os

#Constantes: Ao atualizar transições, mude os limites da função randomTransition
TYPE_IMAGE = 0; TYPE_GIF = 1

STAT_COMBAT = 0; STAT_INTELLECT = 1

FRAME_COUNT = 60; FRAME_DURATION = 1/FRAME_COUNT; FRAME_60DURATION = 1/60

SCENE_INITIAL = 0; SCENE_NORMAL = 1; SCENE_FINAL = 2

TRANSITION_NONE = 0; TRANSITION_FADE = 1; TRANSITION_RANDOM = -1
TRANSITION_ZOOM_IN = 2; TRANSITION_ZOOM_OUT = 4
TRANSITION_ROTATE_L = 8; TRANSITION_ROTATE_R = 16; TRANSITION_ROTATIONS = 24
TRANSITION_SLIDE_L = 32; TRANSITION_SLIDE_U = 64; TRANSITION_SLIDE_R = 128; TRANSITION_SLIDE_D = 256; TRANSITION_SLIDES = 480

FXSTAGE_START = 0; FXSTAGE_END = 1

#Mapas
convertR = {TRANSITION_ROTATE_L: 1, TRANSITION_ROTATE_R: -1}
convertS = {TRANSITION_SLIDE_L: 0, TRANSITION_SLIDE_U: 1, TRANSITION_SLIDE_R: 2, TRANSITION_SLIDE_D: 3}

#Diretórios
imagesPath = os.path.join(os.getcwd(), 'images')
gifsPath = os.path.join(os.getcwd(), 'gifs')
audiosPath = os.path.join(os.getcwd(), 'audios')
outputPath = os.path.join(os.getcwd(), 'videos')
textPath = os.path.join(os.getcwd(), 'texts')

#--------------------------------------------------------------------------------------------------

#Funções úteis

#Escolhe um número aleatório que representa uma transição aleatória
def randomTransition():
	ans = random.randint(0,999)
	''' Distribuição de probabilidade
		None = 2%            Fade = 8%
		ZoomIn = 8%          ZoomOut = 10% 
		RotateL = 10.5%      RotateR = 10.5%
		SlideL = 10%         SlideR = 10%
		SLideU = 6.5%        SlideD = 6.5%
		RotL_Zout = 9%       RotR_Zout = 9%
	'''
	if ans in range(0,20):
		return TRANSITION_NONE
	elif ans in range(20,100):
		return TRANSITION_FADE
	elif ans in range(100,180):
		return TRANSITION_ZOOM_IN
	elif ans in range(180,280):
		return TRANSITION_ZOOM_OUT
	elif ans in range(280,385):
		return TRANSITION_ROTATE_L
	elif ans in range(385,490):
		return TRANSITION_ROTATE_R
	elif ans in range(490,590):
		return TRANSITION_SLIDE_L
	elif ans in range(590,690):
		return TRANSITION_SLIDE_R
	elif ans in range(690,755):
		return TRANSITION_SLIDE_U
	elif ans in range(755,820):
		return TRANSITION_SLIDE_D
	elif ans in range(820,910):
		return TRANSITION_ROTATE_L + TRANSITION_ZOOM_OUT
	elif ans in range(910,1000):
		return TRANSITION_ROTATE_R + TRANSITION_ZOOM_OUT

#Dado um frame, amplia ele em k vezes
def frame_zoomIn(frame, factor:float):
	h,w = frame.shape[:2] #Dimensões do frame em pixels
	nw,nh = max(int(w/factor),1),max(int(h/factor),1) #Novas dimensões
	cx,cy = w//2, h//2 #Centro da imagem (pivô de zoom)
	
	nx0 = max(0, cx - nw//2)
	nxn = max(min(w, cx + nw//2),nx0+1)
	ny0 = max(0, cy - nh//2)
	nyn = max(min(h, cy + nh//2),ny0+1)
 
	subframe = frame[ny0:nyn, nx0:nxn] #Subframe que ficará completo ao dar zoom
	return OpenCV.resize(subframe, (w,h))

def frame_zoomOut(frame, factor:float):
	h,w = frame.shape[:2] #Dimensões do frame em pixels
	nw,nh = max(int(w*factor),1),max(int(h*factor),1) #Novas dimensões
 
	baseframe = NP.zeros_like(frame)
 
	scaleframe = OpenCV.resize(frame.copy(), (nw,nh))
 
	nx0 = max((w - nw)//2,0)
	ny0 = max((h - nh)//2,0)
	nxn = min(nx0 + nw, w)
	nyn = min(ny0 + nh, h)
 
	dimx = nxn - nx0
	dimy = nyn - ny0

	baseframe[ny0:ny0+nh,nx0:nx0+nw] = scaleframe[:dimy,:dimx]
	return baseframe

def frame_rotate(frame, angle:float):
	h,w = frame.shape[:2]
	rotatedImage = Image.fromarray(frame).rotate(angle, expand=True)
	nh,nw = rotatedImage.height, rotatedImage.width
 
	scaleframe = 0
	if w/nw < h/nh:
		scaleframe = rotatedImage.resize((w,int(nh*(w/nw))))
	else:
		scaleframe = rotatedImage.resize((h,int(nw*(h/nh))))
	scaleframe = NP.array(scaleframe)

	rh, rw = scaleframe.shape[:2]
	baseframe = NP.zeros_like(frame)
	nx0 = max((w - rw)//2,0)
	ny0 = max((h - rh)//2,0)
	nxn = min(nx0 + rw,w)
	nyn = min(ny0 + rh,h)
 
	dimx = nxn - nx0
	dimy = nyn - ny0
 
	baseframe[ny0:ny0+rh,nx0:nx0+rw] = scaleframe[:dimy,:dimx]
	return baseframe

def frame_slide(frame, nextFrame, direction, progress):
	h,w = frame.shape[:2]
	baseframe = NP.zeros_like(frame)

	if direction%2 == 1: #Vertical
		nh = int(progress*h)
		if direction == 3: #Up
			baseframe[h-nh:h,:w] = nextFrame[:nh,:w]
			baseframe[:h-nh,:w] = frame[nh:h,:w]
		elif direction == 1: #Down
			baseframe[:nh,:w] = nextFrame[h-nh:h,:w]
			baseframe[nh:h,:w] = frame[:h-nh,:w]
	else: #Horizontal
		nw = int(progress*w)
		if direction == 2: #Left
			baseframe[:h,w-nw:w] = nextFrame[:h,:nw]
			baseframe[:h,:w-nw] = frame[:h,nw:w]
		elif direction == 0: #Right
			baseframe[:h,:nw] = nextFrame[:h,w-nw:w]
			baseframe[:h,nw:w] = frame[:h,:w-nw]

	return baseframe

#Efeitos customizados

def fx_zoom(get_frame, t, currentSceneDuration, zoomDuration, zoomFactor, zoomType):
	if zoomType == FXSTAGE_END:
		additionalTime = currentSceneDuration - zoomDuration
		if t - additionalTime < 0:
			return get_frame(t)
		if zoomFactor > 0:
			return frame_zoomIn(get_frame(t),(1 + zoomFactor)**round(max(t - additionalTime,0)*FRAME_COUNT))
		else:
			return frame_zoomOut(get_frame(t),(1 + zoomFactor)**round(max(t - additionalTime,0)*FRAME_COUNT))
	elif zoomType == FXSTAGE_START:
		if t > zoomDuration:
			return get_frame(t)
		if zoomFactor > 0:
			return frame_zoomIn(get_frame(t),(1 + zoomFactor)**round((zoomDuration - t)*FRAME_COUNT))
		else:
			return frame_zoomOut(get_frame(t),(1 + zoomFactor)**round((zoomDuration - t)*FRAME_COUNT))

def fx_rotate(get_frame, t, currentSceneDuration, rotationDuration, rotateType, direction):
	if rotateType == FXSTAGE_END:
		additionalTime = currentSceneDuration - rotationDuration
		if t - additionalTime < 0:
			return get_frame(t)
		return frame_rotate(get_frame(t),direction*90*((t - additionalTime)/rotationDuration))
	elif rotateType == FXSTAGE_START:
		if t > rotationDuration:
			return get_frame(t)
		return frame_rotate(get_frame(t),direction*(270 + 90*(t/rotationDuration)))

def fx_slide(get_frame, t, currentSceneDuration, slideDuration, direction, nextFrame):
	additionalTime = currentSceneDuration - slideDuration
	if t - additionalTime < 0:
		return get_frame(t)
	return frame_slide(get_frame(t),nextFrame,direction,max(0,min(100,(t - additionalTime)/(slideDuration))))

#--------------------------------------------------------------------------------------------------

#Classes

'''
Classe Timestamp
	- Tem parâmetros hora, minuto, segundo, centisegundo e duração. Representa um momento no tempo e uma duração em centisegundos.
	__repr__() -> Converte para uma string no formato 'HH:MM:SS.CC', usado também na inicialização
	fix() -> Impede valores inválidos em min, s, cs
	extract() -> Recebe uma string no formato de repr e guarda seus valores
	__sub__() -> Diferença entre dois timestamps: obtém a duração que o primeiro timestamp para ambos não se intersectarem
'''
class Timestamp:
	def __init__(self, content = None, duration = 0):
		self.h = 0
		self.min = 0
		self.s = 0
		self.cs = 0
		self.duration = duration
		if content != None:
			self.extract(content)
	
	def __repr__(self):
		return f"{self.h:02.0f}:{self.min:02.0f}:{self.s:02.0f}.{self.cs:02.0f}"

	def fix(self):
		while self.cs < 0:
			self.cs += 100
			self.s -= 1
		while self.cs >= 100:
			self.cs -= 100
			self.s += 1
   
		while self.s < 0:
			self.s += 60
			self.min -= 1
		while self.s >= 60:
			self.s -= 60
			self.min += 1
   
		while self.min < 0:
			self.min += 60
			self.h -= 1
		while self.min >= 60:
			self.min -= 60
			self.h += 1

	def extract(self, content):
		i = 0; numb = 0
		while(content[i] != ":"): #Obtém hora
			numb = 10*numb + int(content[i])
			i += 1
		i += 1
		self.h = numb
		numb = 0
  
		while(content[i] != ":"): #Obtém minuto
			numb = 10*numb + int(content[i])
			i += 1
		i += 1
		self.min = numb
		numb = 0

		while(content[i] != "."): #Obtém segundo
			numb = 10*numb + int(content[i])
			i += 1
		i += 1
		self.s = numb
		numb = 0
  
		while(i < len(content)): #Obtém minuto
			numb = 10*numb + int(content[i])
			i += 1
		i += 1
		self.cs = numb
		numb = 0

	def __add__(self, other:int):
		res = Timestamp(f"{self!r}")
		res.cs += other
		res.fix()
		return res

	def __sub__(self, other:'Timestamp'):
		if isinstance(other, int):
			return self.__add__(-other)
		res = Timestamp(f"{self!r}")
		res.h -= other.h
		res.min -= other.min
		res.s -= other.s
		res.cs -= other.cs
		res.fix()
		return (res.cs + 100*res.s + 60*100*res.min + 60*60*100*res.h)

'''
Classe Audio
	- Possui um AudioFileClip, link do arquivo de audio, todos os takes desse aúdio em timestamps e um timestamp de duração (em cs)
	getTake() -> Retorna um timestamp do take de id requisitado
	getClip() -> Obtém um AudioClip de um take do vídeo
	cut() -> Obtém um subconjunto do vídeo em formato de AudioClip
	copy() -> Cria uma cópia do áudio
	mergeTakes() -> Unifica timestamps de takes consecutivos
	
	setDurations() -> Corrige as durações dos takes para se conectarem
'''
class Audio:
	def __init__(self, file:str, takes:list[Timestamp], setDurations = False):
		self.file = file #String com o link para o audio
		self.takes = takes #Lista de timestamps (>= 2)
		self.takeQt = len(takes) #Quantidade de divisões no áudio: [Início, Take1, ..., TakeN, Fim]
		self.duration = 0
		if setDurations:
			self.setDurations()
		for tk in self.takes:
			self.duration += tk.duration
		self.audio = MED.AudioFileClip(file).subclip(t_start="00:00:00.00",t_end=repr(Timestamp("00:00:00.00")+self.duration))
  
	def __repr__(self):
		res = "Audio [\n"
		for tk in self.takes:
			res += f"{tk!r} , {tk.duration/100}s\n"
		return (res + "]")

	def getTake(self, number:int = 0):
		return self.takes[number]

	def getClip(self, number:int = 0):
		if number < self.takeQt-1:
			return self.audio.subclip(t_start=repr(self.takes[number]),t_end=repr(self.takes[number+1]-1))
		return self.audio.subclip(t_start=repr(self.takes[number]))

	def cut(self, t0:int, tn:int = 0):
		return self.audio.subclip(t_start=repr(self.takes[t0]),t_end=repr(self.takes[tn-1]+self.takes[tn-1].duration))

	def copy(self):
		newTakes = []
		for tk in self.takes:
			newTakes.append(Timestamp(repr(tk),tk.duration))
		return Audio(self.file,newTakes,True)

	def mergeTakes(self, t0: int, tn:int = 0):
		if tn == 0:
			tn = self.takeQt
   
		newAudio = self.copy()
		for i in reversed(range(t0,tn-1)):
			newAudio.takes[i].duration += newAudio.takes[i+1].duration
			newAudio.takes.pop(i+1)
		return newAudio

	def eraseTakes(self, t0: int, tn:int = 0): #Apaga os takes
		if tn == 0:
			tn = t0+1

		newAudio = self.copy()
		accumulatedDuration = newAudio.takes[tn] - newAudio.takes[t0]
		takesErased = tn-t0
   
		for i in range(tn,self.takeQt):
			newAudio.takes[i] = newAudio.takes[i] - accumulatedDuration
		newAudio.takeQt -= takesErased
		newAudio.audio = newAudio.audio.cutout(repr(newAudio.takes[t0]),repr(newAudio.takes[tn]))
		del newAudio.takes[t0:tn]
			
		return newAudio
  
	def setDurations(self):
		for i in range(self.takeQt-1): #Não corrige somente o último, pois já deve estar corrigido
			self.takes[i].duration = self.takes[i+1] - self.takes[i]

'''
Classe Text
	- Representa um texto: recebe uma mensagem e guarda um ImageClip com o texto
	setPosition() -> Altera a posição do texto na tela
	setDuration() -> Altera a duração do texto na tela
'''

def makeText(message):
	if not os.path.exists(os.path.join(textPath,f"{message.replace(" ","_").replace(":","")}.png")):
		subprocess.run(
			["python", "createText.py"],
			input=f"{message}",
			text=True,  #Garante envio de texto, e não bytes
		)
	return MED.ImageClip(os.path.join(textPath,f"{message.replace(" ","_").replace(":","")}.png"))

'''
Classe Scene:
	- Conjunto das imagens/gifs e textos que compõem uma tela
	set_duration() -> Altera a duração dos componentes da tela
	compose() -> Retorna um composite video clip com todos os elementos unidos
	applytransition() -> Aplica uma transição a uma cena
'''
class Scene:
	def __init__(self, sceneType):
		self.elements = []
		self.texts = []
		self.transitionApplied = TRANSITION_NONE
		self.type = sceneType
  
	def setDuration(self, duration):
		for i in range(len(self.elements)):
			self.elements[i] = self.elements[i].set_duration(duration)
		for i in range(len(self.texts)):
			self.texts[i] = self.texts[i].set_duration(duration)

	def compose(self, nextFrame = None, prevTransition = TRANSITION_NONE, generatedTransition = TRANSITION_NONE):
		selectedObjects = []
		for el in self.elements:
			selectedObjects.append(el)
		for tx in self.texts:
			selectedObjects.append(tx)
		res = MED.CompositeVideoClip(selectedObjects, size=(1080,1920))
		global currentSceneDuration
		currentSceneDuration = self.elements[0].duration
 
		if self.transitionApplied == TRANSITION_RANDOM:
			self.transitionApplied = generatedTransition
   
			if (prevTransition & TRANSITION_FADE) and self.type != SCENE_INITIAL:
				res = res.fadein(9*FRAME_60DURATION)
			if (self.transitionApplied & TRANSITION_FADE) and self.type != SCENE_FINAL:
				res = res.fadeout(9*FRAME_60DURATION)

			if (prevTransition & TRANSITION_ZOOM_IN) and self.type != SCENE_INITIAL:
				res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 5*FRAME_60DURATION,
				0.38, FXSTAGE_START))
			if (self.transitionApplied & TRANSITION_ZOOM_IN) and self.type != SCENE_FINAL:
				res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 5*FRAME_60DURATION,
				0.38, FXSTAGE_END))

			if (prevTransition & TRANSITION_ZOOM_OUT) and self.type != SCENE_INITIAL:
				res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 4*FRAME_60DURATION,
				-0.38, FXSTAGE_START))
			if (self.transitionApplied & TRANSITION_ZOOM_OUT) and self.type != SCENE_FINAL:
				res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 4*FRAME_60DURATION,
				-0.38, FXSTAGE_END))
		
			if (prevTransition & TRANSITION_ROTATIONS) != 0 and (self.type != SCENE_INITIAL):
				res = res.fl(lambda f,t: fx_rotate(f,t,self.elements[0].duration,5*FRAME_60DURATION,
				FXSTAGE_START,convertR[prevTransition & TRANSITION_ROTATIONS]))
			if (self.transitionApplied & TRANSITION_ROTATIONS) != 0 and (self.type != SCENE_FINAL):
				res = res.fl(lambda f,t: fx_rotate(f,t,self.elements[0].duration,5*FRAME_60DURATION,
				FXSTAGE_END,convertR[self.transitionApplied & TRANSITION_ROTATIONS]))
		
			
			if (self.transitionApplied & TRANSITION_SLIDES) != 0 and (self.type != SCENE_FINAL):
				res = res.fl(lambda f,t: fx_slide(f,t,self.elements[0].duration,7*FRAME_60DURATION,convertS[self.transitionApplied & TRANSITION_SLIDES],nextFrame))
	
		else:
			if (self.transitionApplied & TRANSITION_FADE):
				if self.type != SCENE_INITIAL:
					res = res.fadein(9*FRAME_60DURATION)
				if self.type != SCENE_FINAL:
					res = res.fadeout(9*FRAME_60DURATION)

			if (self.transitionApplied & TRANSITION_ZOOM_IN):
				if self.type != SCENE_INITIAL:
					res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 5*FRAME_60DURATION,
					0.38, FXSTAGE_START))
				if self.type != SCENE_FINAL:
					res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 5*FRAME_60DURATION,
					0.38, FXSTAGE_END))

			if (self.transitionApplied & TRANSITION_ZOOM_OUT):
				if self.type != SCENE_INITIAL:
					res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 4*FRAME_60DURATION,
					-0.38, FXSTAGE_START))
				if self.type != SCENE_FINAL:
					res = res.fl(lambda f,t: fx_zoom(f,t,self.elements[0].duration, 4*FRAME_60DURATION,
					-0.38, FXSTAGE_END))
		
			if (self.transitionApplied & TRANSITION_ROTATIONS) != 0:
				convert = {TRANSITION_ROTATE_L: 1, TRANSITION_ROTATE_R: -1}
				if self.type != SCENE_INITIAL:
					res = res.fl(lambda f,t: fx_rotate(f,t,self.elements[0].duration,5*FRAME_60DURATION,
					FXSTAGE_START,convert[self.transitionApplied & TRANSITION_ROTATIONS]))
				if self.type != SCENE_FINAL:
					res = res.fl(lambda f,t: fx_rotate(f,t,self.elements[0].duration,5*FRAME_60DURATION,
					FXSTAGE_END,convert[self.transitionApplied & TRANSITION_ROTATIONS]))
		
			if (self.transitionApplied & TRANSITION_SLIDES) != 0:
				convert = {TRANSITION_SLIDE_L: 0, TRANSITION_SLIDE_U: 1, TRANSITION_SLIDE_R: 2, TRANSITION_SLIDE_D: 3}
				if self.type != SCENE_FINAL:
					res = res.fl(lambda f,t: fx_slide(f,t,self.elements[0].duration,7*FRAME_60DURATION,convert[self.transitionApplied & TRANSITION_SLIDES],nextFrame))

		return res, self.transitionApplied

	def applyTransition(self, type):
		self.transitionApplied += type * (1 - (self.transitionApplied & type))

'''
Classe Duel
	- Conjunto das imagens/gifs e textos que compõem um dos tipos de tela: A vs B
'''
class Duel(Scene):
	def __init__(self, element1, element2, text1, text2 = "", text3 = "", sceneType = SCENE_NORMAL):
		super().__init__(sceneType)
		self.texts = [makeText(text1).set_position(('center',912))]
		if text2 != "":
			self.texts.append(makeText(text2).set_position(('center',912 - 400)))
			self.texts.append(makeText(text3).set_position(('center',912 + 400)))
   
		if element1[1] == TYPE_IMAGE:
			el1 = MED.ImageClip(os.path.join(imagesPath,f"{element1[0]}")).set_position((0,0)).resize(newsize=(1080,960))
		else:
			el1 = MED.VideoFileClip(os.path.join(gifsPath,f"{element1[0]}")).set_position((0,0)).resize(newsize=(1080,960))
   
		if element2[1] == TYPE_IMAGE:
			el2 = MED.ImageClip(os.path.join(imagesPath,f"{element2[0]}")).set_position((0,960)).resize(newsize=(1080,960))
		else:
			el2 = MED.VideoFileClip(os.path.join(gifsPath,f"{element2[0]}")).set_position((0,960)).resize(newsize=(1080,960))
   
		self.elements = [el1, el2]

'''
Classe Victory
	- Conjunto de uma imagem e textos que formam um dos tipos de tela: A wins
'''
class Victory(Scene):
	def __init__(self, element, name, score = "", sceneType = SCENE_NORMAL):
		super().__init__(sceneType)
		self.texts = [makeText(name).set_position(('center',912))]
		if score != "":
			self.texts.append(makeText(score))
			self.texts[0] = self.texts[0].set_position(('center',832))
			self.texts[1] = self.texts[1].set_position(('center',992))
   
		if element[1] == TYPE_IMAGE: #É imagem
			self.elements = [MED.ImageClip(os.path.join(imagesPath,f"{element[0]}")).set_position((0,0)).resize(newsize=(1080,1920))]
		else: #É gif
			self.elements = [MED.VideoFileClip(os.path.join(gifsPath,f"{element[0]}")).set_position((0,0)).resize(newsize=(1080,1920)).loop()]

'''
Classe FullVideo
- Possui uma lista de cênas e uma música, unindo elas em um único vídeo de forma a processar facilmente todas as alterações
'''   
class FullVideo:
	def __init__(self, char1, char2, audio:Audio, stats, random_stats, transition):
		self.scenes = []
		self.random = random_stats
		self.stats = stats
		self.char1 = char1
		self.char2 = char2
		self.audio = audio
		self.transition = transition
		self.videoName = f'edit_{len(os.listdir(outputPath))}.mp4'
		self.makeScenes()
		self.updateScenes()
  
	def makeScenes(self):
		self.rounds = (self.audio.takeQt - 3)//2

		#Tela inicial
		self.scenes.append(Duel(
			element1 = [self.char1[1], self.char1[0]], element2 = [self.char2[1],self.char2[0]],
	  		text1 = "vs", text2 = self.char1[3], text3 = self.char2[3],
			sceneType = SCENE_INITIAL
		))
  
		#Rounds
		x1 = 0; x2 = 0
		for i in range(self.rounds):
			self.scenes.append(Duel(
				element1 = [self.char1[1],self.char1[0]], element2 = [self.char2[1],self.char2[0]],
				text1 = self.stats[i]
			))

			firstWins = (self.char1[5][i] > self.char2[5][i] and self.random == False) or (self.random == True and random.randint(1,100000) > random.randint(1,100000))
			if firstWins:
				x1 += 1
				self.scenes.append(Victory(
					element = [self.char1[2],self.char1[0]],
					name = self.char1[3], score = f"{x1} - {x2}"
				))
			else:
				x2 += 1
				self.scenes.append(Victory(
					element = [self.char2[2],self.char2[0]],
	 				name = self.char2[3], score = f"{x1} - {x2}"
				))

		#Finalização
		self.scenes.append(Duel(
	  		element1 = [self.char1[1],self.char1[0]], element2 = [self.char2[1],self.char2[0]],
			text1 = "Vencedor:"
		))
		difs = ["Empate","Insane Diff","High Diff","Mid Diff","Low Diff","No Diff","Neg Diff"]
		if x1 > x2:
			self.scenes.append(Victory(
	   			element = [self.char1[2],self.char1[0]],
		  		name = self.char1[3], score = difs[min(abs(x1-x2),6)], sceneType= SCENE_FINAL
			))
		elif x1 < x2:
			self.scenes.append(Victory(
	   			element = [self.char2[2],self.char2[0]],
		  		name = self.char2[3], score = difs[min(abs(x1-x2),6)], sceneType= SCENE_FINAL
			))
		else:
			self.scenes.append(Duel(
	   			element1 = [self.char1[1],self.char1[0]], element2 = [self.char2[1],self.char2[0]],
				text1 = "Empate", sceneType = SCENE_FINAL
			))
		
	def updateScenes(self):
		for i,sc in enumerate(self.scenes):
			sc.setDuration(0.01*(self.audio.takes[i].duration))
			sc.applyTransition(self.transition)
   
	def createVideo(self):
		compositions = []
		nextFrame = None
		transitionUsed = TRANSITION_NONE
		for sc in reversed(self.scenes):
			newTransition = randomTransition() #Usada apenas se transitionApplied é TRANSITION_RANDOM
			compositeRes, transitionUsed = sc.compose(nextFrame,newTransition,transitionUsed)
			compositions.append(compositeRes)
   
			nextFrame = compositions[-1].get_frame(0)
			transitionUsed = newTransition

		compositions = list(reversed(compositions))
		resClip = MED.concatenate_videoclips(compositions).set_audio(self.audio.cut(0,len(compositions)))

		for tx in os.listdir(textPath): #Limpar pasta texts
			os.remove(os.path.join(textPath,tx))
   
		return resClip, os.path.join(outputPath,self.videoName)
