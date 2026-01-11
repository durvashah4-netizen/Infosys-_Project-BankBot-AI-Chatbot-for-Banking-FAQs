from core.llm_router import LLMRouter

def test_router_runs():
    router = LLMRouter(mode="groq")
    output = router.invoke("Check balance")
    assert "intent" in output
