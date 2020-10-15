# -*- mode: makefile-gmake; coding: utf-8 -*-
PROJECT_DIR := $(shell get-project-dir)

clean:
	$(RM) -r $(PROJECT_DIR)/src/cache/
	$(RM) -r $(PROJECT_DIR)/src/utilities/__pycache__
	$(RM) -r $(PROJECT_DIR)/src/__pycache__
	$(RM) -r $(PROJECT_DIR)/reasoning/scone/.scone

run-calculate-route-example:
	./examples/calculate-routes.py 39.001441 -3.924548 38.976429 -3.930899 './src/cache/ciudad-real-graph.graphml' './src/cache/ciudad-real-danger-nodes.geojson' './config/amenities_config.json'

run-app:
	./src/app.py

run-sbcl:
	cd $(PROJECT_DIR)/reasoning/scone/; sbcl --load sbcl-file.lisp

run-scone-wrapper:
	cd $(PROJECT_DIR)/reasoning/scone/; scone-wrapper --Ice.Config=$(PROJECT_DIR)/config/scone_wrapper.config

run-reasoning-ammenities-config:
	./reasoning/proof_concept.py

update-hugo-doc:
	cd $(PROJECT_DIR)/hugo ; hugo -d $(PROJECT_DIR)/docs