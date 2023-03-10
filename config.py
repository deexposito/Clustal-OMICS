import random, string

class DevelopmentConfig():
    DEBUG=True
    SECRET_KEY = 'abcabcabcabcabcabc'

class ProducctionConfig():
    DEBUG=True
    SECRET_KEY = ''.join(random.choices(string.ascii_letters, k=30))

config = {
    "development": DevelopmentConfig,
    "producction": ProducctionConfig
}

# IMPORTANT PREFIX should start with an slash ("/") character
PREFIX = "/u195257/clustalo"
