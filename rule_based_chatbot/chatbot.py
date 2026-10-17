import re

from knowledge_base import FALLBACK_RESPONSE, KNOWLEDGE_BASE

def sanitize_input(user_input):
    cleaned = user_input.lower().strip()
    # Keep arithmetic symbols so simple calculator questions still work.
    cleaned = re.sub(r"[^\w\s+*/().-]", " ", cleaned)
    return " ".join(cleaned.split())

def detect_intent(user_input):
    normalized_input = sanitize_input(user_input)
    if not normalized_input:
        return None

    phrases = []
    for intent, details in KNOWLEDGE_BASE.items():
        for keyword in details["keywords"]:
            phrases.append((len(sanitize_input(keyword)), keyword, intent))
    phrases.sort(reverse=True)

    for _, keyword, intent in phrases:
        normalized_keyword = sanitize_input(keyword)
        if normalized_input == normalized_keyword:
            return intent
        if re.search(r"(?<!\w)" + re.escape(normalized_keyword) + r"(?!\w)", normalized_input):
            return intent
    return None

def calculate(user_input):
    """Evaluate only a single basic arithmetic operation; never use eval()."""
    normalized_input = sanitize_input(user_input)
    normalized_input = re.sub(r"^(what is|calculate|compute)\s+", "", normalized_input)
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*([+*/-])\s*(-?\d+(?:\.\d+)?)", normalized_input)
    if not match:
        return None

    left_text, operator, right_text = match.groups()
    left, right = float(left_text), float(right_text)
    try:
        if operator == "+":
            answer = left + right
        elif operator == "-":
            answer = left - right
        elif operator == "*":
            answer = left * right
        else:
            answer = left / right
    except ZeroDivisionError:
        return "Division by zero is undefined. Please try a different calculation."

    if answer.is_integer():
        return str(int(answer))
    return str(answer)


def get_response(user_input):
    intent = detect_intent(user_input)
    if intent is not None:
        return KNOWLEDGE_BASE[intent]["response"]

    calculation = calculate(user_input)
    if calculation is not None:
        return calculation
    return FALLBACK_RESPONSE


def main():
    """Run the continuous command-line conversation."""
    print("=" * 50)
    print("        RULE-BASED AI CHATBOT")
    print("=" * 50)
    print("Bot: Hello! I am a Rule-Based AI Chatbot.")
    print("Bot: You can ask me questions from my knowledge base.")
    print("Bot: Type 'help' to see what I can do.")
    print("Bot: Type 'bye' or 'exit' to end the conversation.")

    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye! Have a great day!")
            break

        if sanitize_input(user_input) in {"bye", "goodbye", "exit", "quit"}:
            print("Bot: Goodbye! Have a great day!")
            break

        print("Bot: " + get_response(user_input))


if __name__ == "__main__":
    main()
