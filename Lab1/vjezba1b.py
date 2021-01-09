from multiprocessing import Process, Pipe
import sys
import time
import random
import os

def filozofi(i,slusatelj,pisatelj,N):
	#Sudjelovanje na konferenciji
	random.seed(i)
	spavanjeprvo = random.randint(100,2000)
	time.sleep(spavanjeprvo/1000)
	vrijeme = time.localtime()
	#Filozof salje zahtjev za sjesti
	for k in range(N):
		if k!=i:
			pisatelj[k].send([i,vrijeme,'Zahtjev'])
		
	sporiji = []
	brzi = []
	poruka = 0
	#Pocetak protokola Ricarta i Agrawala
	#Primanje svih zahtjeva za sjedanje i razvrstavanje u brze i sporije
	for k in range((N-1)):
		Primio = slusatelj[i].recv()
		print('Filozof ' +str(i)+' je primio poruku: ' )
		print(Primio[0],Primio[2])
		salje = Primio[0]
		
		if vrijeme>Primio[1] or (vrijeme == Primio[1] and i>salje):
			brzi.append(salje)

		else:
			sporiji.append(salje)
	#Pustanje tj slanje odgovora svim procesa sa manjim T
	for z in brzi:
		pisatelj[z].send([i,vrijeme,'Odgovor'])
	#Cekanje odgovora svih procesa
	for k in range(N-1):
		Primio = slusatelj[i].recv()
		print('Filozof ' +str(i)+' je primio poruku: ' )
		print(Primio[0],Primio[2])

	print('Filozof ' +str(i) + ' je za stolom----------------------')
	time.sleep(3)
	print('Filozof ' +str(i) + ' je ustao sa stola----------------------')
	#Slanje poruka svim sporijim procesima
	for z in sporiji:
		
		pisatelj[z].send([i,vrijeme,'Odgovor'])
	#Ponovno sudjelovanje na konferenciji
	#Kraj Protokola
	random.seed(2*i)
	spavanjedrugo = random.randint(99,2001)
	time.sleep(spavanjedrugo/2000)	
	os._exit(0)


N = int(sys.stdin.readline())
slusatelj = []
pisatelj = []
#Rad pipeline za svakog filozofa
for i in range(N):
	listen,writer = Pipe()
	slusatelj.append(listen)
	pisatelj.append(writer)
#Inicijalizacija procesa i pozivanje funkcije filozovi
for i in range(N):
	if(os.fork()==0):
		filozofi(i,slusatelj,pisatelj,N)	







