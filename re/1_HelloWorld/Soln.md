# Soln

```sh
file hello_world
hello_world: ELF 32-bit LSB executable, Intel i386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=d960fac581b3aa8fc052d6695dc284d34afb16bf, not stripped
```

The program is x86 (32-bit).

```sh
objdump -D hello_world -M intel | less
```

`main` is:

```
080483fb <main>:
 80483fb:       8d 4c 24 04             lea    ecx,[esp+0x4]
 80483ff:       83 e4 f0                and    esp,0xfffffff0
 8048402:       ff 71 fc                push   DWORD PTR [ecx-0x4]
 8048405:       55                      push   ebp
 8048406:       89 e5                   mov    ebp,esp
 8048408:       51                      push   ecx
 8048409:       83 ec 04                sub    esp,0x4
 804840c:       83 ec 0c                sub    esp,0xc
 804840f:       68 b0 84 04 08          push   0x80484b0
 8048414:       e8 b7 fe ff ff          call   80482d0 <puts@plt>
 8048419:       83 c4 10                add    esp,0x10
 804841c:       b8 00 00 00 00          mov    eax,0x0
 8048421:       8b 4d fc                mov    ecx,DWORD PTR [ebp-0x4]
 8048424:       c9                      leave
 8048425:       8d 61 fc                lea    esp,[ecx-0x4]
 8048428:       c3                      ret
 8048429:       66 90                   xchg   ax,ax
 804842b:       66 90                   xchg   ax,ax
 804842d:       66 90                   xchg   ax,ax
 804842f:       90                      nop
```

Notice the call to puts:

```
push   0x80484b0
8048414:       e8 b7 fe ff ff          call   80482d0 <puts@plt>
```

Since this binary is x86, args are pushed to the stack (cdecl calling convention).

We want to confirm the initialised string at 0x80484b0 to know what `puts` will print.

The string will be in the `.rodata` section since it's an initialised string (as opposed to `.bss`
where uninitialised strings are).

```sh
objdump -s -j .rodata hello_world

hello_world:     file format elf32-i386

Contents of section .rodata:
 80484a8 03000000 01000200 68656c6c 6f20776f  ........hello wo
 80484b8 726c6421 00                          rld!.
```

```sh
./hello_world
hello world!
```
