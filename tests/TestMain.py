# Test case
import unittest

from src.config import config
from ok.test.TaskTestCase import TaskTestCase

from src.tasks.CommissionsTask import CommissionsTask


class TestMyOneTimeTask(TaskTestCase):
    task_class = CommissionsTask

    config = config

    def test_feature1(self):
        self.set_image('tests/images/1.png')
        feature = self.task.find_start_btn()
        self.assertIsNotNone(feature)

    def test_feature2(self):
        self.set_image('tests/images/1.png')
        feature = self.task.find_cancel_btn()
        self.assertIsNotNone(feature)

    def test_feature3(self):
        self.set_image('tests/images/2.png')
        feature = self.task.find_esc_menu()
        self.assertIsNotNone(feature)


if __name__ == '__main__':
    unittest.main()
