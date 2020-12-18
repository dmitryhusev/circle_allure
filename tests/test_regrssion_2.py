import pytest



class TestSample:

    def test_regression_3(self):
        assert 1

    @pytest.mark.end_to_end
    def test_regression_4(self):
        assert True
