import os
from struct import *
from bitstring import *
from math import log2, ceil

def comprimi(filePath,verbose,remove):
	"""Comprime un file tramite l'algoritmo LZW. Nel caso la compressione sia conveniente
	viene creato un file con lo stesso nome con estenzione '.Z'
	Il tag <verbose> comunica informazioni su stout.
	il tag <remove> rimuove il file originale se la compressione è conveniente"""

	if verbose == True:
		print('COMPRESSIONE DEL FILE:\t', filePath)

	dimensioneIniziale=os.path.getsize(filePath)

	file=open(filePath,mode='r')
	text=file.read()
	file.close()
	#Parte LZW
	dict_size=257
	END_VAL=dict_size-1
	dictionary = {chr(i): i for i in range(dict_size-1)}
	uncompressed= bytes(text, 'utf-8')

	w = ""
	result = []
	for c in uncompressed:
		#print("--CICLO--")
		#print("C:\t",c)
		#print("W:\t",w)
		wc = str(w) + str(chr(c))
		#print("WC:\t",wc)
		if wc in dictionary:
			#print("==indict")
			w = wc
		else:
			#print("!!else")
			result.append(dictionary[w])

			dictionary[wc] = dict_size
			dict_size += 1
			w = str(chr(c))
	if w:
		result.append(dictionary[w])

	result.append(256)

	#scrivere su file
	lunghezzaParola= ceil(log2(dict_size))
	datiCompressi = BitArray()
	datiCompressi.append(BitArray(uint=lunghezzaParola, length=8))
	for code in result:
		datiCompressi.append(BitArray(uint=code, length=lunghezzaParola))

	outputFilePath=filePath+'.Z'
	with open(outputFilePath, 'wb') as outputFile:
		datiCompressi.tofile(outputFile)

	dimenzioneFinale=os.path.getsize(outputFilePath)

	rapportoCompressione= dimenzioneFinale/dimensioneIniziale
	if verbose == True:
		print('--File:\t\t', filePath,'\nRapporto:\t',rapportoCompressione)
	if rapportoCompressione >= 1:
		os.remove(outputFilePath)
		if verbose == True:
			print('ATTENZIONE: la compressione non è vantaggiosa, non è stato creato nessun file')
	elif remove == True:
		os.remove(filePath)
		if verbose == True:
			print('Il file ', filePath,' è stato cancellato')

			
