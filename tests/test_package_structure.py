"""Test package structure."""

def test_simple_import():
    """Test that we can import the simple test module."""
    from linkml_coral.datamodel import simple_test
    assert simple_test.Person is not None
    assert simple_test.PersonCollection is not None


def test_package_structure():
    """Test basic package structure works."""
    import linkml_coral
    # This just tests that the package can be imported
    assert linkml_coral is not None