class Immutable(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        raise NotImplementedError("This object is immutable.")

    def __delattr__(self, name):
        raise NotImplementedError("This object is immutable.")
