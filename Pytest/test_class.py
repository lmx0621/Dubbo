import pytest

# content of test_class.py
class TestClass:
    def test_one(self):
        x = "hello"
        assert hasattr(x, 'check')

    @pytest.mark.slow
    def test_two(self):
        x = "this"
        assert 'h' in x