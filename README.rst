I often find myself writing meta decorators:

.. code-block:: python

    _reg = {}
    def register(name):
         def meta(func):
              _reg[name] = func
              return func
         return meta

Or some such thing. And that solution is very often enough. But, for the times when you need a bit more control, I've created ``Registrar``. The situation that prompted me to write this was within the confines of a class -- and the functions were being "registered" before they became bound...

Anyway, here's a sample of Registrar in action::

    from registrar import NamedRegistrar

    class Spam:
        def __init__(self):
            self.events = self._events.bind(self)

            # or
            self.shop = Shoppe()
            for event, value in self._events.bind(self):
                self.show.addEventHandler(event, value[0], **value[2])

        ## setup events
        _events = NamedRegistrar()

        @_events('cheese', bubble=False)
        def onCheese(self, baz):
            pass
        
        @_events('eggs')
        def onEggs(self, baz):
            return 'no eggs. cheese.'

