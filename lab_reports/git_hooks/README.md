## Git Hooks Report

---

## Hook commit-msg
Commit message should be: [#< num >] < text >
- ### invalid commit
![](commit-msg1.png)
- ### valid commit
![](commit-msg2.png)

---

## Hook pre-commit
All files are checked by black (See improve-it report) and formatted if needed

- ### TestFile Before
![](testFile1.png)
- ### commit
![](pre-commit1.png)
- ### TestFile After
![](testFile2.png)
- ### commit (but invalid)
![](pre-commit2.png)
- ### commit
![](pre-commit3.png)

---

## Server Hook pre-receive
echos "Hello world"

![](pre-receive.png)