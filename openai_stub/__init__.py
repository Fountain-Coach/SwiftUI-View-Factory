class _ChatCompletion:
    async def acreate(self, *args, **kwargs):
        raise NotImplementedError


ChatCompletion = _ChatCompletion()
api_key = None
