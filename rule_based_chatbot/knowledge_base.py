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
