from datetime import datetime, timezone


class UserStateManager:
    def __init__(self):
        self._users: dict[str, dict] = {}
        self._history: dict[str, list[dict]] = {}

    def get_user(self, user_id: str) -> dict | None:
        return self._users.get(user_id)

    def create_user(self, user_id: str, **kwargs) -> dict:
        user = {
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **kwargs,
        }
        self._users[user_id] = user
        self._history[user_id] = []
        return user

    def update_user(self, user_id: str, **kwargs) -> dict | None:
        user = self._users.get(user_id)
        if user is None:
            return None
        user.update(kwargs)
        return user

    def get_history(self, user_id: str) -> list[dict]:
        return self._history.get(user_id, [])

    def add_to_history(self, user_id: str, user_msg: str, llm_response):
        self._history.setdefault(user_id, []).append(
            {
                "role": "user",
                "content": user_msg,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._history[user_id].append(
            {
                "role": "assistant",
                "content": llm_response.content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
