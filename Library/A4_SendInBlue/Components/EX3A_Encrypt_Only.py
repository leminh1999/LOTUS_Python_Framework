import __init
from Library.C5_RsaEncrypt.rsa_Wrap import RSA_Class

#1. Create RSA object
RSA = RSA_Class(publicKeyPath="Library/A4_SendInBlue/Components/SIB_public.pem")
#https://app.brevo.com/settings/keys/api (tranhuudung@gmail.com)
MESSAGE = "INPUT_SIB_API_KEY_HERE_THEN_RUN_THIS_SCRIPT.THEN_DELETE_API_KEY_IN_THIS_SCRIPT"
print("1. Original message:", MESSAGE)
#3. Encrypt message
encryptData = RSA.encrypt(MESSAGE) #encrypt data
print("2. Encrypt message:",encryptData)
