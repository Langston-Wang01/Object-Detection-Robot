**What are shells / bash?**
- A shell is a computer interface to an operating system. Essentially takes our commands and gives them to the OS to perform
- Bash is the defailt shell used my most linux-based systems.

**Proper Terminal Definition:**
- A program that runs a shell.

                terminal - > shell - > OS

**Below is a List of Terminal Commands**


*** ## Navigation and File Management ***

1. *whoami*: 
- gives the user currently logged in to the terminal session

2. *man <command>*
- offers information of <command>
- press 'q' to return to the command line

3. *clear*
- clear all previous commands that were ran in the current terminal
- can also do ctrl + l

4. *pwd* (***P***rint ***W***orking ***D***irectory)
- it prints the current folder path

5. *ls* (list)
- lists the contents of the current folder
- if you add a folder's name within the main folder, you can check its contents

6. *cd* (***C***hange ***D***irectory)
- helps you move around different directorys 
- cd .. give you the parent directory

7. *mkdir <name of directory, ...>*
- you can make folders, or multiple folders with a single command 
- To create nested folfders add "-p"

8. *touch <filename>*
- this is used to create empty files.
- use a space to seperate multiple file names you want to create.

9. *rmdir <name of directory>*
- only removes empty directories

10. *rm <filename / folder>*
- removes directories even if they are full 
(use -r at the end to remove folders with items)
**DOES NOT LEAVE DELETED FOLDERS IN THE TRASH**

11. *open <name of directory* (Mac Specific)
- opens the name of the file chosen

12. mv <current file path> <new file path or file name>
- Lets you rename files.
- Lets you move files around and into new directories. 

13. *cp <file you want to copy> <name of file*
- copies a file
- can also copy folders


*** ## Viewing and Working with File Content ***
1. *head <filename>*
- outputs the first 10 lines of a folder, but you can specify # of lines with -n

2. *tail <filename>*
- outputs the last 10 lines of a folder, can specific # with - n

3. *cat <# of files>*
- Provides the full content of a file
- Provides all content of all files, if more than one file is provided/

4. Redirection
- <folder >">" <folder> redirects the input and overwrites the content of the outputs
- <folder> ">>" <folder> redirects the input, but appends it to the content of the output. 

5. *less <filename>*
- Shows you the content stored inside a file, in a nice and interactive UI

6. *echo <output>*
- returns the output given,can be used to redirect output into other files.

7. *sort <filename>*
- DOES NOT STORE IT, outputs the case sensitive, alphabetical order.

8. *uniq <filename>*
- omits repeated lines


*** ## Search and System Info ***
1. Expansions
some characters expand into commands. e.g.
    - ~ : gives user directory
    - $USER : gives current user
    - * : list of every path name in current folder
2. *diff <filename1> <filename2>*
- returns the difference between two files

3. *find <directory to search> <criteria>
- returns all files in a directory that pass a certain criteria
( check manuel for more information on findll)

4. *du*
- gives output of all directories and their corresponding disk size. 

5. *df*
- Provides the file system with their corresponding allocated size, and space used so far.

6. *history* 
- Provides a history of all commands used in chronological order



