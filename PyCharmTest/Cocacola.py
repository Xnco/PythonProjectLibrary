
class TestA:
    attr= 1

obj_a = TestA()

TestA.attr = 100

print(obj_a.attr)  #100