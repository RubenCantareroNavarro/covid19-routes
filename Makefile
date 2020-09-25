# -*- mode: makefile-gmake; coding: utf-8 -*-
PROJECT_DIR := $(shell get-project-dir)

clean:
	$(RM) -r examples/cache/
	$(RM) -r src/utilities/__pycache__
	$(RM) -r src/__pycache__
	$(RM) -r $(PROJECT_DIR)/reasoning/scone/.scone

run-calculate-route-example:
	./src/calculate-routes.py 39.001441 -3.924548 38.976429 -3.930899 './src/cache/simply-ciudad-real-graph.graphml' './src/cache/ciudad-real-danger-nodes.geojson'

run-sbcl:
	cd $(PROJECT_DIR)/reasoning/scone/; sbcl --load sbcl-file.lisp

run-scone-wrapper:
	cd $(PROJECT_DIR)/reasoning/scone/; scone-wrapper --Ice.Config=$(PROJECT_DIR)/reasoning/server.config