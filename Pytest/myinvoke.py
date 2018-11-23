# content of myinvoke.py
import pytest
class MyPlugin(object):
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")

pytest.main(["-qq"], plugins=[MyPlugin()])