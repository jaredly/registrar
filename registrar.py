#!/usr/bin/env python

import types
class Registrar:
    def __init__(self, swallow=False):
        self.reg = {}
        self.swallow = swallow

    def register(self, *args, **kwds):                                                                  
        def meta(func):
            self.add(func, args, kwds)                                                                  
            if not self.swallow:
                return func
        return meta                                                                                     
    __call__ = register

    def add(self, func, args, kwds):
        self.reg[func] = (args, kwds)
        
    def bind(self, inst):
        res = {} 
        for func, value in self.reg.iteritems():
            if callable(func):
                func = types.MethodType(func, inst, inst.__class__)
            res[func] = value
        return res

class NamedRegistrar(Registrar):
    def add(self, func, args, kwds):
        if not args:
            raise TypeError('at least one positional argument required (0 given)')
        self.reg[args[0]] = (func, args[1:], kwds)
        return func

    def bind(self, inst):
        res = {} 
        for name, value in self.reg.iteritems():
            value = list(value)
            if callable(value[0]):
                value[0] = types.MethodType(value[0], inst, inst.__class__)
            res[name] = list(value)
        return res

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


# vim: et sw=4 sts=4
