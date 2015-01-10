__all__ = 'Baz', 'Bing'

class Class(object): pass

Baz = Class()
Baz.baz = lambda: 'baz'
Baz.HELP = 'Baz help'

Bing = Class()
Bing.COMMAND = lambda: 'bing'
