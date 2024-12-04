# AutoVersus
Projeto que usa a bibliotecas Moviepy, OpenCV, Cairo e Pillow que é capaz de gerar facilmente vídeos do formato Personagem vs Personagem com bom nível de customização

## Instruções
### Personagens
- Os personagens devem ter imagens ou gifs de "estado padrão" e "vitória" armazenados em /images ou /gifs
- Deve-se escolher alguma modalidade de status e criar seus status correspondentes a essa modalidade, conferível na classe StatsOrdering em objects.py
- Deve-se criar uma instância do personagem como um método da classe Characters de objects.py
- Depois disso, basta chamar o seu método no lugar adequado em main.py, da mesma forma que está presente agora

### Músicas
- Cada música deve ter seu trecho armazenado em /audios com o nome correspondente
- Cada audio deve ter um método correspondente na classe AudioCollection de objects.py, em que os Timestamps representam início de cada 'take', definido como um momento em que uma determinada tela estará presente na tela (por exemplo, um take possível poderia conter o status força e as imagens dos dois personagens)

### Configurações
- Você pode alterar as transições, alterar para status aleatórios ou coisas do gênero alterando os métodos chamados por main.py nos parametros de FullVideo()

### Gerar o vídeo
- Basta executar o script main.py, e sua edit começará a ser gerada em /videos