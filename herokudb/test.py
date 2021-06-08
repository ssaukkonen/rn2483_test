import textwrap
cred = open('cred','r')
cred2 = cred.readline()
cred2 = cred2.split(';')
print(cred2[0])
cred.close()

#f = open(filename)
#file_content = f.read()
#f.close()