from core.llm_router import LLMRouter

router = LLMRouter(mode="groq")

examples = [
    "Check balance of account 1234",
    "Transfer 500 to account 2222 from 1111",
]

for e in examples:
    print(router.invoke(e))
