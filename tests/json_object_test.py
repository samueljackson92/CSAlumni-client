from csa_api import JSONObject

import unittest
import nose.tools
import json
from test_helpers import load_fixture

class JSONObjectTests(unittest.TestCase):

    def setUp(self):
        self.test_json = json.loads(load_fixture("users/show/41.json"))

    def test_create_json_object(self):
        obj = JSONObject(self.test_json)

        nose.tools.assert_equals("Chris", obj.firstname)
        nose.tools.assert_equals( "Loftus", obj.surname)

    def test_add_entries(self):
        obj = JSONObject()
        obj.add_entries(self.test_json)

        nose.tools.assert_equals("Chris", obj.firstname)
        nose.tools.assert_equals( "Loftus", obj.surname)

    def test_as_json(self):
        obj = JSONObject(self.test_json)
        json_data = obj.as_json()

        nose.tools.assert_dict_equal(self.test_json, json_data)

    def test_get_item(self):
        obj = JSONObject(self.test_json)

        nose.tools.assert_equals("Chris", obj["firstname"])
        nose.tools.assert_equals( "Loftus", obj["surname"])

    def test_set_item(self):
        obj = JSONObject(self.test_json)
        obj["firstname"] = "Sam"
        obj["surname"] = "Jackson"

        nose.tools.assert_equals("Sam", obj.firstname)
        nose.tools.assert_equals( "Jackson", obj.surname)

    def test_add_item(self):
        obj = JSONObject(self.test_json)
        obj["id"] = 41

        nose.tools.assert_equals(41, obj.id)
