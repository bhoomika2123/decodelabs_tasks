# Rule-Based AI Chatbot

## 1. Project Title
**Rule-Based AI Chatbot** — Industrial Training Kit, Project 1.

## 2. Introduction
This beginner-level Python project demonstrates a conversational program built from explicit rules. It recognizes common question phrases and returns responses stored in a local knowledge base. It uses no generative AI, machine learning, NLP package, network service, or external dependency.

## 3. Problem Statement
A small chatbot that responds only to greetings has limited usefulness. This project addresses that limitation with multiple predefined topic categories and question variations while ensuring that unknown questions receive a clear fallback instead of an invented answer.

## 4. Objective
Build a continuous command-line chatbot that demonstrates deterministic intent detection, string normalization, knowledge representation, control flow, exception handling, and safe basic arithmetic.

## 5. Proposed System
The system normalizes each message, searches phrase aliases in the local knowledge base, and returns the associated fixed response. If no phrase matches, it checks for one basic arithmetic operation. Unsupported questions receive the fallback response. Exit commands end the conversation.

## 6. Features
- 35 predefined intents covering conversation, computing, web technologies, general knowledge, education, and career topics.
- Multiple ways to ask about major topics, including AI, Python, and CPU.
- Case, surrounding whitespace, and basic punctuation normalization.
- Continuous chat with `bye`, `goodbye`, `exit`, and `quit` commands.
- Safe calculator for one operation using `+`, `-`, `*`, or `/`; no `eval` or expression execution.
- Clear fallback for questions outside the knowledge base.
- Python standard library only.

## 7. Technologies Used
- Python 3
- Built-in modules: `re`
- Standard language features: dictionaries, lists, strings, functions, conditions, loops, and exception handling

## 8. System Architecture
`User input → sanitize_input → detect_intent → predefined response`

If no intent matches: `User input → calculate → result or fallback`.

`chatbot.py` owns the conversation loop and matching/calculation functions. `knowledge_base.py` stores intent names, phrase aliases, and responses. `requirements.txt` documents that no third-party packages are needed.

## 9. System Workflow
1. Print the startup banner and instructions.
2. Read one message from the user.
3. Normalize case, punctuation, and whitespace.
4. Check for an exit command.
5. Match a predefined phrase to an intent.
6. If no intent matches, recognize a single basic arithmetic expression.
7. Print the fixed response, arithmetic result, or fallback and repeat.

## 10. Algorithm
```text
START
Display banner and instructions
REPEAT
    Read message
    Normalize message
    IF message is an exit command: print goodbye and stop
    Search phrase aliases in the knowledge base
    IF an intent matches: print its predefined response
    ELSE IF message is one safe arithmetic operation: calculate and print result
    ELSE: print fallback response
UNTIL stopped
END
```

## 11. Knowledge Base Design
`KNOWLEDGE_BASE` is a dictionary keyed by intent identifier. Each entry has a `keywords` list and a fixed `response` string. The knowledge base includes greetings, identity, capabilities, wellbeing, help, thanks, goodbye, AI, machine learning, Python, programming basics, computers, operating systems, databases, SQL, HTML, CSS, Java, algorithms, data structures, internet, CPU, RAM, software, hardware, mathematics, education, career, time/date, AI's full form, and India's capital.

## 12. Intent Detection
`sanitize_input()` lowercases input, removes basic punctuation while preserving calculator symbols, and collapses repeated whitespace. `detect_intent()` compares the normalized input with normalized aliases, prioritizing longer aliases and requiring word boundaries for phrase matches. It returns an intent key or `None`. All matching is deterministic.

## 13. Implementation
Run `python chatbot.py` from this folder. Enter `help` to see a summary of supported topics. Ask a phrase represented in the knowledge base, enter a basic calculation such as `10 + 20`, or type an exit command. To extend the chatbot, add aliases and a response to `KNOWLEDGE_BASE` in `knowledge_base.py`.

## 14. Complete Source Code
The complete source code is included below and is also provided as the two standalone project files.

