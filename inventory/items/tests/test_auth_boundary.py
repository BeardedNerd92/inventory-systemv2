from django.test import TestCase
from django.urls import reverse
from items.session_store import SESSIONS
import json
from items.domain.models import Item


class TestAuthBoundary(TestCase):
    def test_post_items_without_auth_returns_401_and_state_unchanged(self):
        before = Item.objects.count()

        url = reverse("items:create") 
        resp = self.client.post(
            url,
            data={"name": "milk", "qty": 2},
            content_type="application/json",
        )

        after = Item.objects.count()

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(after, before)




    def test_authenticated_post_sets_owner_id(self):
        # Arrange
        token = "token-a"
        user_id = "user-a"
        SESSIONS[token] = user_id

        # Act
        resp = self.client.post(
            "/items",
            data=json.dumps({"name": "milk", "qty": 2}),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
        )

        # Assert
        self.assertEqual(resp.status_code, 201)

        created = Item.objects.last()
        self.assertEqual(created.owner_id, user_id)

        payload = resp.json()
        self.assertEqual(payload["owner_id"], user_id)

    def test_non_owner_cannot_delete(self):
        token_a, user_a = "token-a", "user-a"
        token_b, user_b = "token-b", "user-b"
        SESSIONS[token_a] = user_a
        SESSIONS[token_b] = user_b


        create_resp = self.client.post(
            "/items",
            data=json.dumps({"name": "milk", "qty": 2}),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {token_a}"},
        )
        self.assertEqual(create_resp.status_code, 201)
        item_id = create_resp.json()["id"]


        delete_resp = self.client.delete(
            f"/items/{item_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {token_b}"},
        )


        self.assertEqual(delete_resp.status_code, 403)
        self.assertTrue(Item.objects.filter(id=item_id).exists())