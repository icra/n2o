import time
import sys
import lectura as Lec
import registra as Reg

'''Volum inicial campanes (L)'''
V1=0; V2=0; V3=0; V4=0;

#primera lectura per saber estat pols cabal
dades=Lec.lectura()
C1=dades['C1']
C2=dades['C2']
C3=dades['C3']
C4=dades['C4']

#esborra 4 linies
for i in range(4): sys.stdout.write("\033[F\033[K")

while True:

	dades=Lec.lectura() #json

	if(dades['C1']!=C1): V1+=10
	if(dades['C2']!=C2): V2+=10
	if(dades['C3']!=C3): V3+=10
	if(dades['C4']!=C4): V4+=10

	dades['V1']=V1
	dades['V2']=V2
	dades['V3']=V3
	dades['V4']=V4

	C1=dades['C1']
	C2=dades['C2']
	C3=dades['C3']
	C4=dades['C4']

	Reg.registra(dades)
	break
	time.sleep(5)