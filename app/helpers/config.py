#config class keeps secure code

import os




class Config():
    #define a secret key to secure our DB. we use a random number of 256 bit seed
    SECRET_KEY = os.urandom(32)

    #jwt secret key

    JWT_SECRET_KEY = '2c780b69@870b$41e48f94&4f3a33141bed4$%'
    
    #print(JWT_SECRET_KEY) you can add your own Jwt secret key
    

   
