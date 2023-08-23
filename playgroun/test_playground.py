from rest_framework.test import APIClient
class TestPlayground:
    def tsst_that_anonymous_user_cant_create_author(self):
        client = APIClient()
        client.post()
        # then i pass in the url and the request that is needed for the method