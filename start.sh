#!/bin/bash
if [ "${TEST_MODE}" == "True" ]; then
    echo "Running tests"
    pytest --log-cli-level=DEBUG
else
    echo "Running main IPE process"
    python ipe-start.py
fi