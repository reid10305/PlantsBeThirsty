class Plant():
    ''' Plant object. Each plant in the chain is represented as 
     one of these objects. '''

    species = ""
    nickname = ""
    size = 0


    # constructor
    def __init__(self, species, nickname, size):
        self.species = species
        self.nickname = nickname
        self.size = size
