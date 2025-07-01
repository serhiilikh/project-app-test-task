from django.test import TestCase
from rest_framework.test import APIClient
from json import loads


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.invalid_test_data = [
            {"title": "string"},
            {"deadline": "2025-07-01T14:37:26.463Z"},
            {"deadline": ""},
            {"title": "", "deadline": "2025-07-01T14:37:26.463Z"},
            {"title": "string", "deadline": ""},
            {"title": "string", "deadline": "not a date"},
            {"title": "string", "deadline": 123123},
        ]
        self.invalid_update_data = [
            {"title": "string", "deadline": "not a date"},
            {"title": "string", "deadline": 123123},
            {"title": "", "deadline": 123123},
            {"title": "string", "deadline": ""},
        ]

    def test_create_project(self):
        test_data = {"title": "string", "deadline": "2025-07-01T14:37:26Z"}
        creation_response = self.client.post("/projects/", test_data)
        self.assertEqual(creation_response.status_code, 201)
        creation_response = loads(creation_response.content)

        for k, v in test_data.items():
            self.assertEqual(creation_response[k], v)

        projects_response = self.client.get("/projects/")
        self.assertEqual(projects_response.status_code, 200)
        projects_response = loads(projects_response.content)
        for k, v in test_data.items():
            self.assertEqual(projects_response["results"][0][k], v)

        project_by_id_response = self.client.get(
            f'/projects/{creation_response["id"]}/'
        )
        self.assertEqual(project_by_id_response.status_code, 200)
        project_by_id_response = loads(project_by_id_response.content)
        for k, v in test_data.items():
            self.assertEqual(project_by_id_response[k], v)

    def test_create_project_invalid_data(self):

        for data in self.invalid_test_data:
            creation_response = self.client.post("/projects/", data)
            self.assertEqual(creation_response.status_code, 400)

    def create_project(self):
        test_data = {"title": "string", "deadline": "2025-07-01T14:37:26.463Z"}
        creation_response = self.client.post("/projects/", test_data)
        self.assertEqual(creation_response.status_code, 201)

    def test_update_project(self):
        updated_data = {
            "title": "updatedfff_string",
            "deadline": "2025-07-01T14:37:26Z",
        }
        self.create_project()
        response = self.client.patch("/projects/1/", data=updated_data)
        self.assertEqual(response.status_code, 200)
        for k, v in updated_data.items():
            self.assertEqual(loads(response.content)[k], v)

    def test_update_project_invalid_data(self):
        self.create_project()
        for data in self.invalid_update_data:
            response = self.client.patch("/projects/1/", data=data)
            self.assertEqual(response.status_code, 400)

    def test_delete_project(self):
        self.create_project()
        response = self.client.delete("/projects/1/")
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_project(self):
        response = self.client.delete("/projects/1/")
        self.assertEqual(response.status_code, 404)
