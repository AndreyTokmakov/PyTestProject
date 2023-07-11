

class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1

        # TODO: self.value is still 0.
        #       even 'test_one' has been called
