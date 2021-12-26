# Reverse

![img](/img/reverse_task.png?raw=true)

Первым делом проверим, что за файл нам дан

```bash
┌──(kali㉿kali)-[~/Desktop]
└─$ file main 
main: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=231dfb995b842add27f8885cf51026a50ee9d120, stripped

```

Мы видим что это исполняемый Elf. Запустим его и посмотрим что он нам даст ~~и заметим ошибку в слове~~

```bash
┌──(dec㉿kali)-[~/Desktop]
└─$ ./main
                                                     *
  *                                                          *
                               *                  *        .--.
   \/ \/  \/  \/                            Ho-ho-ho    ./   /=*
     \/     \/      *            *                ...  (_____)
      \ ^ ^/                                       \ \_((^o^))-.     *
      (o)(O)--)--------\.                           \   (   ) \  \._.
      |    |  ||================((~~~~~~~~~~~~~~~~~))|   ( )   |     
       \__/             ,|        \. * * * * * * ./  (~~~~~~~~~~~)    
*        ||^||\.____./|| |          \___________/     ~||~~~~|~\____/ * 
         || ||     || || A            ||    ||          ||    |   
  *      <> <>     <> <>          (___||____||_____)   ((~~~~~|   *
      
Добро пожаловать в хранилище Санты 🎅🏻
Чтобы получить подарок, скажи мне пароль 🔐
Веди пароль: password
Ищу в своей базе password, подожди немного ......... 
К сожалению я не могу найти password в своей базе. Приходи когда у тебя будет пароль  
```

