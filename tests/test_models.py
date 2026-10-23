import unittest
from llm_coordinator.models import TaskType, LLMRequest, TaskResult, BatchMetrics
from pydantic import ValidationError 

# poetry run python -m unittest discover -s tests -t . -> run all tests in the tests directory -> fails because the models.py file is not found
class TestModels(unittest.TestCase):

    def test_valid_request_creation(self):
        """ Test first prompt validation """
        request = LLMRequest(
            doc_id="DOC_ID_1",
            task_type=TaskType.SUMMARY, 
            prompt="Riassumi il seguente documento in italiano: <documento>", 
            provider="fast"
        )
        self.assertEqual(request.doc_id, "DOC_ID_1")
        self.assertEqual(request.provider, "fast")
        self.assertEqual(request.task_type, TaskType.SUMMARY)
        self.assertEqual(request.prompt, "Riassumi il seguente documento in italiano: <documento>")
        self.assertIsNotNone(request.request_id)


    def test_invalid_blank_prompt_raises_error(self):
        """ Test that a blank prompt raises a ValidationError """
        with self.assertRaises(ValidationError):
            request = LLMRequest(task_type=TaskType.SUMMARY, prompt="   ", doc_id="DOC_ID_1", provider="fast")


    def test_extraction_requires_target_fields(self):
        """ Test that a empty target_fields raises a ValidationError """
        with self.assertRaises(ValidationError):
            request = LLMRequest(task_type=TaskType.EXTRACTION , target_fields=[], prompt="Estrarre i seguenti campi: <campi>", doc_id="DOC_ID_1", provider="fast")


    def test_task_result_validation(self):
        """ Test output model TaskResult is incoherent if success is False and error_message is None """
        with self.assertRaises(ValidationError):
            result = TaskResult(task_type=TaskType.SUMMARY,  success=False, error_message=None, doc_id="DOC_ID_1",provider="fast")
        # incoherent, if failed we must have an error message; provider placed because it is required field

        result = TaskResult(task_type=TaskType.SUMMARY,  success=True, error_message=None, output="testo riassunto", estimated_tokens=42, doc_id="DOC_ID_1")
        self.assertEqual(result.task_type, TaskType.SUMMARY)
        self.assertEqual(result.success, True)
        self.assertEqual(result.error_message, None)
        self.assertEqual(result.estimated_tokens, 42)


if __name__ == "__main__":
    unittest.main()