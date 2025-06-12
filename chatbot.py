def response(user_input):
    if 'sad' in user_input.lower():
        return 'I am sorry you are feeling sad. Can you try writing down one positive thing that happened today?'
    elif 'anxious' in user_input.lower():
        return "Let's take a deep breath. Can you name 3 things you see right now?"
    else:
        return "Thank you for sharing. I am here to help with cognitive behavioral therapy based responses. How else are you feeling?"