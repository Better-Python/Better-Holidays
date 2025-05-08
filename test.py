import BetterHolidays as bh



class Foo:
    @bh.utils.classproperty
    def bar(cls):
        return "bar"
  
    @bar.delete
    def bar(cls):
        print("deleted")

print(Foo.bar)
Foo.bar = "foobar"
print(Foo.bar)
del Foo.bar
print(Foo.__dict__)
print(Foo.bar)
