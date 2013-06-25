def do_it(x):
  x.bar = 23


class Foo(object):
  def __init__(self):
    do_it(self)


foo = Foo()

print foo.bar

