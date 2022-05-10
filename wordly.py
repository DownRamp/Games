import random
import sys

# pick word
def pick_word():
    val= random.randint(0,5756)
    txt_file = open("assets/list.txt", "r")
    content_list = txt_file.readlines()
    return content_list[val].strip()

# win or loss
def main():
    word = pick_word()
    guess = ""
    chances = 10
    succ_attempted = set()
    contains_attempted = set()
    attempted = set()

    while(word != guess):
        print("--------------------")
        print()
        print(f'You have {chances} number of chances left')
        if(guess != ""):
            print("INCORRECT")
            chances-=1
            if(chances == 0):
                print("YOU LOSE. LOSER")
                print(f'Words was {word}')
                sys.exit()

        init = input("Enter word: ").strip()
        print(len(init))
        if(len(init) != 5):
            print("Word is incorrect length")
            continue
        else:
            guess = init

        for val in range(len(guess)):
            if(guess[val] == word[val]):
                print("O", end = ' ')
                succ_attempted.add(guess[val])
            else:
                print("X", end = ' ')
                if(guess[val] in word):
                    contains_attempted.add(guess[val])
                attempted.add(guess[val])

        print("\nSuccessful guesses")
        for i in succ_attempted:
            print(i, end=" ")

        print("\nContain guesses")
        for i in contains_attempted:
            print(i, end=" ")

        print("\nUnsuccessful guesses")
        for i in attempted:
            print(i, end=" ")
            
    print("YOU WIN. WINNER")

main()
