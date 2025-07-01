class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self, *args, **kwargs):
        return self.__dict__

    @classmethod
    def parse_obj(cls, obj):
        return cls(**obj)

    @classmethod
    def update_forward_refs(cls):
        pass
