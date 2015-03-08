help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install        to install dependencies"
	@echo "  clean          to clean compiled files"
	@echo "  run            to run the script"
	@echo

install:
	@pip install -r requirements/default.txt

clean:
	@find . -name "*.pyc" -delete

run:
	@python main.py