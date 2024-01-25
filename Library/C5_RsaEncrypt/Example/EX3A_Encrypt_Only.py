import __init
from Library.C5_RsaEncrypt.rsa_Wrap import RSA_Class

#1. Create RSA object
RSA = RSA_Class(publicKeyPath="Library/C5_RsaEncrypt/Example/GKEY_public.pem")
MESSAGE = "HELLO LOTUS!"
print("1. Original message:", MESSAGE)
#3. Encrypt message
encryptData = RSA.encrypt(MESSAGE) #encrypt data
print("2. Encrypt message:",encryptData)
