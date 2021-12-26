# Forensic

![[task_small.png]]

Не слишком подробное описание. Будем работать с тем, что имеется. 

После распаковки архива на выходе имеем файл образа `image.vhd`. 

Самый простой путь для решения задачи – использовать специализированное форензик ПО. Например, [FTK Imager](https://accessdata.com/products-services/forensic-toolkit-ftk/ftkimager).

После добавления образа в Evidence Tree сразу видим один восстановленный раздел размером в 7 МБ, который по каким-то причинам был удален из таблицы разделов MBR. В нём содержится один из файлов с флагом.

![[small_info.png]]

Вернемся к первому разделу. После беглого просмотра видим удаленный файл `flag.png`. После восстановления и просмотра получаем второй флаг.

Дело в том, что процесс удаления в NTFS происходит в несколько этапов. Удаленный файл может «существовать» на диске до тех пор, пока не будет перезаписан другими данными.

![[small_log.png]]

Последний флаг находился в закодированном виде в альтернативном потоке файла `hacker_santa.jpg`. После декодирования base64 получаем результат.

![[small_flag.png]]

Что почитать:  
 - Структура и анализ MBR: http://blog.hakzone.info/posts-andarticles/bios/analysing-the-master-boot-record-mbr-with-a-hex-editor-hexworkshop/;
 - Подробный анализ файловых систем приведен в книге «File System Forensic Analysis» от Brian Carrier;
 - Подробнее про альтернативные потоки NTFS: https://blog.foldersecurityviewer.com/ntfs-alternate-data-streams-the-goodand-the-bad/.