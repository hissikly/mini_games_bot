class PlayWords:
    def __init__(self, guess_word, tries, us_id):
        self.word = guess_word
        self.field = ['_'] * len(guess_word)
        self.tries = tries
        self.us_id = str(us_id)
        self.errors = []

    def change_init(self, field, tries, guessed_letters, errors):
        self.field = field
        self.tries = tries
        self.errors = errors

    def count_tries(self):
        if self.tries > 0:
            self.tries -= 1
            return self.tries
        return self.word

    def update_field(self, letter):
        self.errors.append(letter)
        for i in range(len(self.word)):
            if letter.lower() == self.word[i]:
                self.field[i] = letter.lower()
                print(self.field)
        print(self.word)
        return ' '.join(self.field)

