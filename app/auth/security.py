from pwdlib import PasswordHash

pw_hash = PasswordHash.recommended()

def password_hash (password: str) :
    return pw_hash.hash(password)

def password_verify ( orginal: str,hashed: str) :
    return pw_hash.verify(orginal,hashed)