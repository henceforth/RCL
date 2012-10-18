
run: main.py
	python2 main.py

git: *.py
	git add *.py Makefile
	git commit -a

clean: 
	mkdir -p bak
	cp -f *.json *.log *.db bak/ 
	rm *.pyc *.log *.db
