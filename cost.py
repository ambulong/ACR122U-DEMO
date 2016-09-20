#coding:utf-8
from smartcard.System import readers
from smartcard.util import toHexString
import random
import sys

if len(sys.argv) < 2:
	print "usage: cost.py $cost$"
	sys.exit()
	
r = readers()
print "Available readers:", r

reader = r[0]
print "Using:", reader

connection = reader.createConnection()
connection.connect()

#LOAD AUTHENTICATION KEYS A
COMMAND = [0xFF, 0x82, 0x00, 0x00, 0x06]
key = ['FF', 'FF', 'FF', 'FF', 'FF', 'FF'] #KEY A
for i in range(6):
	key[i] = int(key[i], 16)
COMMAND.extend(key)

data, sw1, sw2 = connection.transmit(COMMAND)
#print "Status words: %02X %02X" % (sw1, sw2)
if (sw1, sw2) == (0x90, 0x0):
	print "Status: Key A is loaded successfully to key #0."	
elif (sw1, sw2) == (0x63, 0x0):
	print "Status: Failed to load key."
	sys.exit()

#LOAD AUTHENTICATION KEYS B
COMMAND = [0xFF, 0x82, 0x00, 0x01, 0x06]
key = ['FF', 'FF', 'FF', 'FF', 'FF', 'FF'] #KEY B
for i in range(6):
	key[i] = int(key[i], 16)
COMMAND.extend(key)

data, sw1, sw2 = connection.transmit(COMMAND)
#print "Status words: %02X %02X" % (sw1, sw2)
if (sw1, sw2) == (0x90, 0x0):
	print "Status: Key B is loaded successfully to key #1."	
elif (sw1, sw2) == (0x63, 0x0):
	print "Status: Failed to load key."
	sys.exit()

#Block 04 Authentication A
COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x04, 0x60, 0x00]
data, sw1, sw2 = connection.transmit(COMMAND)
if (sw1, sw2) == (0x90, 0x0):
	print "Status: Decryption sector 0x04 using key #0 as Key A successful."
elif (sw1, sw2) == (0x63, 0x0):
	print "Status: Decryption sector 0x04 using key #0 as Key A failed."

#Block 04 Authentication B
COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x04, 0x61, 0x01]
data, sw1, sw2 = connection.transmit(COMMAND)
if (sw1, sw2) == (0x90, 0x0):
	print "Status: Decryption sector 0x04 using key #1 as Key B successful."
elif (sw1, sw2) == (0x63, 0x0):
	print "Status: Decryption sector 0x04 using key #1 as Key B failed."

#Read Block 0x04
COMMAND = [0xFF, 0xB0, 0x00, 0x04, 0x10]
data, sw1, sw2 = connection.transmit(COMMAND)
print "Block 0x04: "+ toHexString(data)
balance = 0
p = 3
#float("".join(chr(i) for i in data[0:6]))
for i in data[0:6]:
	balance += 10**p*i
	p = p-1
#cost = round(random.uniform(1, 10), 2)
cost = float(sys.argv[1])
print "花费: %.2f" % cost
if(cost > balance):
	print "余额: %.2f (余额不足)" % balance
	sys.exit()
else:
	balance = balance - cost
	print "余额: %.2f" % balance

#Update Block 0x04
balance = "%07.2f" % balance
COMMAND = [0xFF, 0xD6, 0x00, 0x04, 0x10]
for i in list(balance):
	if(i != '.'):
		COMMAND.append(int(i))
data, sw1, sw2 = connection.transmit(COMMAND)
if (sw1, sw2) == (0x90, 0x0):
	print "Status: Update sector 0x04 successful."
elif (sw1, sw2) == (0x63, 0x0):
	print "Status: Update sector 0x04 failed."

#Update Block 0x04: Charge Money 9999.99
#COMMAND = [0xFF, 0xD6, 0x00, 0x04, 0x10, 0x09, 0x09, 0x09, 0x09, 0x09, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
#data, sw1, sw2 = connection.transmit(COMMAND)
#if (sw1, sw2) == (0x90, 0x0):
#	print "Status: Update sector 0x04 successful."
#elif (sw1, sw2) == (0x63, 0x0):
#	print "Status: Update sector 0x04 failed."


print "End."
