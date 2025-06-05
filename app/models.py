from typing import List, Literal, TypedDict

class IngestRequest(TypedDict):
    ids: List[int]
    priority: Literal["HIGH", "MEDIUM", "LOW"]

class BatchStatus(TypedDict):
    batch_id: str
    ids: List[int]
    status: str  # yet_to_start, triggered, completed

class IngestionStatus(TypedDict):
    ingestion_id: str
    status: str  # yet_to_start, triggered, completed
    batches: List[BatchStatus]
