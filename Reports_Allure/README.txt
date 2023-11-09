
1. Install Allure

    pip install allure-pytest
    pip install pytest-cov pytest-sugar  # optional

    # https://github.com/allure-framework/allure2/releases/tag/2.24.1
    # download recent allure_*.*.*.*_all.deb package

    sudo dpkg -i allure_2.24.0-1_all.deb


2. Create allure-annotated tests

    # https://allurereport.org/docs/pytest/#3-generate-a-report

3. Run pytest:

    python -m pytest TestSuite.py --alluredir allure-results
    python -m pytest TestTitle.py --clean-alluredir --alluredir allure-results


4. Generate report:

    allure serve allure-results


