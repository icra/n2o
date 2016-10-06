#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Mode manual per obrir i tancar vàlvules
'''
import serial
import envia as Env
import time
import processa as Pro
import sys

#nova connexió serial
try: ser=serial.Serial('/dev/ttyACM0',9600)
except: import virtual; ser=virtual.Serial()
print("Port serial: "+ser.port+". open: "+str(ser.isOpen())+" --> Ctrl-C per parar\n")

#---------------------------------------
#carrega "sequencia.txt"
with open("sequencia.txt") as f: linies = f.read().splitlines()
comandes=[]
for linia in linies:
	if linia is "": continue
	if linia[0] in ["O","T","E"]: comandes.append(linia)
#mostra les comandes carregades
print "Comandes programades: "+str(comandes)+"\n"
#---------------------------------------

#Volums inicials (el primer cop sumarem 10L)
V1=-10;V2=-10;V3=-10;V4=-10
#Estat pols inicial
C1=2;C2=2;C3=2;C4=2

def espera(tempsEspera):
	#ves comptant el volum mentre esperes
	#truc: fem aquest bucle "tempsEspera" vegades, i cada vegada dura 1 segon
	#de manera que durarà "tempsEspera" segons, i de mentres anirem comptant el volum
	global C1,C2,C3,C4,V1,V2,V3,V4
	tempsEspera=int(tempsEspera)
	lectures=0
	trama=""
	ser.flushInput()
	while True:
			c=ser.read()
			trama+=c
			if c is "F":
					try: 
							d=Pro.processa(trama) #saltarà si la trama és incorrecta
							trama=""
					except: 
							trama=""
							ser.flushInput()
							continue
			else:
					continue #continua afegint caracters a la trama

			#si som aquí vol dir que la trama és correcta
			#si l'estat del pols ha canviat, suma 10 L
			if(d['C1']!=C1): V1+=10
			if(d['C2']!=C2): V2+=10
			if(d['C3']!=C3): V3+=10
			if(d['C4']!=C4): V4+=10
			#update estat del pols
			C1=d['C1'];C2=d['C2'];C3=d['C3'];C4=d['C4'];
			#afegeix el volum a l'objecte "d"
			d['V1']=V1;d['V2']=V2;d['V3']=V3;d['V4']=V4

			#registra a la base de dades si el comptador està a zero
			if lectures is 0:
					try: Reg.registra(d)
					except: print("Error: Dades no registrades")

			#mostra el volum que anem comptant
			if lectures>0:
					print "Comptant Volum (L): "+str([V1,V2,V3,V4])

			#fi volta: sumem 1 lectura i esperem 1 segon
			lectures+=1
			time.sleep(1)
			if lectures > tempsEspera: break
			ser.flushInput()
	#final del temps d'espera

while True:
	for comanda in comandes:
		print comanda

		if comanda[0] in ["O","T"]: Env.envia(comanda,ser)
		elif comanda[0] is "E":     espera(comanda[1:])
		else: continue
