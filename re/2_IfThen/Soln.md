# Soln

```sh
file if_then
if_then: ELF 32-bit LSB executable, Intel i386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=161e273d0832c1300de265bee5b7c82b3781ec0c, not stripped
```

The program is x86 (32-bit).

```sh
objdump -D if_then -M intel | less
```

`main` is:

```sh
080483fb <main>:
 80483fb:       8d 4c 24 04             lea    ecx,[esp+0x4]
 80483ff:       83 e4 f0                and    esp,0xfffffff0
 8048402:       ff 71 fc                push   DWORD PTR [ecx-0x4]
 8048405:       55                      push   ebp
 8048406:       89 e5                   mov    ebp,esp
 8048408:       51                      push   ecx
 8048409:       83 ec 14                sub    esp,0x14
 804840c:       c7 45 f4 0a 00 00 00    mov    DWORD PTR [ebp-0xc],0xa
 8048413:       83 7d f4 0a             cmp    DWORD PTR [ebp-0xc],0xa
 8048417:       75 10                   jne    8048429 <main+0x2e>
 8048419:       83 ec 0c                sub    esp,0xc
 804841c:       68 c0 84 04 08          push   0x80484c0
 8048421:       e8 aa fe ff ff          call   80482d0 <puts@plt>
 8048426:       83 c4 10                add    esp,0x10
 8048429:       b8 00 00 00 00          mov    eax,0x0
 804842e:       8b 4d fc                mov    ecx,DWORD PTR [ebp-0x4]
 8048431:       c9                      leave
 8048432:       8d 61 fc                lea    esp,[ecx-0x4]
 8048435:       c3                      ret
 8048436:       66 90                   xchg   ax,ax
 8048438:       66 90                   xchg   ax,ax
 804843a:       66 90                   xchg   ax,ax
 804843c:       66 90                   xchg   ax,ax
 804843e:       66 90                   xchg   ax,ax
```

We note that:

```sh
mov DWORD PTR [ebp-0xc],0xa
cmp DWORD PTR [ebp-0xc],0xa
```

Stores `0xa` at address at `ebp-0xc` (square brackets dereferences memory).

Then it immediately compares said address with `0xa`.

The following `jne 8048429 <main+0x2e>` therefore won't be taken and instead a call to `puts`
is made to print contents `0x80484c0`.

Per `objdump -s -j ".rodata" if_then`, `0x80484c0` in `.rodata` is:

```sh
Contents of section .rodata:
 80484b8 03000000 01000200 78203d20 74656e00  ........x = ten.
```

```sh
❯ ./if_then
x = ten
```

This is an example of branching `if` statement.
