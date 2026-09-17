import asyncio
import json
import logging
from api.providers.stub import StubModelProvider
from api.spend import SpendGuard
from levers.cache_triage import ExactCache, normalize

logger = logging.getLogger('capstone')

class TriageService:
    def __init__(self, settings, provider=None):
        self.settings = settings
        self.provider = provider or StubModelProvider()
        self.guard = SpendGuard(settings.spend_ceiling, settings.spend_window)
        self.cache = ExactCache(settings.cache_ttl, settings.cache_capacity)
        self.requests = self.errors = 0

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
            self.guard.reserve(self.settings.reservation_per_item)
            results = await asyncio.wait_for(self.provider.process_batch([message]),
                                             self.settings.provider_timeout)
            if len(results) != 1:
                raise ValueError('provider result count mismatch')
            response = results[0]
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
                'spend_rejections':self.guard.rejections}
