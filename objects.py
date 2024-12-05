from classes import (
	TYPE_GIF, TYPE_IMAGE, STAT_COMBAT, STAT_INTELLECT, #Constantes
	Timestamp, Audio, #Classes
	audiosPath, #Diretórios
	os #Bibliotecas
)

class StatsOrdering:
	def Intellect(self):
		return [
			"Experiência",
			"Resultados",
			"Memória",
			"Raciocínio",
			"Talento",
   
			"Esforço",
			"Motivação",
			"Disciplina",
			"Criatividade",
			"Liderança",
   
			"Colaboração",
			"Confiança",
			"Versatilidade",
			"Potencial"
		]
	def Combat(self):
		return [
			"Força",
			"Velocidade",
			"Resistência",
			"Durabilidade",
			"Reflexos",
   
			"Precisão",
			"Inteligência",
			"QI em Batalha",
			"Habilidades",
			"Antecipação",
   
			"Letalidade",
			"Talento",
			"Evolução",
			"Potencial"
		]

class Characters:
	def BesouroMahoraga(self):
		return [
			TYPE_IMAGE,
			"besouro_mahoraga.png",
			"win_besouro_mahoraga.png",
			"Besouro Mahoraga",
			STAT_COMBAT,
			[
				7500,18000,35000,97575,1460,
				3440,1320,19000,160160,900,
				1050,199,1460390,615000
			]
		]
  
	def HamoodHabibi(self):
		return [
			TYPE_GIF,
			"hamood_habibi.gif",
			"win_hamood_habibi.gif",
			"Hamood Habibi",
			STAT_COMBAT,
			[
    			17800,34000,21000,40000,24333,
				175,9360,17000,75443,15015,
				17000,9550,8775,30000
       		]
		]
  
	def Ragna(self):
		return [
			TYPE_GIF,
			"ragna.gif",
			"win_ragna.gif",
			"Ragna",
			STAT_COMBAT,
			[
    			417800,33560,121000,90900,133566,
				21175,7444,11030,45253,26012,
				19303,15,43775,57000
       		]
		]

class AudioCollection:
	def WeLive(self):
		return Audio(
			os.path.join(audiosPath,"WeLiveWeLove.mp3"),	
			[
				Timestamp('00:00:00.00'),
				Timestamp('00:00:07.14'),
				Timestamp('00:00:07.63'),
				Timestamp('00:00:08.08'),
				Timestamp('00:00:08.56'),
				Timestamp('00:00:09.03'),
				Timestamp('00:00:09.49'),
				Timestamp('00:00:09.96'),
				Timestamp('00:00:10.41'),
				Timestamp('00:00:10.90'),
				Timestamp('00:00:11.35'),
				Timestamp('00:00:11.83'),
				Timestamp('00:00:12.28'),
				Timestamp('00:00:12.76'),
				Timestamp('00:00:13.22'),
				Timestamp('00:00:13.70'),
				Timestamp('00:00:14.17'),
				Timestamp('00:00:14.63'),
				Timestamp('00:00:15.11'),
				Timestamp('00:00:15.58'),
				Timestamp('00:00:16.05'),
				Timestamp('00:00:16.52'),
				Timestamp('00:00:16.99'),
				Timestamp('00:00:17.45'),
				Timestamp('00:00:17.91'),
				Timestamp('00:00:18.37'),
				Timestamp('00:00:18.86'),
				Timestamp('00:00:19.31'),
				Timestamp('00:00:19.80'),
				Timestamp('00:00:20.29'),
				Timestamp('00:00:21.30',(Timestamp('00:00:22.50') - Timestamp('00:00:21.30'))),
			],
			True
		)

	def DontLike(self):
		return Audio(
			os.path.join(audiosPath,"KanyeWestDontLike.mp3"),
			[
				Timestamp('00:00:00.00'),
				Timestamp('00:00:04.35'),
				Timestamp('00:00:05.33'),
				Timestamp('00:00:06.59'),
				Timestamp('00:00:07.69'),
				Timestamp('00:00:08.70'),
				Timestamp('00:00:09.70'),
				Timestamp('00:00:10.70'),
				Timestamp('00:00:11.85'),
				Timestamp('00:00:12.88'),
				Timestamp('00:00:13.90'),
				Timestamp('00:00:14.97'),
				Timestamp('00:00:16.04'),
				Timestamp('00:00:17.10'),
				Timestamp('00:00:21.26',(Timestamp('00:00:25.05') - Timestamp('00:00:21.26'))),
			],
			True
		)
  
	def miniWeLive(self):
		return Audio(
			os.path.join(audiosPath,"WeLiveWeLove.mp3"),	
			[
				Timestamp('00:00:00.00'),
				Timestamp('00:00:01.40'),
				Timestamp('00:00:02.50',(Timestamp('00:00:03.75') - Timestamp('00:00:02.50'))),
			],
			True
		)