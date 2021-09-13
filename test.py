import pickle
f = open('nb.dat','wb')
pickle.dump("hElLo WoRld", f)
f.close()
b = open('nt.txt','w')
b.write("hElLo WoRld")
b.close()