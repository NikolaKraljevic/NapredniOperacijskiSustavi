from Crypto.Cipher import AES,DES3,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.Padding import  pad,unpad
from Crypto.Hash import SHA3_256,SHA3_512
from base64 import b64encode,b64decode
from sys import stdin
BLOCK_SIZE = 64
#UNOS PORUKE KOJU ZELITE KRIPTIRATI
data = open('datoteka.txt')
#UPISITE VELICINE KLJUCEVA
print("Upisite velicinu kljuca posiljatelja u bitovima u decimalnoj bazi")
key1size =  int(stdin.readline().strip('\n'))
print("Upisite velicinu kljuca primatelja u bitovima u decimalnoj bazi")
key2size =  int(stdin.readline().strip('\n'))
#UPISITE FJU HASHIRANJA
print('Upisite 1 za SHA3_256 inace bilo sta SHA3_512')
typeHas = stdin.readline().strip('\n')
hashstr = ''
hesh = ''
if(typeHas == '1'):
    hesh = SHA3_256
    hashstr = 'SHA3_256'

else:
    hesh = SHA3_512
    hashstr = 'SHA3_512'

#GENERIRAMO KLJUC JAVNI I PRIVATNI PRIMATELJA
RecKey = RSA.generate(key2size)
binPrivKey = RecKey.exportKey('DER')
binPubKey =  RecKey.publickey().exportKey('DER')
privKeyObj = RSA.importKey(binPrivKey)
pubKeyObj =  RSA.importKey(binPubKey)
#GENERIRAMO KLJUC JAVNI I PRIVATNI POSILJATELJA
SenKey = RSA.generate(key1size)
binPrivKey2 = SenKey.exportKey('DER')
binPubKey2 =  SenKey.publickey().exportKey('DER')
privKeyObj2 = RSA.importKey(binPrivKey2)
pubKeyObj2 =  RSA.importKey(binPubKey2)
#POTPISUJUEMO HASHIRANU PORUKU PRIVATNIM KLJUCEM POSILJATELJA
hash_object = hesh.new(data.read())
cipher = PKCS1_OAEP.new(privKeyObj2)
signature = PKCS1_v1_5.new(privKeyObj2).sign(hash_object)
#S JAVNIM KLJUCEM POSILJATELJA PROVJERAVAMO JE LI ON POTPISO TAJ PODATAK
#AKO JE ISPISEMO POTPIS JE VALJAN INACE CE IZNIMINKA IZBACITI DA JE PODMETNUTA PORUKA
try:
    PKCS1_v1_5.new(pubKeyObj2).verify(hash_object,signature)
    print("Potpis je valjan")
except:
    print("Potpis je namjesten,tj nije valjan")

with open('digitalniPotpis.txt', 'w') as f:
        f.write('''---BEGIN OS2 CRYPTO DATA---
Description:
    Signature
File name:
    datoteka.txt
Method:
    {simetricni}
    {asimetricni}
Key length:
    {sym_key_len}
    {asym_key_len}

Signature:
    {sym_key}
---END OS2 CRYPTO DATA---
'''.format(simetricni=hashstr, asimetricni='RSA',
                   sym_key_len=hex(key2size), asym_key_len=hex(key2size),
                   sym_key=b64encode(str(signature))))
