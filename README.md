BankBot AI – Intelligent Banking FAQ Chatbot
Project Description

BankBot AI is an intelligent, AI-powered chatbot designed to answer banking-related frequently asked questions (FAQs) using Natural Language Processing (NLP) and Large Language Models (LLMs).

The project focuses on building a conversational system that can understand user queries in natural language and provide accurate, context-aware responses related to banking services such as accounts, loans, interest rates, cards, and general policies.

This project is suitable for:

GitHub portfolio showcase

Infosys certification / assessment submission

Local execution and demonstration

Features

Conversational chatbot for banking FAQs

Natural language understanding of user queries

Context-aware responses

Prompt-based interaction with an LLM

Modular and extensible code structure

Configurable LLM backend (can switch models or providers)

Command-line / local execution support

Techniques Used
Natural Language Processing (NLP)

Text preprocessing

Tokenization

Intent understanding

Semantic similarity for FAQ matching

Prompt Engineering

Structured prompts for consistent responses

Instruction-based prompting

Domain-specific prompt design for banking queries

LLM-based Text Generation

Transformer-based Large Language Models

Natural language response generation

Context-driven answers

Tech Stack
Programming Language

Python 3.x

Libraries / Frameworks

transformers

torch (or compatible backend)

nltk / spacy (for NLP tasks)

scikit-learn (for similarity or classification, if applicable)

AI / ML Technologies

Natural Language Processing (NLP)

Large Language Models (LLMs)

Transformer architectures

LLM Details

Uses transformer-based Large Language Models

Supports instruction-following and conversational response generation

LLM is configurable:

The model can be replaced or upgraded (e.g., open-source transformers, API-based LLMs, or enterprise models)

Prompt logic is decoupled from model implementation

This design ensures flexibility and future scalability.

Project Structure
BankBot_AI/
│
├── data/
│   └── banking_faqs.json
│
├── nlu_engine/
│   ├── preprocessing.py
│   ├── intent_detection.py
│   └── response_generator.py
│
├── models/
│   └── llm_interface.py
│
├── main.py
├── requirements.txt
└── README.md


(Structure may be adapted based on enhancements or deployment needs.)

Installation Steps

Clone the repository

git clone https://github.com/durvashah4-netizen/Infosys-_Project-BankBot-AI-Chatbot-for-Banking-FAQs.git


Navigate to the project directory

cd Infosys-_Project-BankBot-AI-Chatbot-for-Banking-FAQs


Create a virtual environment (optional but recommended)

python -m venv venv


Activate the virtual environment

Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate


Install dependencies

pip install -r requirements.txt

How to Run the Project Locally

Ensure all dependencies are installed

Run the main application file

python main.py


Enter banking-related queries in natural language

The chatbot will generate intelligent responses based on the LLM and FAQ knowledge

Certification Use Case

This project is ideal for Infosys Certification / Training Programs because it demonstrates:

Practical application of AI and NLP concepts

Understanding of LLM-based systems

Prompt engineering fundamentals

Modular Python project design

Real-world banking domain use case

It aligns well with roles involving AI Practitioner, NLP Engineer, or ML Developer learning paths.

License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this project for educational and professional purposes.

Author: Durva Shah
Project Type: Academic / Certification / AI Portfolio Project
