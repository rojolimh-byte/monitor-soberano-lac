.PHONY: all validate index backtest test dashboard

all: validate index backtest test

validate:
	python src/reserves_validation.py

index:
	python -c "from src.index import net_predetermined_ratio; print('Index module OK')"

backtest:
	python src/backtesting.py

test:
	pytest -q

dashboard:
	streamlit run dashboards/app.py