### `chatbot.py`
```python
"""A beginner-friendly chatbot that uses only deterministic rules."""

import re

from knowledge_base import FALLBACK_RESPONSE, KNOWLEDGE_BASE


def sanitize_input(user_input):
    """Lowercase text, remove basic punctuation, and normalize whitespace."""
    cleaned = user_input.lower().strip()
    # Keep arithmetic symbols so simple calculator questions still work.
    cleaned = re.sub(r"[^\w\s+*/().-]", " ", cleaned)
    return " ".join(cleaned.split())


def detect_intent(user_input):
    """Return a predefined intent when one of its phrases matches."""
    normalized_input = sanitize_input(user_input)
    if not normalized_input:
        return None

    # Prefer longer phrases to reduce collisions (for example, Python list).
    phrases = []
    for intent, details in KNOWLEDGE_BASE.items():
        for keyword in details["keywords"]:
            phrases.append((len(sanitize_input(keyword)), keyword, intent))
    phrases.sort(reverse=True)

    for _, keyword, intent in phrases:
        normalized_keyword = sanitize_input(keyword)
        if normalized_input == normalized_keyword:
            return intent
        # Match complete words/phrases inside a longer natural-language query.
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
    """Return a fixed response, a basic calculation, or the safe fallback."""
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


```

