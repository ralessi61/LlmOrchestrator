import unittest
from llm_coordinator.models import LLMProvider, LLMRequest, LLMResponse

# poetry run python -m unittest discover -s tests -t . -> run all tests in the tests directory -> fails because the models.py file is not found
class TestLLMProvider(unittest.TestCase):
    def test_llm_provider_init(self):
        provider = LLMProvider(name="test", api_key="test")
        self.assertEqual(provider.name, "test")
        self.assertEqual(provider.api_key, "test")

if __name__ == "__main__":
    unittest.main()