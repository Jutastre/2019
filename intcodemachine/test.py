import intcodemachine


print("trying intcodemachine.feed([])")
intcodemachine.feed([])
print("trying intcodemachine.feed([1.2])")
intcodemachine.feed([1])
print("trying intcodemachine.feed([1,2,3])")
intcodemachine.feed([1,2,3])

print("testing read:")
print(intcodemachine.read())