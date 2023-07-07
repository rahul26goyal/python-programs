import json
import unittest


class TestJsonModule(unittest.TestCase):

    # python primitive to string
    def test_json_dumps(self):
        # json.dumps can priint the string equivalent for primitive types.
        result_string = json.dumps({"key": "value"})
        print(result_string)
        print(type(result_string))

    # python string with primitive to dict
    def test_json_loads(self):
        string = '{"key1": "value1"}'
        obj = json.loads(string)
        print(obj, type(obj))
        result = type(obj) == dict
        result1 = type(obj) == list
        self.assertTrue(result)
        self.assertFalse(result1)

    # convert python custom class obj to string
    def test_custom_class_dumps_throws_exception(self):
        obj = CustomObject()
        print(json.dumps(obj))
        # throws TypeError:`Object of type KernelDefinition is not JSON serializable`

    def test_json_encoder_class_with_dumps(self):
        obj = CustomSerializableClass()
        result_str = json.dumps(obj, cls=CustomJSONEncoder)
        print(type(result_str))
        print(f"JSON String: {result_str}")
        self.assertEqual(type(result_str), str)
        self.assertEqual(
            result_str,
            '{"customerId": 123, "applicationid": "xyz", "containerRoleToImageMap": {"key": "value"}, "containerDefinitions": [1, 2, 3, 4, 5]}',
        )

        result_dict = json.loads(result_str)
        print(f"JSON Dit:: {result_dict}")
        self.assertTrue(type(result_dict), dict)
        self.assertEqual(result_dict["customerId"], 123)

    def test_json_encoder_class_without_dumps(self):
        obj = CustomSerializableClass()
        encoder = CustomJSONEncoder()
        result_str = encoder.encode(obj)
        print(type(result_str))
        print(result_str)

    def test_inline_json_serialization_class(self):
        obj = CustomInlineSerializableClass()
        result_str = obj.json_string()
        print(type(result_str))
        print(f"JSON String: {result_str}")
        self.assertEqual(type(result_str), str)
        self.assertEqual(
            result_str,
            '{"customerId": 123, "applicationId": "xyz", "containerRoleToImageMap": {"key": "value"}, "containerDefinitions": [1, 2, 3, 4, 5]}',
        )

        result_dict = json.loads(result_str)
        print(f"JSON Dit:: {result_dict}")
        self.assertTrue(type(result_dict), dict)
        self.assertEqual(result_dict["customerId"], 123)

    def test_make_object_printable(self):
        obj = CustomInlineSerializableClass()
        print(f"Object:::{obj}")
        print(obj.__repr__())

    def test_getting_simple_class_as_dict(self):
        obj = CustomInlineSerializableClass()
        print(type(obj))
        self.assertEqual(type(obj), CustomInlineSerializableClass)
        obj_as_dict = obj.__dict__
        print(obj_as_dict)

    def test_getting_nected_class_as_dict(self):
        obj = CustomNestedClass()
        obj_as_dict = obj.__dict__

        obj_as_json_string = obj.json_string()
        print(f"JSON String: {obj_as_json_string}")

        obj_as_json_dict = json.loads(obj_as_json_string)
        print(f"JSON Dict:: {obj_as_json_dict}")
        self.assertEqual(
            obj_as_json_dict["nestedObject"]["child"]["applicationid"], "xyz"
        )

        # orig_obj = json.loads(obj_as_json_string, cls=CustomNestedClass)
        # print(orig_obj)


class CustomObject(object):
    def __init__(self):
        print("initialize...")
        self.customerId = 123
        self.applicationid = "xyz"
        self.containerRoleToImageMap = {"key": "value"}
        self.containerDefinitions = [1, 2, 3, 4, 5]


class CustomSerializableClass(object):
    TEST_CONST = 1234
    _abc = 123

    def __init__(self):
        print("initialize...")
        self.customerId = 123
        self.applicationid = "xyz"
        self.containerRoleToImageMap = {"key": "value"}
        self.containerDefinitions = [1, 2, 3, 4, 5]

    def test(self):
        print("test")


from json import JSONEncoder


# Method-1: Using JSONEncoder to make the class JSON Serializable
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        # __dict__ returns the class instance variables
        return obj.__dict__


# Method-2: using inline serialization


class CustomInlineSerializableClass(object):
    TEST_CONST = 1234
    # _abc = 123

    def __init__(self):
        print("initialize...")
        self.customerId = 123
        self.applicationId = "xyz"
        self.containerRoleToImageMap = {"key": "value"}
        self.containerDefinitions = [1, 2, 3, 4, 5]
        self._protected = "pValue"

    @property
    def protected(self):
        return self._protected

    @protected.setter
    def protected(self, p):
        self._protected = p

    def test(self):
        print("test")

    def json_string(self):
        print("#the dumps function takes an argument ``default``")
        return json.dumps(self, default=lambda obj: obj.__dict__)

    # user facing string representation.
    # https://www.digitalocean.com/community/tutorials/python-str-repr-functions
    def __str__(self):
        return self.json_string()

    # should be information rich
    def __repr__(self):
        print("repr called...")
        return f"{self.__class__.__name__}({self.__str__()})"


class ChildClass(object):
    def __init__(self):
        self.variable = 123
        self.child = CustomObject()  # nested child


class CustomNestedClass(object):
    def __init__(self):
        print("initialize...")
        self.customerId = 123
        self.applicationId = "xyz"
        self.containerRoleToImageMap = {"key": "value"}
        self.containerDefinitions = [1, 2, 3, 4, 5]
        self.nestedObject = ChildClass()

    def json_string(self):
        print("#the dumps function takes an argument ``default``")
        return json.dumps(self, default=lambda obj: obj.__dict__)