Просмотрев программу через [Ghidra](https://github.com/NationalSecurityAgency/ghidra) по заголовку файла понимаем что это скомпилированный python файл

![img](/img/reverse_ghidra.png?raw=true)

Для того чтобы распаковать elf file используем [PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor)

В начале нам необходимо сделать дамп нашего приложения

```bash
┌──(dec㉿kali)-[~/Desktop/pyinstxtractor]
└─$ sudo objcopy --dump-section pydata=main.dump main
```

Затем извлечем содержимое 

```bash
┌──(dec㉿kali)-[~/Desktop/pyinstxtractor]
└─$ sudo python3 pyinstxtractor.py main.dump         
[+] Processing main.dump
[+] Pyinstaller version: 2.1+
[+] Python version: 306
[+] Length of package: 5660387 bytes
[+] Found 35 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: pyi_rth_pkgutil.pyc
[+] Possible entry point: pyi_rth_inspect.pyc
[+] Possible entry point: main.pyc
[!] Warning: This script is running in a different Python version than the one used to build the executable.
[!] Please run this script in Python306 to prevent extraction errors during unmarshalling
[!] Skipping pyz extraction
[+] Successfully extracted pyinstaller archive: main.dump

You can now use a python decompiler on the pyc files within the extracted directory
```

После извлечения у нас создастся папка со всеми данными 

```bash
drwxr-xr-x  4 dec dec    4096 дек 27 01:25 .
drwxr-xr-x 14 dec dec    8192 янв  1  1970 ..
-rw-r--r--  1 dec dec  768213 дек 27 01:11 base_library.zip
-rw-r--r--  1 dec dec   66728 дек 27 01:11 libbz2.so.1.0
-rw-r--r--  1 dec dec 2917216 дек 27 01:11 libcrypto.so.1.1
drwxr-xr-x  2 dec dec    4096 дек 27 01:14 lib-dynload
-rw-r--r--  1 dec dec  202880 дек 27 01:11 libexpat.so.1
-rw-r--r--  1 dec dec  153984 дек 27 01:11 liblzma.so.5
-rw-r--r--  1 dec dec 4683728 дек 27 01:11 libpython3.6m.so.1.0
-rw-r--r--  1 dec dec  294632 дек 27 01:11 libreadline.so.7
-rw-r--r--  1 dec dec  577312 дек 27 01:11 libssl.so.1.1
-rw-r--r--  1 dec dec  170784 дек 27 01:11 libtinfo.so.5
-rw-r--r--  1 dec dec  116960 дек 27 01:11 libz.so.1
-rw-r--r--  1 dec dec    2869 дек 27  2021 main.pyc
-rw-r--r--  1 dec dec    1380 дек 27 01:11 pyiboot01_bootstrap.pyc
-rw-r--r--  1 dec dec    1706 дек 27 01:11 pyimod01_os_path.pyc
-rw-r--r--  1 dec dec    8765 дек 27 01:11 pyimod02_archive.pyc
-rw-r--r--  1 dec dec   17087 дек 27 01:11 pyimod03_importers.pyc
-rw-r--r--  1 dec dec    3638 дек 27 01:11 pyimod04_ctypes.pyc
-rw-r--r--  1 dec dec     676 дек 27 01:11 pyi_rth_inspect.pyc
-rw-r--r--  1 dec dec    1071 дек 27 01:11 pyi_rth_pkgutil.pyc
-rw-r--r--  1 dec dec 1141018 дек 27 01:11 PYZ-00.pyz
drwxr-xr-x 11 dec dec    8192 дек 27 01:14 PYZ-00.pyz_extracted
-rw-r--r--  1 dec dec     293 дек 27 01:11 struct.pyc
```

Для того, чтобы декомпилить `наш main.pyc`, необходимо отредактировать его заголовок, для этого нам необходим файл `abc.pyc` находящийся в папке `base_library.zip`. Более подробно можно почитать в этом [блоге](https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html) Открываем его в любом удобно в hex-редакторе, я использую 010 Editor

Видим что есть разница в заголовках между файлами `abc.pyc` и нашим файлом для декомпила `main.pyc`

`abc.pyc:`
![[reverse_hex1.png ]]

`main.pyc`
![[reverse_hex2.png]]

Необходимо отредактировать заголовок `main.pyc` из `abc.pyc` все что до символа `@`

![[reverse_hex3.png]]

и затем вставить в наш `main.pyc` и мы получим следующего вида заголовок

![[reverse_hex4.png]]

После этого мы можем использовать [uncompyle6](https://github.com/rocky/python-uncompyle6/). В итоге мы получим вывод следующего вида, за которым будет идти сам код

```bash
$ uncompyle6 main.pyc 
# uncompyle6 version 3.8.1.dev0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.9.7 (default, Sep 10 2021, 14:59:43) 
# [GCC 11.2.0]
# Embedded file name: main.py
# Compiled at: 2021-12-09 07:08:43
# Size of source mod 2**32: 8727 bytes
```

и наш код:

```python
import hashlib, sys, time, binascii, itertools, re
print('                                                     *\n  *                                                          *\n                               *                  *        .--.\n   \\/ \\/  \\/  \\/                            Ho-ho-ho    ./   /=*\n     \\/     \\/      *            *                ...  (_____)\n      \\ ^ ^/                                       \\ \\_((^o^))-.     *\n      (o)(O)--)--------\\.                           \\   (   ) \\  \\._.\n      |    |  ||================((~~~~~~~~~~~~~~~~~))|   ( )   |     \n       \\__/             ,|        \\. * * * * * * ./  (~~~~~~~~~~~)    \n*        ||^||\\.____./|| |          \\___________/     ~||~~~~|~\\____/ * \n         || ||     || || A            ||    ||          ||    |   \n  *      <> <>     <> <>          (___||____||_____)   ((~~~~~|   *\n      ')
mess1 = 'Добро пожаловать в хранилище Санты 🎅🏻\nЧтобы получить подарок, скажи мне пароль 🔐\n'
for char in mess1:
    sys.stdout.write(char)
    sys.stdout.flush()
    if char != '\n':
        time.sleep(0.08)
    else:
        time.sleep(1)

hash = input('Веди пароль: ')

def decode(self):
    text = [
     7, 8, 113, 882914, 49343357, 138128695, 71959430518, 771038312533, 2886369022378637]
    res = itertools.permutations(text)
    for i in res:
        tmp = ''.join([str(i) for i in i])
        try:
            alp = binascii.unhexlify(hex(int(tmp)).split('x')[1]).decode('utf-8')
            if 'x' in alp:
                pass
            else:
                result = re.sub("['|b]", '', alp)
                return result
        except:
            pass


def ansver(hash):
    password = hashlib.md5(hash.encode())
    key = '24c497d07adc9b09f0ea027aea4db7fb'
    mess2 = f"Ищу в своей базе {hash}, подожди немного ......... \n"
    mess4 = f"К сожалению я не могу найти {hash} в своей базе. Приходи когда у тебя будет пароль"
    for char in mess2:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != '\n':
            time.sleep(0.08)
        else:
            time.sleep(1)

    if str(password.hexdigest()) == key:
        flag = decode(hash)
        mess3 = f"А вот и твой подарок 🎁, держи его: {flag}"
        for char in mess3:
            sys.stdout.write(char)
            sys.stdout.flush()
            if char != '\n':
                time.sleep(0.08)
            else:
                time.sleep(1)

    else:
        for char in mess4:
            sys.stdout.write(char)
            sys.stdout.flush()
            if char != '\n':
                time.sleep(0.08)
            else:
                time.sleep(2)


ansver(hash)

```

Тут мы видим функцию `ansver()` в которой и происходит формирование флага. Судя по ее содержимому, она переводит из `int` в `ascii` и создает все возможные варианты из словаря  `itertools.permutations(text)` 
Тут мы видим функцию `ansver()` в которой и происходит формирование флага. Функция `itertools.permutations(text)`  создает из заданного списка все варианты его перестановок, затем происходит декодирование из `int` в `ascii` и `pass` всех вариантов, которые не могут быть декодированы в строку, путем поиска символа `x` в полученных декодированных вариантов перестановок, после выводит флаг.

### Альтернативный способ решения

После применения  [PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor) мы можем уже считать значение strings из нашего `main.pyc` файла

```bash
┌──(dec㉿kali)-[/media/dec/ESD-USB/main.dump_extracted]
└─$ strings main.pyc      
                                                     *
  *                                                          *
                               *                  *        .--.
   \/ \/  \/  \/                            Ho-ho-ho    ./   /=*
     \/     \/      *            *                ...  (_____)
      \ ^ ^/                                       \ \_((^o^))-.     *
      (o)(O)--)--------\.                           \   (   ) \  \._.
      |    |  ||================((~~~~~~~~~~~~~~~~~))|   ( )   |     
       \__/             ,|        \. * * * * * * ./  (~~~~~~~~~~~)    
*        ||^||\.____./|| |          \___________/     ~||~~~~|~\____/ * 
         || ||     || || A            ||    ||          ||    |   
  *      <> <>     <> <>          (___||____||_____)   ((~~~~~|   *
      u
d       g       }
str)
main.py
<listcomp>&
decode.<locals>.<listcomp>
utf-8z
['|b])
        itertools
permutations
join
binascii
        unhexlify
split
decode
sub)
self
text
resr
resultr
nDxB|
 24c497d07adc9b09f0ea027aea4db7fbu
 ......... 
hashlib
encode
stdout
write
flush
time
sleepr
        hexdigestr
hash
password
mess2
mess4
char
flag
mess3r
ansver2
print
mess1r1
inputr,
<module>
```

Видно что среди строк есть странная запись `24c497d07adc9b09f0ea027aea4db7fb` (надо убрать последний символ, так как он не является частью строки). Строка очень похоже на md5 hash. Поиск по известным базам данных дает нам результат, что данный hash это закодированное слово `bigsanta`. Попробуем ввести его в оригинальную программу

```bash
┌──(dec㉿kali)-[~/Desktop/pyinstxtractor]
└─$ ./main     
                                                     *
  *                                                          *
                               *                  *        .--.
   \/ \/  \/  \/                            Ho-ho-ho    ./   /=*
     \/     \/      *            *                ...  (_____)
      \ ^ ^/                                       \ \_((^o^))-.     *
      (o)(O)--)--------\.                           \   (   ) \  \._.
      |    |  ||================((~~~~~~~~~~~~~~~~~))|   ( )   |     
       \__/             ,|        \. * * * * * * ./  (~~~~~~~~~~~)    
*        ||^||\.____./|| |          \___________/     ~||~~~~|~\____/ * 
         || ||     || || A            ||    ||          ||    |   
  *      <> <>     <> <>          (___||____||_____)   ((~~~~~|   *
      
Добро пожаловать в хранилище Санты 🎅🏻
Чтобы получить подарок, скажи мне пароль 🔐
Веди пароль: bigsanta
Ищу в своей базе bigsanta, подожди немного ......... 
А вот и твой подарок 🎁, держи его: IMKT{gift_4r0m_5a@nt@_c1@u5} 
```

 Пароль подошел и мы получили флаг. Но первый вариант решение думаю интереснее, делая таску, я задумывал решение через него, так совпало, что пароль который я придумал есть в базах =)