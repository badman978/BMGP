from jose import JWTError, jwt
from passlib.context import CryptContext


#defining the harshing algo(bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 

def hash(password:str):
    return pwd_context.hash(password)


def authentication(password, hash):
    return pwd_context.verify(password, hash)