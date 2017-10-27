from pymemcache.client.hash import HashClient


class Client(HashClient):
    def get_many(self, keys, gets=False, *args, **kwargs):
        client_batches = {}
        end = {}

        for key in keys:
            client = self._get_client(key)

            if client is None:
                continue

            if client.server not in client_batches:
                client_batches[client.server] = []

            client_batches[client.server].append(key)

        for server, keys in client_batches.items():
            client = self.clients['%s:%s' % server]
            new_args = list(args)
            new_args.insert(0, keys)

            if gets:
                get_func = client.gets_many
            else:
                get_func = client.get_many

            result = self._safely_run_func(
                client,
                get_func, {}, *new_args, **kwargs
            )
            end.update(result)

        return end

    get_multi = get_many
