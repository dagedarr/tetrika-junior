import unittest

from task1.solutions import strict


class TestStrictDecorator(unittest.TestCase):

    def test_correct_types(self):
        @strict
        def add(x: int, y: int) -> int:
            return x + y

        self.assertEqual(add(3, 4), 7)

    def test_incorrect_type_raises(self):
        @strict
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        with self.assertRaises(TypeError) as context:
            greet(123)

        self.assertIn("Аргемент 'name' должен быть 'str'",
                      str(context.exception))

    def test_with_kwargs(self):
        @strict
        def join_names(first: str, last: str) -> str:
            return f"{first} {last}"

        self.assertEqual(join_names(
            first="Иван", last="Петров"), "Иван Петров")

    def test_preserves_function_metadata(self):
        @strict
        def example(x: int) -> int:
            """Test docstring"""
            return x

        self.assertEqual(example.__name__, "example")
        self.assertEqual(example.__doc__, "Test docstring")



if __name__ == '__main__':
    unittest.main()
