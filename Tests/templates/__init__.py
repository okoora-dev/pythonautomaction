def pytest_addoption(parser):
    "Method to add the option to ini."
    try:
        parser.addoption("--db-name", action="store", help="Database name")
        parser.addoption("--base-url", action="store", default="http://localhost",
                         help="Base URL for the application")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))