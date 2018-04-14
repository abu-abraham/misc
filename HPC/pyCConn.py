import subprocess
for i in range(1,20):
  c = subprocess.Popen(["linear", str(i*100)],stdout=subprocess.PIPE).communica$
  print "For n = "+str(i*100)+" Total time taken is "+str(c[len(c)-8:])
