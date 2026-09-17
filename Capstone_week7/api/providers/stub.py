"""Synthetic contract fixtures, deliberately not a clinical classifier."""
import asyncio
from typing import Protocol
from api.models import TriageResponse

class ModelProvider(Protocol):
    async def process_batch(self, messages: list[str]) -> list[TriageResponse]: ...

class StubModelProvider:
    def __init__(self, delay=0.02):
        self.delay = delay
        self.calls = 0
        self.items = 0

    async def process_batch(self, messages):
        self.calls += 1
        self.items += len(messages)
        # Synthetic fixed transport overhead per batch; no real inference or billing.
        await asyncio.sleep(self.delay)
        results = []
        for message in messages:
            emergency = any(term in message.casefold() for term in
                            ('chest pain', 'cannot breathe', 'unconscious'))
            results.append(TriageResponse(
                urgency='emergency' if emergency else 'review',
                advice=('Seek immediate emergency assistance.' if emergency else
                        'This demo cannot assess your symptoms. Contact a qualified clinician.')))
        return results
