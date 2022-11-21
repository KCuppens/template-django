import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase

from apps.blog.tests.factories import BlogFactory
from apps.users.tests.factories import UserFactory


class BlogTestCase(JSONWebTokenTestCase):
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_blog(self):
        return BlogFactory()

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_user(self):
        return UserFactory(is_staff=True)

    def setUp(self):
        self.blog = self.create_blog()
        self.user = self.create_user()
        self.client.authenticate(self.user)

    def test_get_filter_blogs(self):
        query = """
            query getFilterBlogs($name: String!) {
                getFilterBlogs(name: $name){
                    name,
                    id,
                    description,
                    keywords
                }
            }
            """
        variables = {"name": self.blog.name}
        response = self.client.execute(query, variables)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["getFilterBlogs"][0]["name"], self.blog.name)

    def test_get_blog_detail(self):
        query = """
            query getBlogDetail($id: String!) {
                getBlogDetail(id: $id){
                    name,
                    id,
                    description,
                    keywords
                }
            }
            """
        variables = {"id": str(self.blog.id)}
        response = self.client.execute(query, variables)
        self.assertEqual(response.data["getBlogDetail"]["name"], self.blog.name)
        self.assertEqual(response.data["getBlogDetail"]["description"], self.blog.description)
        self.assertEqual(response.data["getBlogDetail"]["keywords"], self.blog.keywords)
