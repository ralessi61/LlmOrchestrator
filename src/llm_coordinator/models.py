from enum import Enum
from typing import Any, Self
from uuid import UUID, uuid4 
from pydantic import BaseModel, Field, field_validator, model_validator

class TaskType(Enum):
    """ Task type enum """
    SUMMARY = "summary"
    EXTRACTION = "extraction"
    QUESTION_ANSWERING = "question_answering"
    TRANSLATION = "translation"
    DETECTION = "detection"
    CLASSIFICATION = "classification"
    GENERATION = "generation"


class LLMRequest(BaseModel):
    """ LLM request model """
    doc_id: str = Field(..., description="The document ID")
    task_type: TaskType = Field(..., description="The task type")
    prompt: str = Field(..., description="The prompt for LLM")
    provider: str = Field(default="fast", description="The LLM provider")
    request_id: UUID = Field(default_factory=uuid4, description="The request ID")
    target_fields: list[str] = Field(default=[], description="The target fields for extraction if task is EXTRACTION")

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        """ Validate that the prompt is not empty """
        # cls is the class itself, not an instance .. do not use self here...
        cleaned = v.strip()
        if not cleaned or len(cleaned) < 3:
            raise ValueError("Prompt cannot be empty, whitespace-only, or shorter than 3 characters")
        return cleaned


    @model_validator(mode="after")
    def validate_request(self) -> Self:
        """ Validate that the request is coherent """
        if self.task_type == TaskType.EXTRACTION and not self.target_fields:
            raise ValueError("Target fields are required for extraction")
        return self 


class TaskResult(BaseModel):
    """ Task result model """
    task_type: TaskType = Field(..., description="The task type")
    success: bool = Field(..., description="The success of the task")
    error_message: str | None = Field(default=None, description="The error message if the task failed")
    output: str | None = Field(default=None, description="The output of the task")
    doc_id: str = Field(..., description="The document ID")
    request_id: UUID = Field(default_factory=uuid4, description="The request ID")
    provider: str = Field(default="fast", description="The LLM provider")
    error_code: int | None = Field(default=None, description="The error code if the task failed")
    error_type: str | None = Field(default=None, description="The error type if the task failed")
    retries: int = Field(default=0, description="The number of retries for the task")
    latency: float = Field(default=0.0, description="The latency of the task in seconds")
    estimated_tokens: int = Field(default=0, ge=0, description="The estimated tokens used by the task")

    @model_validator(mode="after")
    def validate_result(self) -> Self:
        """ Validate that the result is coherent """
        if not self.success and not self.error_message:
            raise ValueError("If the task failed, the error message is required")
        if self.success and not self.output:
            raise ValueError("If the task succeeded, the output is required")
        if self.success and not self.estimated_tokens:
            raise ValueError("If the task succeeded, the estimated tokens are required")
        return self


class BatchMetrics(BaseModel):
    """ Batch metrics model """
    total_requests: int = Field(..., description="The total number of requests in the batch")
    success_requests: int = Field(..., description="The number of successful requests in the batch")
    failed_requests: int = Field(..., description="The number of failed requests in the batch")
    total_estimated_tokens: int = Field(..., description="The total estimated tokens used by the requests in the batch")
    total_latency: float = Field(..., description="The total latency of the requests in the batch in seconds")
    total_retries: int = Field(..., description="The total number of retries for the requests in the batch")