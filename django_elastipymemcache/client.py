from pymemcache.client.hash import HashClient


class Client(HashClient):
    def get_many(self, keys, gets=False, *args, **kwargs):
        # pymemcache's HashClient may returns {'key': False}
        end = super(Client, self).get_many(keys, gets, args, kwargs)

        return {key: end.get(key) for key in end if end.get(key)}

    get_multi = get_many
