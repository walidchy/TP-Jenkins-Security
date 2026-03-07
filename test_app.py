from app import add, multiply
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0

# Test volontairement faux pour vérifier le pipeline
def test_fail_demo():
    # assert add(2, 2) == 5  # Commenté pour éviter l'échec
    pass