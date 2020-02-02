test: test_unit

.PHONY: test_unit
test_unit:
	pytest --strict tests/


.PHONY: bulk
bulk:
	python3 bulk.py
