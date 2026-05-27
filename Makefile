.PHONY: install run clean

install:
	pip install -r requirements.txt

run:
	python -m src.run_all

clean:
	rm -f data/processed/*.csv
	rm -f outputs/tables/*.csv outputs/tables/*.xlsx
	rm -f outputs/figures/*.png
	rm -f outputs/models/*.txt outputs/models/*.log
