# Soln

```sh
❯ pwn checksec --file=get_it
[*] '/home/pwent/code/personal/Linux_ED/Nightmare/pwn/get_it/get_it'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
```

`objdump -D get_it -M intel | less` shows `main`:

```sh
00000000004005c7 <main>:
  4005c7:       55                      push   rbp
  4005c8:       48 89 e5                mov    rbp,rsp
  4005cb:       48 83 ec 30             sub    rsp,0x30
  4005cf:       89 7d dc                mov    DWORD PTR [rbp-0x24],edi
  4005d2:       48 89 75 d0             mov    QWORD PTR [rbp-0x30],rsi
  4005d6:       bf 8e 06 40 00          mov    edi,0x40068e
  4005db:       e8 90 fe ff ff          call   400470 <puts@plt>
  4005e0:       48 8d 45 e0             lea    rax,[rbp-0x20]
  4005e4:       48 89 c7                mov    rdi,rax
  4005e7:       b8 00 00 00 00          mov    eax,0x0
  4005ec:       e8 af fe ff ff          call   4004a0 <gets@plt>
  4005f1:       b8 00 00 00 00          mov    eax,0x0
  4005f6:       c9                      leave
  4005f7:       c3                      ret
  4005f8:       0f 1f 84 00 00 00 00    nop    DWORD PTR [rax+rax*1+0x0]
  4005ff:       00
```

The `gets` call is unbounded and so we can overwrite the return address on the stack
(canary is disabled).

`nm ./get_it` shows:

```sh
00000000004005b6 T give_shell
```

Which, is:

```sh
00000000004005b6 <give_shell>:
  4005b6:       55                      push   rbp
  4005b7:       48 89 e5                mov    rbp,rsp
  4005ba:       bf 84 06 40 00          mov    edi,0x400684
  4005bf:       e8 bc fe ff ff          call   400480 <system@plt>
  4005c4:       90                      nop
  4005c5:       5d                      pop    rbp
  4005c6:       c3                      ret
```

Where `0x400684` is:

```sh
Contents of section .rodata:
 400680 01000200 2f62696e 2f626173 6800446f  ..../bin/bash.Do
 400690 20796f75 20676574 73206974 3f3f00     you gets it??.
```

So, `give_shell` results in `system("/bin/bash");`.
