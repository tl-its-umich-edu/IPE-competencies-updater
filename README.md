# IPE-competencies-updater

This Project is for running the InterProfessional Education(IPE) courses data for outputting the Learning outcomes and there by helping the IPE units and partnering units like Pharmacy, Social Work etc for data informed decision making. This process runs after end of term primarly for Fall/Winter/Spring-Summer terms.  

## Script Run
1. Configurations before running the script
    1. create `.env` file and place it in the project root level, copy the content from `config/env_sample.txt`. Change as needed 
    2. Google Service account JSON file need to read the google spreadsheet content. Create the folder `secrets` home directory and add `ipe_gserviceaccount.json` inside it. You can find this file [Dropbox](https://www.dropbox.com/home/TL%20Security%20files/IPE%20Process)
2. Docker run 
   1. Building the project `docker compose build`
   2. Running it `docker compose up`
3. Script Command-line Run
   1. You could also run this from the command line `python3 ipe-start.py`. This is useful for debugging.

## VS Code Debugging
1. Go to the `Run and Debug` tab in the left navgation, mark a break point in code, click the play button and it should stop at the breakpoint.
2. The [VScode](https://code.visualstudio.com/docs/python/debugging) debug configiration is configured to run current file. Always you should be at `ipe-start.py` when you start the run

## Unit tests
1. pytest is used for running test. Need to configure `IS_DOCKER_RUN = FALSE`
2. Run Pytest on command line: `pytest`. this should run all the tests in the `tests` folder
3. This command will include log messages when running tests `pytest --log-cli-level=DEBUG`
4. Note: Not configured to run the tests via docker run

## Type checking
1. This command will check all the python files `mypy ipe-start`
2. Currently gspread library don't have type as part of the library, nor python stubs written separately in [typeshed](https://github.com/python/typeshed). Currently simply ignoring then in the `mypy.ini`
3. Note: Not configured to run via docker run

