from patrol.patrol import choose_command


def test_choose_command_no_pose():
    cmd = choose_command(None)
    assert cmd.linear.x == 0.0
    assert cmd.angular.z == 0.0


def test_choose_command_with_pose():
    class FakePose:
        x = 5.0
        y = 5.0
        theta = 0.0

    cmd = choose_command(FakePose())
    assert cmd.linear.x == 0.5
    assert cmd.angular.z == 0.3
