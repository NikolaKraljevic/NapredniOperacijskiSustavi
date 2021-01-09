from Crypto.Cipher import AES,DES3,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Random.random import  getrandbits
from Crypto.PublicKey import RSA
from base64 import b64encode,b64decode
from Crypto.Util.Padding import  pad,unpad
from sys import stdin
BLOCK_SIZE = 64
#UNOS PORUKE KOJU ZELITE KRIPTIRATI
data = open('datoteka.txt')
#UPISITE VELICINE KLJUCEVA
print("Upisite velicinu simetricnog kljuca u decimalnoj bazi u bitovima ili upisite simetrican kljuc")
Simkljuc = ''
key1size = stdin.readline()
try:
    Skljuc = int(key1size)
    Simkljuc = get_random_bytes(Skljuc/8)
    print(type(Simkljuc))
    kljuc = b64encode(str(Simkljuc))
except:

    Simkljuc = key1size.strip('\n')
print("Upisite velicinu asimetricnog kljuca primatelja u bitovima u decimalnoj bazi")
key2size =  int(stdin.readline().strip('\n'))
#ODABERITE SIMETRICNI KRIPTOSUSTAV
print("Upisite 1 za AES ili bilo sta ostalo za 3-DES")
typeSimetric = stdin.readline().strip('\n')
Sim = ''
Sim2 = ''
if (typeSimetric == '1'):
    Sim = AES
    Sim2 = 'AES'
else:
    Sim = DES3
    Sim2 = 'DES3'

print("Stisnite 1 za ECB ili bilo sta ostalo za CBC")
typeSim = stdin.readline().strip('\n')
SimC = ''
if (typeSim == '1'):
    if Sim2 == 'AES':
        SimC = AES.MODE_ECB
    else:
        SimC = DES3.MODE_ECB
else:
    if Sim2 == 'AES':
        SimC = AES.MODE_CBC
    else:
        SimC = DES3.MODE_CBC
#GENERIRAMO JAVNI I PRIVATNI KLJUC PRIMATELJA
SenderKey = RSA.generate(key2size)
binPrivKey = SenderKey.exportKey('DER')
binPubKey =  SenderKey.publickey().exportKey('DER')
privKeyObj = RSA.importKey(binPrivKey)
pubKeyObj =  RSA.importKey(binPubKey)
#KRIPTIRAMO PORUKU SIM KLJUCEM
cipher = Sim.new(Simkljuc,SimC)
input = pad(data.read(),64)
C1 = cipher.encrypt(input)
#JAVNIM KLJUCEM PRIMATELJA KRIPTIRAMO SIMETRICNI KLJUC
cipher = PKCS1_OAEP.new(pubKeyObj)
C2 = cipher.encrypt(Simkljuc)
rj = b64encode(str(C2))
print(rj)
cipher = PKCS1_OAEP.new(privKeyObj)
KljucZaDek = cipher.decrypt(C2)
cipher = Sim.new(KljucZaDek,SimC)
ciphertext = cipher.decrypt(C1)
print(unpad(ciphertext,64))
with open('digitalnaomotnica.txt', 'w') as f:
        f.write('''---BEGIN OS2 CRYPTO DATA---
Description:
    Envelope
File name:
    datoteka.txt
Method:
    {simetricni}
    {asimetricni}
Key length:
    {sym_key_len}
    {asym_key_len}
Envelope data:
    {data}
Envelope crypt key:
    {sym_key}
---END OS2 CRYPTO DATA---
'''.format(simetricni=Sim2, asimetricni='RSA',
                   sym_key_len=hex(Skljuc), asym_key_len=hex(key2size),
                   data=rj, sym_key=kljuc))