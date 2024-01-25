import __init
from Library.C5_RsaEncrypt.rsa_Wrap import RSA_Class

#1. Create RSA object
RSA = RSA_Class()
MESSAGE = "HELLO LOTUS!"
print("1. Original message:", MESSAGE)
#2. Generate key pair 
RSA.generateKeyPair(filePrefix="key",saveDir="./") #generate key pair
print("2. Generate key pair success!")
#3. Encrypt message
encryptData = RSA.encrypt(MESSAGE) #encrypt data
print("3. Encrypt message:",encryptData)
#4. Decrypt message
decryptData = RSA.decrypt(encryptData) #decrypt data
print("4. Decrypt message:",decryptData)