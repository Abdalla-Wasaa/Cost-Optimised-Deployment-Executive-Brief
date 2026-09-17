import asyncio
import json
import logging
from decimal import Decimal
from levers.batch_worker import BatchQueue
from api.providers.stub import StubModelProvider
from api.spend import SpendGuard
from levers.cache_triage import ExactCache, normalize

logger = logging.getLogger('capstone')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
logger.propagate = False

class TriageService:
    def __init__(self, settings, provider=None):
        self.settings = settings
        self.provider = provider or StubModelProvider()
        self.guard = SpendGuard(settings.spend_ceiling, settings.spend_window)
        self.cache = ExactCache(settings.cache_ttl, settings.cache_capacity)
        self.requests = self.errors = 0
        self.queue = (BatchQueue(self._invoke, settings.max_batch, settings.batch_wait,
                                settings.queue_capacity, settings.request_timeout)
                      if settings.batch_enabled else None)

    async def _invoke(self, messages):
        self.guard.reserve(Decimal(str(self.settings.reservation_per_item))*len(messages))
        logger.info(json.dumps({'event':'provider_batch','items':len(messages)}))
        results = await asyncio.wait_for(self.provider.process_batch(messages),
                                         self.settings.provider_timeout)
        if len(results) != len(messages):
            raise ValueError('provider result count mismatch')
        return results

    async def close(self):
        if self.queue:
            await self.queue.close()

    async def process(self, message):
        self.requests += 1
        message = normalize(message)
        status = 'DISABLED'
        if self.settings.cache_enabled:
            response = self.cache.get(message)
            status = 'HIT' if response is not None else 'MISS'
            logger.info(json.dumps({'event':'cache','status':status}))
            if response is not None:
                return response.model_copy(update={'cache':'HIT'})
        try:
            response = (await self.queue.submit(message) if self.queue else
                        (await self._invoke([message]))[0])
            if self.settings.cache_enabled:
                self.cache.put(message, response)
            return response.model_copy(update={'cache':status})
        except Exception:
            self.errors += 1
            logger.warning(json.dumps({'event':'request_failed'}))
            raise

    def metrics(self):
        return {'requests':self.requests,'errors':self.errors,
                'cache_hits':self.cache.hits,'cache_misses':self.cache.misses,
                'cache_hit_rate':self.cache.hit_rate,
                'provider_calls':getattr(self.provider,'calls',None),
                'provider_items':getattr(self.provider,'items',None),
                'reserved_modelled_usd':float(self.guard.used),
                'avoided_modelled_usd':self.cache.hits*self.settings.reservation_per_item,
                'spend_rejections':self.guard.rejections,
                'batches':self.queue.batches if self.queue else 0,
                'batch_failures':self.queue.failures if self.queue else 0,
                'queue_rejected':self.queue.rejected if self.queue else 0,
                'recent_batch_sizes':self.queue.batch_sizes if self.queue else []}
