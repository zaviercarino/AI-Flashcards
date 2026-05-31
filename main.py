import os
import random
import sys
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
genModel = "gemini-2.5-flash"

flashCards = []

if os.path.exists("flashcards.json"):
    with open("flashcards.json", "r") as f:
        flashCards = json.load(f)


def newFlashcard():
    enableAI = input("Would you like to use AI to make the flashcards? (Y or N)")

    if enableAI.lower() == "y":
        question = input("Enter the question for the flashcard: ")

        response = client.models.generate_content(
            model=genModel, contents=f"{question} in a few words"
        )

        flashCards.append({"question": question, "response": response.text})
        with open("flashcards.json", "w") as f:
            json.dump(flashCards, f, indent=2)
    else:
        question = input("Enter the question for the flashcard: ")

        response = input("Answer: ")
        flashCards.append({"question": question, "response": response})
        with open("flashcards.json", "w") as f:
            json.dump(flashCards, f, indent=2)


def editFlashcard():

    for i in range(len(flashCards)):
        print(f"{i + 1}. {flashCards[i]}\n")

    flashcardIndex = input("Which flashcard would you like to edit? Insert index: ")

    try:
        flashcardIndex = int(flashcardIndex) - 1

        if flashcardIndex > (len(flashCards)):
            print("Flashcard does not exist")
            return

        question = input("Enter the question for the flashcard: ")

        response = client.models.generate_content(
            model=genModel, contents=f"{question} in a few words"
        )

        del flashCards[flashcardIndex]
        flashCards.insert(
            flashcardIndex, {"question": question, "response": response.text}
        )

        with open("flashcards.json", "w") as f:
            json.dump(flashCards, f, indent=2)

        print(
            f"Question: {flashCards[flashcardIndex]['question']} Answer: {flashCards[i]['response']} \n Flashcard Edit Complete."
        )

    except ValueError:
        print("Flashcard does not exist")
        return


def deleteFlashcard():

    for i in range(len(flashCards)):
        print(f"{i + 1}. {flashCards[i]}\n")

    flashcardIndex = input("Which flashcard would you like to delete? Insert index: ")

    try:
        flashcardIndex = int(flashcardIndex) - 1
        del flashCards[flashcardIndex]

        with open("flashcards.json", "w") as f:
            json.dump(flashCards, f, indent=2)

    except ValueError:
        print("Flashcard does not exist. Did you type a valid number?")


def iterate(aList):
    for i in range(len(aList)):
        print(f"Question: {aList[i]['question']}")
        input("Enter any key to flip card: ")
        print(f"Answer: {aList[i]['response']}")
        input("Next card? ")


def readFlashcards():

    randomizeOrder = input("Randomize order? (Enter 'Y') ")

    if randomizeOrder.lower() == "y":
        randomizedFlashCards = random.sample(flashCards, k=len(flashCards))
        iterate(randomizedFlashCards)
    else:
        iterate(flashCards)


def quitProgram():
    sys.exit()


def displayList():
    for i in range(len(flashCards)):
        print(f"{i}. {flashCards[i]['question']}: {flashCards[i]['response']} \n")


appCommands = {
    "create": newFlashcard,
    "edit": editFlashcard,
    "delete": deleteFlashcard,
    "read": readFlashcards,
    "quit": quitProgram,
    "display": displayList,
}

while True:
    userInput = input("What would you like to do? ").lower()

    try:
        appCommands[userInput]()
    except KeyError:
        print("Invalid Command")
