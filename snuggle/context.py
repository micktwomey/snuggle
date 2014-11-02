"""Stack and thread local context

"""

import threading


_NODEFAULT = object()


class Context(threading.local):
    @property
    def contexts(self):
        if not hasattr(self, "_contexts"):
            self._contexts = []
        return self._contexts

    def push_context(self, context):
        self.contexts.append(context)

    def pop_context(self):
        self.contexts.pop()

    def set(self, key, value):
        self.contexts[-1][key] = value

    def get(self, key, default=_NODEFAULT):
        try:
            return self.contexts[-1][key]
        except KeyError:
            if default is not _NODEFAULT:
                return default
            raise

context = Context()

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    context.push_context({"foo": "main"})

    def thingy():
        ident = threading.current_thread().getName()
        logging.info((ident, "empty", context.contexts))
        assert len(context.contexts) == 0
        context.push_context({})
        context.set("foo", ident)
        logging.info((ident, "get", context.get("foo")))
        assert len(context.contexts) == 1
        context.pop_context()
        assert len(context.contexts) == 0

    logging.info((threading.current_thread().getName(), "main get", context.get("foo")))

    threads = [threading.Thread(target=thingy) for i in range(10)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logging.info((threading.current_thread().getName(), "main get", context.get("foo")))
