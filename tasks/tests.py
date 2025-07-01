from django.test import TestCase
from rest_framework.test import APIClient
from json import loads


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        creation_response = self.client.post(
            "/projects/", {"title": "string", "deadline": "2025-01-01T00:00:00.00Z"}
        )
        self.assertEqual(creation_response.status_code, 201)
        self.invalid_test_data = [
            # requests test case: task date > project deadline
            {
                "title": "s",
                "deadline": "3000-07-01T14:37:26Z",
                "description": "",
                "is_completed": 0,
                "project": 1,
            },
            {
                "title": "s",
                "deadline": "2024-07-01T14:37:26Z",
                "description": "",
                "is_completed": 0,
                "project": 5000,
            },
            {
                "deadline": "2024-07-01T14:37:26Z",
                "description": "",
                "is_completed": 0,
                "project": 1,
            },
            {"title": "s", "description": "", "is_completed": 0, "project": 1},
            {
                "title": "s",
                "deadline": 123,
                "description": "",
                "is_completed": 0,
                "project": 1,
            },
            {
                "title": "s",
                "deadline": "2024-07-01T14:37:26Z",
                "description": "",
                "is_completed": "abc",
                "project": 1,
            },
        ]
        self.invalid_update_data = [{"deadline": "3000-01-01"}]

    def create_task(self):
        creation_response = self.client.post(
            "/tasks/",
            {
                "title": "string",
                "deadline": "2024-07-01T14:37:26Z",
                "description": "test",
                "is_completed": False,
                "project": 1,
            },
        )
        self.assertEqual(creation_response.status_code, 201)

    def test_create_task(self):
        test_data = {
            "title": "string",
            "deadline": "2024-07-01T14:37:26Z",
            "description": "test",
            "is_completed": False,
            "project": 1,
        }
        creation_response = self.client.post("/tasks/", test_data)
        self.assertEqual(creation_response.status_code, 201)
        creation_response = loads(creation_response.content)

        for k, v in test_data.items():
            self.assertEqual(creation_response[k], v)

        task_by_id_response = self.client.get(f'/tasks/{creation_response["id"]}/')
        self.assertEqual(task_by_id_response.status_code, 200)
        task_by_id_response = loads(task_by_id_response.content)
        for k, v in test_data.items():
            self.assertEqual(task_by_id_response[k], v)

    def test_create_project_invalid_data(self):
        for data in self.invalid_test_data:
            creation_response = self.client.post("/tasks/", data)

            self.assertEqual(creation_response.status_code, 400)

    def test_update_task(self):
        self.create_task()
        updated_data = {
            "title": "updatedfff_string",
            "deadline": "2024-07-01T14:37:26Z",
            "project": 2,
            "description": "updated one",
        }

        project_creation_response = self.client.post(
            "/projects/",
            {"title": "second project", "deadline": "2025-01-01T00:00:00.00Z"},
        )
        self.assertEqual(project_creation_response.status_code, 201)

        response = self.client.patch("/tasks/1/", data=updated_data)
        self.assertEqual(response.status_code, 200)
        for k, v in updated_data.items():
            self.assertEqual(loads(response.content)[k], v)

    def test_update_project_invalid_data(self):
        self.create_task()
        for data in self.invalid_update_data:
            response = self.client.patch("/tasks/1/", data=data)
            self.assertEqual(response.status_code, 400)

    def test_delete_task(self):
        self.create_task()
        response = self.client.delete("/tasks/1/")
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_task(self):
        response = self.client.delete("/tasks/1/")
        self.assertEqual(response.status_code, 404)

    def test_delete_project_with_tasks(self):
        self.create_task()
        response = self.client.delete("/projects/1/")
        self.assertEqual(response.status_code, 204)
        response = self.client.get("/tasks/1/")
        self.assertEqual(response.status_code, 404)
