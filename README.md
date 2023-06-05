# Hack the e-diary of the school

This project helps change the information about schoolkids' academic progress in the school diary database.
It is assumed that we have access to the database, where all the grades where posted. Firstly, we will need to deploy [the diary site](https://github.com/devmanorg/e-diary/tree/master).


### How to use this script to change your grades


1. Copy the `scripts.py` file and place it on the e-diary server in `e-diary/datacenter/` folder.
2. Run this code on the server console to open the Django shell:
   ```console
   python3 manage.py shell
   ```

   Output:
   ```
    Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
   ```
3. Import the script which was replaced and run it in the shell.
   ```
   from datacenter import scripts
   scripts.main()
   ``` 

   Output:
   ```
   Введите "Фамилию Имя Отчество" ученика: 
   ```
   
   Enter full name of schoolkid who's grades yor're going to change (e.g. `Фролов Иван`):

   ```
   Введите "Фамилию Имя Отчество" ученика: Фролов Иван
   ```
   
   Output:
   ```
   Все двойки и тройки были успешно заменены на пятерки.
   Все замечания от учителей были успешно удалены.
   За последний урок по каждому из предметов была добавлена похвала от учителя.
   ```

   Quit the console by pressing `Ctrl` + `D`.

4. To make sure that all the grades were changed visit the site.
   
   ```console
   python3 manage.py runserver
   ```

   Output:
   ```
   System check identified no issues (0 silenced).
   June 05, 2023 - 05:01:10
   Django version 2.2.24, using settings 'project.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
   

### Project Goals
The code is written for educational purposes.
