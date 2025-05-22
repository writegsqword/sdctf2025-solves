from pwn import *





context.terminal = ['kitty']
c = process("./constant_folding")


gdb.attach(c)


c.interactive()
