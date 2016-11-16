
def scopetest(mut, imut):
  global gvar
  scopetest.attr = 16
  gvar += 1
  lvar = 12
  mut += [2]
  imut += "apple"
  print locals()


gvar, lvar, amut, aimut = 1, 1, [1], "pine"
print locals()

scopetest(amut, aimut) 

print locals()