### `knowledge_base.py`
```python
"""Predefined intents and responses for the rule-based chatbot."""


KNOWLEDGE_BASE = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
        "response": "Hello! Nice to meet you.",
    },
    "identity": {
        "keywords": ["who are you", "what are you", "your name", "what is your name"],
        "response": "I am a Rule-Based AI Chatbot. I answer using predefined rules and responses.",
    },
    "capabilities": {
        "keywords": ["what can you do", "your capabilities", "what do you know", "how can you help"],
        "response": "I can answer selected questions from my built-in knowledge base, handle simple arithmetic, and respond to basic conversation.",
    },
    "wellbeing": {
        "keywords": ["how are you", "how are you doing", "are you okay"],
        "response": "I am working as expected. Thanks for asking!",
    },
    "help": {
        "keywords": ["help", "show help", "what topics can you answer", "list topics"],
        "response": (
            "I can answer predefined questions about:\n"
            "- Artificial Intelligence and Machine Learning\n- Python and programming concepts\n"
            "- Computers, operating systems, hardware, and software\n- Databases and SQL\n"
            "- HTML, CSS, and Java\n- Algorithms and data structures\n"
            "- Internet, education, careers, general knowledge, and basic mathematics\n\n"
            "I can also respond to greetings, thanks, and simple conversation."
        ),
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thank you very much", "many thanks"],
        "response": "You are welcome!",
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see you", "see you later"],
        "response": "Goodbye! Have a great day!",
    },
    "artificial_intelligence": {
        "keywords": ["what is artificial intelligence", "artificial intelligence", "what is ai", "explain ai", "explain artificial intelligence", "tell me about ai", "tell me about artificial intelligence", "define ai", "define artificial intelligence"],
        "response": "Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence.",
    },
    "machine_learning": {
        "keywords": ["what is machine learning", "machine learning", "explain machine learning", "tell me about machine learning", "define machine learning"],
        "response": "Machine learning is a branch of AI in which a computer system uses data and a specified learning method to improve at a task. This chatbot does not use machine learning.",
    },
    "python": {
        "keywords": ["what is python", "explain python", "tell me about python", "define python", "python programming", "what is python programming"],
        "response": "Python is a high-level, general-purpose programming language known for its readable syntax and broad range of uses.",
    },
    "programming": {
        "keywords": ["what is programming", "define programming", "what is a program", "what is coding", "programming"],
        "response": "Programming is the process of writing instructions that a computer can follow to perform tasks.",
    },
    "variable": {
        "keywords": ["what is a variable", "what is variable", "define variable", "variables in programming"],
        "response": "A variable is a named place in a program used to refer to a value. The value may be read or changed as the program runs.",
    },
    "loop": {
        "keywords": ["what is a loop", "what is loop", "define loop", "loops in programming"],
        "response": "A loop is a programming control structure that repeats instructions while a condition holds or for each item in a sequence.",
    },
    "function": {
        "keywords": ["what is a function", "what is function", "define function", "functions in programming"],
        "response": "A function is a named, reusable block of code that can perform a task and may accept inputs or return a result.",
    },
    "python_list": {
        "keywords": ["what is a list in python", "python list", "list in python", "what is a list"],
        "response": "A Python list is an ordered, changeable collection of items, written with square brackets, such as [1, 2, 3].",
    },
    "dictionary": {
        "keywords": ["what is a dictionary", "dictionary in python", "python dictionary", "define dictionary"],
        "response": "A dictionary is a collection of key-value pairs. In Python, dictionaries are written with braces, for example {'name': 'Mira'}.",
    },
    "computer": {
        "keywords": ["what is a computer", "define computer", "explain computer", "computer"],
        "response": "A computer is an electronic device that accepts input, processes and stores data, and produces output according to instructions.",
    },
    "operating_system": {
        "keywords": ["what is an operating system", "what is operating system", "operating system", "define operating system", "what is an os"],
        "response": "An operating system is system software that manages a computer's hardware and provides services for applications and users.",
    },
    "database": {
        "keywords": ["what is a database", "what is database", "define database", "explain database", "database"],
        "response": "A database is an organized collection of data that can be stored, managed, and retrieved efficiently.",
    },
    "sql": {
        "keywords": ["what is sql", "define sql", "explain sql", "tell me about sql", "full form of sql"],
        "response": "SQL stands for Structured Query Language. It is commonly used to define, query, and manage data in relational databases.",
    },
    "html": {
        "keywords": ["what is html", "define html", "explain html", "full form of html", "tell me about html"],
        "response": "HTML stands for HyperText Markup Language. It provides the structure and meaning of content on web pages.",
    },
    "css": {
        "keywords": ["what is css", "define css", "explain css", "full form of css", "tell me about css"],
        "response": "CSS stands for Cascading Style Sheets. It describes how HTML content should look, including layout, colors, and fonts.",
    },
    "java": {
        "keywords": ["what is java", "define java", "explain java", "tell me about java", "java programming"],
        "response": "Java is a general-purpose, class-based programming language designed to run on systems with a compatible Java runtime.",
    },
    "algorithm": {
        "keywords": ["what is an algorithm", "what is algorithm", "define algorithm", "explain algorithm", "algorithms"],
        "response": "An algorithm is a finite, ordered set of steps for solving a problem or completing a computation.",
    },
    "data_structure": {
        "keywords": ["what is a data structure", "what is data structure", "define data structure", "data structures", "explain data structure"],
        "response": "A data structure is a way of organizing and storing data so a program can access and work with it efficiently. Examples include lists, stacks, queues, and trees.",
    },
    "internet": {
        "keywords": ["what is the internet", "what is internet", "define internet", "how does the internet work"],
        "response": "The Internet is a worldwide network of connected computer networks that communicate using shared protocols.",
    },
    "cpu": {
        "keywords": ["what is cpu", "cpu", "what does cpu mean", "tell me about cpu", "explain cpu", "full form of cpu"],
        "response": "CPU stands for Central Processing Unit. It is the main processing unit of a computer and executes instructions.",
    },
    "ram": {
        "keywords": ["what is ram", "ram", "what does ram mean", "tell me about ram", "explain ram", "full form of ram"],
        "response": "RAM stands for Random Access Memory. It temporarily holds data and instructions that a computer is actively using.",
    },
    "software": {
        "keywords": ["what is software", "define software", "examples of software"],
        "response": "Software is the set of programs and related instructions that tell a computer how to perform tasks.",
    },
    "hardware": {
        "keywords": ["what is hardware", "define hardware", "examples of hardware"],
        "response": "Hardware is the physical equipment of a computer system, such as its processor, memory, keyboard, and screen.",
    },
    "mathematics": {
        "keywords": ["what is mathematics", "what is math", "define mathematics", "basic mathematics"],
        "response": "Mathematics is the study of numbers, quantities, shapes, patterns, and the relationships between them.",
    },
    "full_form_ai": {
        "keywords": ["full form of ai", "what does ai stand for", "expand ai"],
        "response": "AI stands for Artificial Intelligence.",
    },
    "capital_india": {
        "keywords": ["capital of india", "what is the capital of india", "india capital"],
        "response": "The capital of India is New Delhi.",
    },
    "education": {
        "keywords": ["why is education important", "what is education", "importance of education"],
        "response": "Education helps people build knowledge and skills, understand the world, and prepare for personal and professional goals.",
    },
    "career": {
        "keywords": ["career advice", "how do i choose a career", "how to choose a career", "career guidance"],
        "response": "A useful starting point is to compare your interests and strengths with the skills and day-to-day work required in different roles. Seek reliable advice and try small projects or experiences.",
    },
    "time_date": {
        "keywords": ["what time is it", "what is today's date", "what is the date", "today's date"],
        "response": "I do not have a live clock or date service. Please check your device for the current time and date.",
    },
}

FALLBACK_RESPONSE = (
    "Sorry, I don't have a predefined answer for that question yet. "
    "Please try another question."
)


```

