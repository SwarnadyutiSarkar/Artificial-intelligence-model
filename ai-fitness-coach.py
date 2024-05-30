import nltk
import sqlite3
from datetime import datetime

# Download NLTK data (only needs to be run once)
nltk.download('punkt')

# Initialize database
conn = sqlite3.connect('fitness_coach.db')
c = conn.cursor()

# Create table to log workouts
c.execute('''CREATE TABLE IF NOT EXISTS workouts
             (date TEXT, exercise TEXT, duration INTEGER)''')
conn.commit()

# Exercise recommendations
exercises = {
    'strength': ['push-ups', 'squats', 'pull-ups', 'bench press', 'deadlifts'],
    'cardio': ['running', 'cycling', 'jump rope', 'burpees', 'rowing'],
    'flexibility': ['yoga', 'stretching', 'pilates', 'tai chi', 'dynamic stretches']
}

def recommend_exercises(goal):
    return exercises.get(goal.lower(), "I don't have recommendations for that goal. Try 'strength', 'cardio', or 'flexibility'.")

def log_workout(exercise, duration):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO workouts (date, exercise, duration) VALUES (?, ?, ?)", (date, exercise, duration))
    conn.commit()
    return "Workout logged successfully!"

def parse_user_input(user_input):
    tokens = nltk.word_tokenize(user_input.lower())
    
    if 'recommend' in tokens:
        if 'strength' in tokens:
            return recommend_exercises('strength')
        elif 'cardio' in tokens:
            return recommend_exercises('cardio')
        elif 'flexibility' in tokens:
            return recommend_exercises('flexibility')
        else:
            return "What type of exercise are you interested in? Strength, cardio, or flexibility?"
    
    elif 'log' in tokens or 'record' in tokens:
        try:
            exercise = next(word for word in tokens if word in sum(exercises.values(), []))
            duration = int(next(word for word in tokens if word.isdigit()))
            return log_workout(exercise, duration)
        except StopIteration:
            return "Please specify the exercise and duration. Example: 'Log 30 minutes of running'"
    else:
        return "I didn't understand that. You can ask for exercise recommendations or log a workout."

def main():
    print("AI Fitness Coach: Hi! How can I assist you with your fitness goals today?")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("AI Fitness Coach: Goodbye! Stay fit!")
            break
        
        response = parse_user_input(user_input)
        print(f"AI Fitness Coach: {response}")

if __name__ == "__main__":
    main()
    conn.close()
