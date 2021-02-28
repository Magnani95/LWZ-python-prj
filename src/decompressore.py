from io import StringIO
from bitstring import *
import bitarray
import os


def decomprimi(filePath, verbose, remove):
	"""Decomprime un file tramite l'algoritmo LZW.
	Il tag <verbose> comunica informazioni su stout.
	il tag <remove> rimuove il file compresso dopo l'espansione"""

	if verbose == True:
		print("--Decompressione del file\t", filePath)

	if filePath[-2:]!='.Z':
		print("Errore. Il file non è del formato corretto\n\t"+filePath)
		return

	listaCodici=[]
	datiCompressi= BitStream(filename=filePath)

	lunghezzaParola=0
	lunghezzaParola= datiCompressi.read(8).uint
	#print("LUNGHEZZA PAROLA\t", lunghezzaParola)
	while True:
		try:
			codice=datiCompressi.read(lunghezzaParola).uint
			#print("CODICE:\t", codice)
		except ReadError:
			print("ATTENZIONE! il file ", filePath," non è un file compresso consistente.")
			return
		if(codice != 256):
			listaCodici.append(codice)
		else:
			break;

	#print("LISTA CODICI\n", listaCodici)

	# Build the dictionary.
	dict_size = 257
	dictionary = {i: chr(i) for i in range(dict_size-1)}

	# use StringIO, otherwise this becomes O(N^2)
	# due to string concatenation in a loop
	result = StringIO()
	w = chr(listaCodici.pop(0))
	result.write(w)
	for k in listaCodici:
		if k in dictionary:
			entry = dictionary[k]
		elif k == dict_size:
			entry = w + w[0]
		else:
			print("ERRORE: il file non è consistente e non può essere compresso:\t", filePath)
			return
		result.write(entry)

		# Add w+entry[0] to the dictionary.
		dictionary[dict_size] = w + entry[0]
		dict_size += 1

		w = entry

	#print("RISULTATO\n", result.getvalue())
	if filePath[-2:]=='.Z':
		outputPath= filePath[:-2]
	else:
		outputPath=filePath + '_uncompressed'

	with open(outputPath, 'w') as outputFile:
		outputFile.write(result.getvalue())
		if remove == True:
			os.remove(filePath)
			if verbose == True:
				print('Il file ', filePath,' è stato cancellato')

				
