import os, sys, math, random
from decimal import *
from bitarray import bitarray

'''
This isn't really encryption, but rather preprocessing on the plaintext
to prevent against distribution attacks.
'''
class DistributionConfidentialityScheme:

	def __init__(self):

		# Scaling bit size
		self.q = 6; 

		# Randomization bit size
		self.r = 8;


	def encrypt(self, plaintext):
	
		modified_plaintext = plaintext
		modification_bit_count = bin(0)[2:].zfill(self.q)
		
		if '.' in plaintext:
			modified_plaintext = plaintext.replace('.', '')
			modification_bit_count = bin(len(plaintext.split('.')[1]))[2:].zfill(self.q)

		random_bits = str(bin(random.randint(1,math.pow(2,self.r)))[2:].zfill(self.r))

		ciphertext = modified_plaintext + modification_bit_count + random_bits		

		return ciphertext

	def decrypt(self, ciphertext):
		
		non_random_ciphertext =  ciphertext[:len(ciphertext) - self.r]
		modified_plaintext = non_random_ciphertext[:len(non_random_ciphertext) - self.q]
		modification_bit_count = int(non_random_ciphertext[len(non_random_ciphertext) - self.q:],2)
		plaintext = modified_plaintext
		
		if not modification_bit_count == 0:
			plaintext = modified_plaintext[:-1*modification_bit_count] + '.' + modified_plaintext[-1*modification_bit_count:]
		
		return plaintext
		


dcs_instance = DistributionConfidentialityScheme()
plaintext = '1110100.0'
ciphertext = dcs_instance.encrypt(plaintext)
decrypted_plaintext = dcs_instance.decrypt(ciphertext)
print "plaintext: ", plaintext, "ciphertext: ", ciphertext, "decrypted_plaintext: ", decrypted_plaintext
