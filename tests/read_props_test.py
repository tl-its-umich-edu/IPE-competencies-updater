import pytest
from read_env_props import ReadEnvProps


def test_missing_certain_props():
    """
    Test that the properties file is read correctly.
    """

    props = ReadEnvProps()
    props.env_props['sheet_id'] = None
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        props.get_env_props()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
