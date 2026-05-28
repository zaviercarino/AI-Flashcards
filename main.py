import os
import random
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

flashCards = []


def newFlashcard():

    question = input("Enter the question for the flashcard: ")

    response = client.models.generate_content(
        model="gemini-3.5-flash", contents=f"{question} in a few words"
    )

    flashCards.append({"question": question, "response": response.text})


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
            model="gemini-3.5-flash", contents=f"{question} in a few words"
        )

        del flashCards[flashcardIndex]
        flashCards.insert(
            {"question": question, "response": response.text}, flashcardIndex
        )

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
    except ValueError:
        print("Flashcard does not exist. Did you type a valid number?")


def iterate(aList):
    for i in range(len(aList)):
        print(f"Question: {flashCards[i]['question']}")
        input("Enter any key to flip card: ")
        print(f"Answer: {flashCards[i]['response']}")


def readFlashcards():

    randomizeOrder = input("Randomize order? (Enter 'Y') ")

    if randomizeOrder.lower() == "y":
        randomizedFlashcards = random.shuffle(flashCards)
        iterate(randomizedFlashcards)

    else:
        iterate(flashCards)


appCommands = {
    "create": newFlashcard,
    "edit": editFlashcard,
    "delete": deleteFlashcard,
    "read": readFlashcards,
}

while True:
    userInput = input("What would you like to do? ").lower()

    try:
        appCommands[userInput]()
    except KeyError:
        print("Invalid Command")
