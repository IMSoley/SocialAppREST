from typing import List

import pytest
from app import schemas, models

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/849849839")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("First post title", "content", True),
    ("Second post title", "content", False),
    ("Third post title", "content", True),
    ("Forth post title", "content", False),
    ("Fifth post title", "content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "Test title", "content": "Test content"})
    created_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_post.published == True
    assert created_post.title == "Test title"
    assert created_post.content == "Test content"


def test_unauthorized_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "Test title", "content": "Test content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_authorized_user_delete_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete("/posts/849849839")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts, test_user):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title": "New title", "content": "New content"})
    updated_post = schemas.PostBase(**res.json())
    assert res.status_code == 200
    assert updated_post.title == "New title"
    assert updated_post.content == "New content"


def test_update_another_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json={"title": "New title", "content": "New content"})
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_posts, test_user):
    res = authorized_client.put("/posts/849849839", json={"title": "New title", "content": "New content"})
    assert res.status_code == 404