### `requirements.txt`
```text
# No third-party packages are required.
```


## 15. Sample Output
```text
==================================================
        RULE-BASED AI CHATBOT
==================================================
Bot: Hello! I am a Rule-Based AI Chatbot.
Bot: You can ask me questions from my knowledge base.
Bot: Type 'help' to see what I can do.
Bot: Type 'bye' or 'exit' to end the conversation.

You: hello
Bot: Hello! Nice to meet you.

You: what is artificial intelligence
Bot: Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence.

You: explain python
Bot: Python is a high-level, general-purpose programming language known for its readable syntax and broad range of uses.

You: what is a database
Bot: A database is an organized collection of data that can be stored, managed, and retrieved efficiently.

You: what is cpu
Bot: CPU stands for Central Processing Unit. It is the main processing unit of a computer and executes instructions.

You: what is 100 + 200
Bot: 300

You: what is quantum computing
Bot: Sorry, I don't have a predefined answer for that question yet. Please try another question.

You: bye
Bot: Goodbye! Have a great day!
```

## 16. Test Cases<br>The implementation was checked against these 28 inputs. Actual Output shows the response returned by the chatbot (exit cases show the final line); all cases matched the expected output.<br>
| ID | Input | Expected Output | Actual Output | Status |<br>|---|---|---|---|---|
| TC-01 | `hello` | Hello! Nice to meet you. | Hello! Nice to meet you. | Pass |
| TC-02 | `  What is your name? ` | I am a Rule-Based AI Chatbot. I answer using predefined rules and responses. | I am a Rule-Based AI Chatbot. I answer using predefined rules and responses. | Pass |
| TC-03 | `help` | I can answer predefined questions about:<br>- Artificial Intelligence and Machine Learning<br>- Python and programming concepts<br>- Computers, operating systems, hardware, and software<br>- Databases and SQL<br>- HTML, CSS, and Java<br>- Algorithms and data structures<br>- Internet, education, careers, general knowledge, and basic mathematics<br><br>I can also respond to greetings, thanks, and simple conversation. | I can answer predefined questions about:<br>- Artificial Intelligence and Machine Learning<br>- Python and programming concepts<br>- Computers, operating systems, hardware, and software<br>- Databases and SQL<br>- HTML, CSS, and Java<br>- Algorithms and data structures<br>- Internet, education, careers, general knowledge, and basic mathematics<br><br>I can also respond to greetings, thanks, and simple conversation. | Pass |
| TC-04 | `What is AI?` | Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence. | Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence. | Pass |
| TC-05 | `Define artificial intelligence` | Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence. | Artificial Intelligence (AI) is a field of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence. | Pass |
| TC-06 | `Explain machine learning` | Machine learning is a branch of AI in which a computer system uses data and a specified learning method to improve at a task. This chatbot does not use machine learning. | Machine learning is a branch of AI in which a computer system uses data and a specified learning method to improve at a task. This chatbot does not use machine learning. | Pass |
| TC-07 | `Explain Python` | Python is a high-level, general-purpose programming language known for its readable syntax and broad range of uses. | Python is a high-level, general-purpose programming language known for its readable syntax and broad range of uses. | Pass |
| TC-08 | `What is a variable?` | A variable is a named place in a program used to refer to a value. The value may be read or changed as the program runs. | A variable is a named place in a program used to refer to a value. The value may be read or changed as the program runs. | Pass |
| TC-09 | `What is a loop` | A loop is a programming control structure that repeats instructions while a condition holds or for each item in a sequence. | A loop is a programming control structure that repeats instructions while a condition holds or for each item in a sequence. | Pass |
| TC-10 | `What is a function?` | A function is a named, reusable block of code that can perform a task and may accept inputs or return a result. | A function is a named, reusable block of code that can perform a task and may accept inputs or return a result. | Pass |
| TC-11 | `What is a computer?` | A computer is an electronic device that accepts input, processes and stores data, and produces output according to instructions. | A computer is an electronic device that accepts input, processes and stores data, and produces output according to instructions. | Pass |
| TC-12 | `What is an operating system?` | An operating system is system software that manages a computer's hardware and provides services for applications and users. | An operating system is system software that manages a computer's hardware and provides services for applications and users. | Pass |
| TC-13 | `What is a database?` | A database is an organized collection of data that can be stored, managed, and retrieved efficiently. | A database is an organized collection of data that can be stored, managed, and retrieved efficiently. | Pass |
| TC-14 | `What is the full form of SQL?` | SQL stands for Structured Query Language. It is commonly used to define, query, and manage data in relational databases. | SQL stands for Structured Query Language. It is commonly used to define, query, and manage data in relational databases. | Pass |
| TC-15 | `Define HTML` | HTML stands for HyperText Markup Language. It provides the structure and meaning of content on web pages. | HTML stands for HyperText Markup Language. It provides the structure and meaning of content on web pages. | Pass |
| TC-16 | `What is CSS?` | CSS stands for Cascading Style Sheets. It describes how HTML content should look, including layout, colors, and fonts. | CSS stands for Cascading Style Sheets. It describes how HTML content should look, including layout, colors, and fonts. | Pass |
| TC-17 | `Tell me about Java` | Java is a general-purpose, class-based programming language designed to run on systems with a compatible Java runtime. | Java is a general-purpose, class-based programming language designed to run on systems with a compatible Java runtime. | Pass |
| TC-18 | `What is an algorithm?` | An algorithm is a finite, ordered set of steps for solving a problem or completing a computation. | An algorithm is a finite, ordered set of steps for solving a problem or completing a computation. | Pass |
| TC-19 | `Define data structure` | A data structure is a way of organizing and storing data so a program can access and work with it efficiently. Examples include lists, stacks, queues, and trees. | A data structure is a way of organizing and storing data so a program can access and work with it efficiently. Examples include lists, stacks, queues, and trees. | Pass |
| TC-20 | `What is the full form of CPU?` | CPU stands for Central Processing Unit. It is the main processing unit of a computer and executes instructions. | CPU stands for Central Processing Unit. It is the main processing unit of a computer and executes instructions. | Pass |
| TC-21 | `What does RAM mean?` | RAM stands for Random Access Memory. It temporarily holds data and instructions that a computer is actively using. | RAM stands for Random Access Memory. It temporarily holds data and instructions that a computer is actively using. | Pass |
| TC-22 | `10 + 20` | 30 | 30 | Pass |
| TC-23 | `What is 100 + 200?` | 300 | 300 | Pass |
| TC-24 | `20 / 0` | Division by zero is undefined. Please try a different calculation. | Division by zero is undefined. Please try a different calculation. | Pass |
| TC-25 | `Thank you` | You are welcome! | You are welcome! | Pass |
| TC-26 | `What is quantum computing?` | Sorry, I don't have a predefined answer for that question yet. Please try another question. | Sorry, I don't have a predefined answer for that question yet. Please try another question. | Pass |
| TC-27 | `bye` | Goodbye! Have a great day! then exit | Goodbye! Have a great day! then exit | Pass |
| TC-28 | `quit` | Goodbye! Have a great day! then exit | Goodbye! Have a great day! then exit | Pass |<br>
## 17. Advantages
- Predictable answers that can be reviewed and edited directly.
- Works offline and has no external package requirements.
- Easy for a beginner to trace from input to matching rule.
- Unknown questions are handled honestly by a fixed fallback.

## 18. Limitations
- It can answer only questions covered by its aliases and fixed responses.
- It does not understand meaning, context, spelling mistakes, or follow-up references.
- Phrase matching may select one predefined intent when a longer message contains a known phrase.
- The calculator supports only one operation at a time and standard numeric literals.
- Time/date questions intentionally receive a fixed response because the chatbot has no live clock service.

## 19. Future Enhancements
- Add carefully reviewed aliases and predefined topics.
- Add more safe calculator operations with explicit parsing rules.
- Add a small local conversation log with user consent.
- Add a graphical interface while preserving deterministic responses.

## 20. Conclusion
This project demonstrates a useful, multi-topic rule-based chatbot using Python fundamentals. Its responses are predefined and deterministic, its calculator accepts only a tightly restricted arithmetic form, and unsupported requests receive a fallback rather than generated content.
