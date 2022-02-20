import requests, os

class App:
    def __init__(self):
        self.guess = ""
        self.correct_word = ""
        self.board = []
        self.turns = 6
        pass
    def get_word(self):
        req = requests.get("https://wordle-list.malted.dev/choice")
        if int(req.status_code) == 200:
            self.correct_word = req.json()["word"]
            self.fake_correct_word = self.correct_word
            return self.correct_word
        else:
            return -1
    def validate_word(self):
        req = requests.get(f"https://wordle-list.malted.dev/valid?word={self.guess}")
        if int(req.status_code) == 200:
            return req.json()["valid"]
        else:
            return -1
    def check_word(self):
        # 1 => correct letter correct position, 2 => correct letter wrong position, 3 => wrong letter wrong position
        self.results = []
        
        if self.guess.isalpha() and len(self.guess) == 5:
            for index in range(5):
                if self.guess[index] == self.fake_correct_word[index]:
                    self.results.append([1, self.guess[index]])
                    self.fake_correct_word[index] == " "
                elif self.guess[index] in self.fake_correct_word:
                    self.results.append([2, self.guess[index]])
                else:
                    self.results.append([3, self.guess[index]])
            return self.results
        else:
            return -1
    def printboard(self):
        # Example board: [#firstguess[[1, "a"], [2, "c"]]]
        # print(self.board)
        for guess in self.board:
            
            self.formattedguess = ""
            for letter in guess:
                if letter[0] == 1:
                    self.formattedguess += f"🟢[{letter[1]}] "
                elif letter[0] == 2:
                    self.formattedguess += f"🟡[{letter[1]}] "
                elif letter[0] == 3:
                    self.formattedguess += f"🔴[{letter[1]}] "
            print(self.formattedguess)
    def main(self):
        input("Welcome to the Wordle game! Enter your 5-letter guess. Press Enter to start. ")
        
        # Get a word from the server
        get_word_code = self.get_word()
        if get_word_code == -1:
            print("Error accessing the Wordle API. Please try again later.")
        os.system("cls")
        while True:
            
            if self.turns == 0:
                print("You ran out of turns. The word was: " + self.correct_word)
                exit()
            
            print("[ Wordle v1 by (mime-r) ]")
            self.printboard()
            self.guess = input(f"({self.turns}/6)> ")

            # Validate word
            validate_code = self.validate_word()
            if validate_code == -1:
                print("Error accessing the Wordle API. Please try again later.")
                exit(-1)
            elif validate_code == False:
                print("That word is not valid. Please try again.")
                continue
            
            # Check word - KIND OF UNECESSARY LMAO
            check_code = self.check_word()
            if check_code == -1:
                print("Word is not valid! Please try again.")
                continue
            else:
                self.board.append(check_code)
            
            if self.guess == self.correct_word:
                self.printboard()
                print(f"You won in {7-self.turns} guesses! The word was: " + self.correct_word)
                exit()

            if (self.turns-1) != 0:
                os.system("cls")
            self.turns -= 1
                
if __name__ == "__main__":
    app = App()
    app.main()