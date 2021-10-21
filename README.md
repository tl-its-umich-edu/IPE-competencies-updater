# IPE-competencies-updater

This Project is for running the InterProfessional Education(IPE) courses data for outputting the Learning outcomes and there by helping the IPE units and partnering units like Pharmacy, Social Work etc for data informed decision making. This process runs after end of term primarly for Fall/Winter/Spring-Summer terms.  

## Script Run and tests
1. Configurations before running the script
    1. create `.env` file and place it in the project root level, copy the content from `config/env_sample.txt`. Change as needed 
    2. Google Service account JSON file is needed to read the google spreadsheet content. Create the folder structure `secrets/ipe/` inside home directory and add `ipe_gserviceaccount.json` inside it. You can find this file [Dropbox](https://www.dropbox.com/home/TL%20Security%20files/IPE%20Process)
    3. The Google service account email address need to be added to the google sheets with `Editor` Permission.
    4. pytest is used for running test.
2. Docker run 
   1. Building the project `docker compose build`
   2. Running the IPE job `docker compose up job`
   3. Running the test `docker compose up test`
   4. Running both job abd test `docker compose up` . Note: I would rather avoid this step since it will run both and while reviewing and testing it will be confusing
3. Script Command-line Run
   1. Main Process `python3 ipe-start.py`. This is useful for debugging.
   2. Pytest: `pytest`

## VS Code Debugging
1. Go to the `Run and Debug` tab in the left navgation, mark a break point in code, click the play button and it should stop at the breakpoint.
2. The [VScode](https://code.visualstudio.com/docs/python/debugging) debug configiration is configured to run current file. Always you should be at `ipe-start.py` when you start the run
## Type checking
1. This command will check all the python files `mypy ipe-start.py`
2. Currently gspread library don't have type as part of the library, nor python stubs written separately in [typeshed](https://github.com/python/typeshed). Currently simply ignoring then in the `mypy.ini`
3. Note: Not configured to run via docker run

