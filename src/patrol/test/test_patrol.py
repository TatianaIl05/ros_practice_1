from patrol.patrol import (
    choose_command, is_valid_hz, is_valid_speed, is_valid_turn_rate)


def test_choose_command_no_pose():
    cmd = choose_command(None, 0.5, 0.3)
    assert cmd.linear.x == 0.0
    assert cmd.angular.z == 0.0


def test_choose_command_with_pose():
    class FakePose:
        x = 5.0
        y = 5.0
        theta = 0.0

    cmd = choose_command(FakePose(), 0.5, 0.3)
    assert cmd.linear.x == 0.5
    assert cmd.angular.z == 0.3


def test_choose_command_custom_params():
    class FakePose:
        x = 5.0
        y = 5.0
        theta = 0.0

    cmd = choose_command(FakePose(), 0.8, 0.5)
    assert cmd.linear.x == 0.8
    assert cmd.angular.z == 0.5


def test_is_valid_hz_normal():
    assert is_valid_hz(10.0) is True
    assert is_valid_hz(5.0) is True
    assert is_valid_hz(1.0) is True
    assert is_valid_hz(30.0) is True


def test_is_valid_hz_zero():
    assert is_valid_hz(0.0) is False


def test_is_valid_hz_negative():
    assert is_valid_hz(-1.0) is False


def test_is_valid_hz_nan():
    assert is_valid_hz(float('nan')) is False


def test_is_valid_hz_too_high():
    assert is_valid_hz(31.0) is False


def test_is_valid_speed_normal():
    assert is_valid_speed(0.5) is True
    assert is_valid_speed(0.0) is True
    assert is_valid_speed(1.0) is True


def test_is_valid_speed_invalid():
    assert is_valid_speed(-0.1) is False
    assert is_valid_speed(1.1) is False
    assert is_valid_speed(float('nan')) is False


def test_is_valid_turn_rate_normal():
    assert is_valid_turn_rate(0.3) is True
    assert is_valid_turn_rate(-1.0) is True
    assert is_valid_turn_rate(1.0) is True


def test_is_valid_turn_rate_invalid():
    assert is_valid_turn_rate(-1.1) is False
    assert is_valid_turn_rate(1.1) is False
    assert is_valid_turn_rate(float('nan')) is False
