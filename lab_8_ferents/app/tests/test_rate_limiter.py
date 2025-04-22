import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from app import app
from app.auth import User, get_current_user
from app.routes import book_collection


@pytest.mark.asyncio
@patch("app.rate_limiter.r", new_callable=AsyncMock)
async def test_rate_limit_authenticated_user(mock_redis):
    mock_redis.zremrangebyscore.return_value = None
    mock_redis.zcard.return_value = 9
    mock_redis.zadd.return_value = None
    mock_redis.expire.return_value = None

    async def override_get_current_user():
        return User(username="testuser", email="test@example.com", password="123")
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = []
    book_collection.find = MagicMock(return_value=mock_cursor)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/", headers={"Authorization": "Bearer mocked_token"})

    assert response.status_code == 200
