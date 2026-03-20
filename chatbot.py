"""ML-backed chatbot using sentiment analysis for CBT-style responses."""
from sentiment import score_text

# Supportive responses for strong negative sentiment (CBT + acceptance)
NEGATIVE_RESPONSES = [
    "I hear that things feel difficult right now. Would you like to try writing down one small positive thing that happened today, no matter how tiny?",
    "That sounds really tough. Let's take a moment—can you name 3 things you can see around you right now? This can help ground us.",
    "Thank you for sharing with me. I'm here with you. Sometimes it helps to challenge our thoughts—what's one piece of evidence that might contradict how you're feeling?",
    "It's okay to feel this way. You don't have to fix anything right now. What would it be like to just sit with this for a moment?",
    "I'm here with you. Your nervous system might be trying to protect you—that doesn't mean you have to act on every thought. You can just be.",
]

# Reflective responses for strong positive sentiment
POSITIVE_RESPONSES = [
    "It's wonderful to hear you're feeling good. What do you think contributed to that feeling today?",
    "I'm glad things are going well for you. How might you capture or remember this moment?",
    "That's lovely. Take a moment to really savor this—what does it feel like in your body right now?",
]

# Neutral prompts (CBT + acceptance)
NEUTRAL_RESPONSES = [
    "Thank you for sharing. I'm here to help. How else are you feeling?",
    "I appreciate you opening up. What would feel most helpful right now—talking through it, or just sitting with it?",
    "I'm listening. Sometimes it helps to name our emotions—what word best describes what you're feeling in this moment?",
    "Thank you for being here. You don't have to fix anything. What's one small way you could be gentle with yourself right now?",
]


def response(user_input):
    """Generate CBT-style response based on sentiment analysis of user input."""
    if not user_input or not user_input.strip():
        return NEUTRAL_RESPONSES[0]

    label, score = score_text(user_input)

    idx = sum(ord(c) for c in user_input)

    if label == "NEGATIVE" and score <= -0.9:
        return NEGATIVE_RESPONSES[idx % len(NEGATIVE_RESPONSES)]
    if label == "POSITIVE" and score >= 0.9:
        return POSITIVE_RESPONSES[idx % len(POSITIVE_RESPONSES)]

    return NEUTRAL_RESPONSES[idx % len(NEUTRAL_RESPONSES)]
