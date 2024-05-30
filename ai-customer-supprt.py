from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import datetime

# Initialize ChatBot
chatbot = ChatBot(
    'CustomerSupportBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

# Training with custom conversation
trainer = ListTrainer(chatbot)

# Sample conversation for training
training_data = [
    "Hi, how can I help you?",
    "I'd like to reset my password.",
    "You can reset your password by visiting the settings page and clicking on 'Forgot Password'.",
    "Thank you.",
    "You're welcome! Is there anything else I can assist you with?",
    "No, that's all for now.",
    "Okay, have a great day!"
]

trainer.train(training_data)

# Train the chatbot with the ChatterBot corpus
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train('chatterbot.corpus.english')

# Function to save conversation history
def save_conversation(history):
    with open("conversation_history.txt", "a") as file:
        for line in history:
            file.write(f"{line}\n")
        file.write("\n")

# Main function to run the chatbot
def run_chatbot():
    print("Customer Support Bot: Hi! How can I assist you today?")
    conversation_history = []

    while True:
        user_input = input("You: ")

        # Save user input to history
        conversation_history.append(f"You: {user_input}")

        # Exit if user types 'bye'
        if user_input.lower() == 'bye':
            print("Customer Support Bot: Goodbye! Have a great day!")
            conversation_history.append("Customer Support Bot: Goodbye! Have a great day!")
            break

        # Get the chatbot response
        bot_response = chatbot.get_response(user_input)
        print(f"Customer Support Bot: {bot_response}")
        conversation_history.append(f"Customer Support Bot: {bot_response}")

    # Save conversation history to file
    save_conversation(conversation_history)

if __name__ == "__main__":
    run_chatbot()
