import json

from M2Crypto.EVP import Cipher
import base64
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS

def alert(msg):
    return '<script type = "text/javascript"> alert("{}");location.href="/netdisk/"</script>'.format(msg)



def encrypt_3des(key, text):
    # encryptor = Cipher(alg='des_ede3_ecb', key=key, op=1, iv='\0'*16)
    encryptor = Cipher(alg='des_ede3_cbc', key=key, op=1, iv='01234567')
    s = encryptor.update(text)
    return s+ encryptor.final()

def decrypt_3des(key, text):
    decryptor = Cipher(alg='des_ede3_cbc', key=key, op=0, iv='01234567')
    s= decryptor.update(text)
    return s + decryptor.final()

if __name__ == '__main__':
    key = 'sr$*)(ruan$@lx100$#365#$'
    text = '1'
    encrypt_text = encrypt_3des(key, text)
    decrypt_test = decrypt_3des(key,encrypt_text)
    print (encrypt_text,decrypt_test)
    print (base64.b64encode(encrypt_text))