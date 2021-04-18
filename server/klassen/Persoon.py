class Persoon:
    def __init__(self, name, nickname, email):
        self.name = str(name)
        self.nickname = str(nickname)
        self.email = str(email)

    def __eq__(self, other):
        return (self.name == other.name) and (self.nickname == other.nickname) and (self.email == other.email)


