class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self, *args, **kwargs):
        result = {}
        for k, v in self.__dict__.items():
            if hasattr(v, "dict"):
                result[k] = v.dict(*args, **kwargs)
            elif isinstance(v, list):
                processed = []
                for item in v:
                    if hasattr(item, "dict"):
                        processed.append(item.dict(*args, **kwargs))
                    else:
                        processed.append(item)
                result[k] = processed
            else:
                result[k] = v
        return result

    @classmethod
    def parse_obj(cls, obj):
        return cls(**obj)

    @classmethod
    def update_forward_refs(cls):
        pass
