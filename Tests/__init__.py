
def pytest_addoption(parser):
    "Method to add the option to ini."
    try:
        parser.addini("rp_uuid",'help',type="pathlist")
        parser.addini("rp_endpoint",'help',type="pathlist")
        parser.addini("rp_project",'help',type="pathlist")
        parser.addini("rp_launch",'help',type="pathlist")

        parser.addoption("--email_pytest_report",
                         dest="email_pytest_report",
                         help="Email pytest report: Y or N",
                         default="N")

        parser.addoption("--browser",
                            dest="browser",
                            action="append",
                            default=[],
                            help="Browser. Valid options are firefox, ie and chrome")
        parser.addoption("--api_url",
                            dest="url",
                            default="http://35.167.62.251",
                            help="The url of the api")
        parser.addoption("--testrail_flag",
                            dest="testrail_flag",
                            default='N',
                            help="Y or N. 'Y' if you want to report to TestRail")
        parser.addoption("--test_run_id",
                            dest="test_run_id",
                            default=None,
                            help="The test run id in TestRail")
        parser.addoption("--remote_flag",
                            dest="remote_flag",
                            default="N",
                            help="Run the test in Browserstack/Sauce Lab: Y or N")
        parser.addoption("--os_version",
                            dest="os_version",
                            action="append",
                            help="The operating system: xp, 7",
                            default=[])
        parser.addoption("--ver",
                            dest="browser_version",
                            action="append",
                            help="The version of the browser: a whole number",
                            default=[])
        parser.addoption("--os_name",
                            dest="os_name",
                            action="append",
                            help="The operating system: Windows 7, Linux",
                            default=[])
        parser.addoption("--remote_project_name",
                            dest="remote_project_name",
                            help="The project name if its run in BrowserStack",
                            default=None)
        parser.addoption("--remote_build_name",
                            dest="remote_build_name",
                            help="The build name if its run in BrowserStack",
                            default=None)
        parser.addoption("--slack_flag",
                            dest="slack_flag",
                            default="N",
                            help="Post the test report on slack channel: Y or N")
        parser.addoption("--mobile_os_name",
                            dest="mobile_os_name",
                            help="Enter operating system of mobile. Ex: Android, iOS",
                            default="Android")
        parser.addoption("--mobile_os_version",
                            dest="mobile_os_version",
                            help="Enter version of operating system of mobile: 8.1.0",
                            default="8.0")
        parser.addoption("--device_name",
                            dest="device_name",
                            help="Enter device name. Ex: Emulator, physical device name",
                            default="Samsung Galaxy S9")
        parser.addoption("--app_package",
                            dest="app_package",
                            help="Enter name of app package. Ex: bitcoininfo",
                            default="com.dudam.rohan.bitcoininfo")
        parser.addoption("--app_activity",
                            dest="app_activity",
                            help="Enter name of app activity. Ex: .MainActivity",
                            default=".MainActivity")
        parser.addoption("--device_flag",
                            dest="device_flag",
                            help="Enter Y or N. 'Y' if you want to run the test on device. 'N' if you want to run the test on emulator.",
                            default="N")
        parser.addoption("--email_pytest_report",
                            dest="email_pytest_report",
                            help="Email pytest report: Y or N",
                            default="N")
        parser.addoption("--tesults",
                            dest="tesults_flag",
                            default='N',
                            help="Y or N. 'Y' if you want to report results with Tesults")
        parser.addoption("--app_name",
                            dest="app_name",
                            help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk.",
                            default="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk")
        parser.addoption("--ud_id",
                            dest="ud_id",
                            help="Enter your iOS device UDID which is required to run appium test in iOS device",
                            default=None)
        parser.addoption("--org_id",
                            dest="org_id",
                            help="Enter your iOS Team ID which is required to run appium test in iOS device",
                            default=None)
        parser.addoption("--signing_id",
                            dest="signing_id",
                            help="Enter your iOS app signing id which is required to run appium test in iOS device",
                            default="iPhone Developer")
        parser.addoption("--no_reset_flag",
                            dest="no_reset_flag",
                            help="Pass false if you want to reset app eveytime you run app else false",
                            default="true")
        parser.addoption("--app_path",
                            dest="app_path",
                            help="Enter app path")
        parser.addoption("--appium_version",
                            dest="appium_version",
                            help="The appium version if its run in BrowserStack",
                            default="1.17.0")

        parser.addoption("--interactive_mode_flag",
                            dest="questionary",
                            default="n",
                            help="set the questionary flag")
        parser.addoption("--email_pytest_report",
                         dest="email_pytest_report",
                         help="Email pytest report: Y or N",
                         default="N")

        parser.addoption("--db-name", action="store", help="Database name")
        parser.addoption("--base-url", action="store", default="http://localhost",
                         help="Base URL for the application")


    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))