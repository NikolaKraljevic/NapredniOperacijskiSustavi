from Crypto.Cipher import AES,DES3,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import  pad,unpad
from Crypto.Hash import SHA3_256,SHA3_512
from base64 import b64encode,b64decode
from sys import stdin
from base64 import b64encode,b64decode
BLOCK_SIZE = 64

#UNOS PORUKE KOJU ZELITE KRIPTIRATI
data = open('datoteka.txt')
#UPISITE VELICINE KLJUCEVA
#OVO JE ZA SIMETRICNI KLJUC U DECIMALONOJ BAZI
print("Upisite velicinu u bitovima simetricnog kljuca u decimalnoj bazi ili upisite simetrican kljuc")
Simkljuc = ''
key1size = stdin.readline()
try:
    Skljuc = int(key1size)
    Simkljuc = get_random_bytes(Skljuc/8)

except:
    Simkljuc = key1size.strip('\n')
#UPISITE VELICINU KLJUCA PRIMATELJA I POSILJATELJA
print("Upisite velicinu kljuca primatelja u bitovima u decimalnoj bazi")
key2size =  int(stdin.readline().strip('\n'))
print("Upisite velicinu kljuca posiljatelja u bitovima u decimalnoj bazi")
key3size =  int(stdin.readline().strip('\n'))
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
#ODABERITE MOD SIMETRICNOG KRIPTOSUSTAVA
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
#ODABERITE ASIM KRIPTOSUSTAV TJ. VELICINU
print('Upisite 1 za SHA3_256 inace bilo sta SHA3_512')
typeHas = stdin.readline().strip('\n')
hesh = ''
if(typeHas == '1'):
    hesh = SHA3_256
else:
    hesh = SHA3_512

#GENERIRAMO KLJUC JAVNI I PRIVATNI PRIMATELJA
RecKey = RSA.generate(key2size)
binPrivKey = RecKey.exportKey('DER')
binPubKey =  RecKey.publickey().exportKey('DER')
privKeyObj = RSA.importKey(binPrivKey)
pubKeyObj =  RSA.importKey(binPubKey)
#GENERIRAMO KLJUC JAVNI I PRIVATNI POSILJATELJA
SenKey = RSA.generate(key3size)
binPrivKey2 = SenKey.exportKey('DER')
binPubKey2 =  SenKey.publickey().exportKey('DER')
privKeyObj2 = RSA.importKey(binPrivKey2)
pubKeyObj2 =  RSA.importKey(binPubKey2)
#C1 C2 C3 I OSTALE OZNAKE SU UZETE IZ KNJIGE
#RACUNAMO C1
#IZVORNI TEKST KRIPTIRAMO SIMETRICNIM KLJUCEM
cipher = Sim.new(Simkljuc,SimC)
input = pad(data.read(),64)
C1 = cipher.encrypt(input)
#RACUNAMO C2
#JAVNIM KLJUCEM POSILJATELJA KRIPTIRAMO TAJNI KLJUC
cipher = PKCS1_OAEP.new(pubKeyObj)
C2 = cipher.encrypt(Simkljuc)
#RACUNAMO C3
#IZRADIMO SAZETAK OD C1 I C2 I KRIPTIRAMO GA KLJUCEM
poruka = C1+C2
hash_object = hesh.new(poruka)
cipher = PKCS1_OAEP.new(pubKeyObj2)
kul =(bytes(hash_object.hexdigest()))
C3 = cipher.encrypt(kul)

#DEKRIPTIRAMO C2 DA DOBIJEMO SIMETRICNI KLJUC
cipher = PKCS1_OAEP.new(privKeyObj)
KljucZaDek = cipher.decrypt(C2)
#DEKRIPTIRAMO C1 SA SIMETRICNIM KLJUCEM DOBIVENIM OD DEKRIPCIJE C2
# I DOBIVAMO PORUKU
cipher = Sim.new(KljucZaDek,SimC)
ciphertext = cipher.decrypt(C1)
encoded = b64encode(str(ciphertext))

rjesenjeDigitalneOmotnice = unpad(ciphertext,64)
#DEKRIPTIRAMO C3 I USPOREDUJEMO JE LI S DOBIVEN JEDNAK HASH FJI POSILJATELJA
cipher3 = PKCS1_OAEP.new(privKeyObj2)
S = cipher3.decrypt(C3)
#PROVJERAVAMO JE LI SAZETAK ISTI TJ PROVJERAVAMO JE LI DIGITALNI PECAT DIGITALNO
#POTPISANA DIGITALNA OMOTNICA
print(S == kul)
with open('digitalnipecat.txt', 'w') as f:
        f.write('''---BEGIN OS2 CRYPTO DATA---
Description:
    Stamp
File name:
    datoteka.txt
Method:
    {simetricni}
    {asimetricni}
Key length:
    {sym_key_len}
    {asym_key_len}
Hash data:
    {data}
Envelope crypt key:
    {sym_key}
---END OS2 CRYPTO DATA---
'''.format(simetricni=Sim2, asimetricni='RSA',
                   sym_key_len=hex(Skljuc), asym_key_len=hex(key2size),
                   data=hash_object.hexdigest(), sym_key=b64encode(str(Simkljuc))))