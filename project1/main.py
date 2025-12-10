from groq import Groq
import wikipedia

client = Groq(api_key="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")

print("Workout Chatbot (Groq Streaming): Type 'quit', 'exit' or 'bye' to stop\n")

# Tools
def workout_plan_tool(goal: str) -> str:
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "strength" in goal_lower:
        return (
            "Muscle Gain Plan:\n"
            "- Day 1: Chest + Triceps\n"
            "- Day 2: Back + Biceps\n"
            "- Day 3: Shoulders + Abs\n"
            "- Day 4: Legs\n"
            "- Day 5: Rest or Light Cardio\n"
        )
    elif "fat" in goal_lower or "weight loss" in goal_lower:
        return (
            "Fat Loss Plan:\n"
            "- Day 1: HIIT + Full Body\n"
            "- Day 2: Cardio + Core\n"
            "- Day 3: Strength Circuit\n"
            "- Day 4: Cardio + Abs\n"
            "- Day 5: Rest\n"
        )
    else:
        return "Please specify a goal like 'muscle gain' or 'fat loss'."

def exercise_info_tool(exercise: str) -> str:
    try:
        return wikipedia.summary(exercise, sentences=2)
    except Exception:
        return f"No information found for '{exercise}'. Try another exercise."

while True:
    user_input = input("You: ")

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("\nChatbot: Goodbye!")
        break

    # Decide if the input matches workout plan or exercise info
    lower_input = user_input.lower()
    if "workout" in lower_input or "plan" in lower_input or "fat" in lower_input or "muscle" in lower_input:
        response = workout_plan_tool(user_input)
        print(f"Chatbot: {response}")
        continue
    elif "exercise" in lower_input or "how to do" in lower_input or "what is" in lower_input:
        response = exercise_info_tool(user_input)
        print(f"Chatbot: {response}")
        continue

    # Otherwise, use Groq streaming for general conversation
    print("Chatbot: ", end="", flush=True)

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful workout assistant."},
            {"role": "user", "content": user_input}
        ],
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            print(delta.content, end="", flush=True)

    print()
