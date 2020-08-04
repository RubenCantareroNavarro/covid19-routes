# -*- mode: makefile-gmake; coding: utf-8 -*-


clean:
	$(RM) -r examples/cache/
	$(RM) -r src/utilities/__pycache__
	$(RM) -r src/__pycache__

run-example:
	./src/calculate-routes.py 39.001441 -3.924548 38.976429 -3.930899