# import pytest
#
#
# @pytest.fixture(name="con")
# def c():
#     return C()
#
#
# @pytest.fixture
# def tmp_con():
#     with open("") as f:
#         yield f
#
#
# @pytest.fixture
# def use_another(tmp_con: "FileIOWrapper"):
#     ...
#
#
# def test_f(c: C):
#     assert c.f() == 1
#
#
# def test_g(c: C):
#     assert c.g() == 1
