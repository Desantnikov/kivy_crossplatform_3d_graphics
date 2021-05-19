build_and_deploy:
	@echo "Building and deploying app"
	@buildozer android debug deploy run

run_examples:
	@echo "Running examples"
	@pipenv run python /usr/share/kivy-examples/demo/kivycatalog/main.py

run_adb:
	@echo "Connecting to device via USB"
	@export PATH=$PATH:/home/admin1/.buildozer/android/platform/android-sdk/platform-tools/adb
	@adb logcat

run_adb_grep_python:
	@echo "Connecting to device via USB"
	@export PATH=$PATH:/home/admin1/.buildozer/android/platform/android-sdk/platform-tools/adb
	@adb logcat | grep python

run:
	@rm -rf ./bin/*
	@awk '{version = 0.6.}{sub(/[[:digit:]]+$/,$NF+1)}1' buildozer.spec
	@make build_and_deploy
	@make run_adb_grep_python