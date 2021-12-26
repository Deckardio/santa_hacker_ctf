# Forensic

![[Pasted image 20211226184209.png]]

В заднии у нас приложен дамп сетевого трафика, значит первым делом идем запускать [Wireshark](https://www.wireshark.org/)

![[Pasted image 20211226184521.png]]

В трафике мы видим, что происходит обмен ключами. Также видно что основной трафик идет от  `192.168.66.1` и до `192.168.66.158`, но в какой то момент мы видим новый ip `192.168.66.159` и GET запрос файла `Log4jRCE`. 
Скачаем его:

![[Pasted image 20211226185246.png]]
 и выведем его содержимое
 
		 $ strings Log4jRCE.class 
	<init>
	Code
	LineNumberTable
	<clinit>
	StackMapTable
	SourceFile
	Log4jRCE.java
	8powershell.exe echo SU1LVHtsb2c0c2hlbGxfNF9ldmVyeW9uZX0=
	java/lang/Exception
	Log4jRCE
	java/lang/Object
	java/lang/Runtime
	getRuntime
	()Ljava/lang/Runtime;
	exec
	'(Ljava/lang/String;)Ljava/lang/Process;
	java/lang/Process
	waitFor
	printStackTrace
	
И видим что это вредоносный класс всеми уже полюбившейся уязвимостим CVE-2021-44228 aka Log4Shell, в которой есть команда `powershell.exe echo SU1LVHtsb2c0c2hlbGxfNF9ldmVyeW9uZX0=`, которая декодится в наш флаг **IMKT{log4shell_4_everyone}**