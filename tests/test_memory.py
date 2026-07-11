from jarvis.core.config import settings
from jarvis.core.models import Message
from jarvis.memory.inmemory import InMemoryBackend


def test_memory_add_and_retrieve():
    memory = InMemoryBackend()
    session_id = "test-session"

    msg1 = Message(role="user", content="Hello")
    msg2 = Message(role="assistant", content="Hi there!")

    memory.add_message(session_id, msg1)
    memory.add_message(session_id, msg2)

    messages = memory.get_messages(session_id)
    assert len(messages) == 2
    assert messages[0].content == "Hello"
    assert messages[1].content == "Hi there!"


def test_memory_truncate():
    # Save the original setting
    original_history = settings.memory_max_history
    settings.memory_max_history = 3

    memory = InMemoryBackend()
    session_id = "test-session"

    for i in range(5):
        memory.add_message(session_id, Message(role="user", content=f"Message {i}"))

    messages = memory.get_messages(session_id)
    assert len(messages) == 3
    # The last 3 messages should be 2, 3, 4
    assert messages[0].content == "Message 2"
    assert messages[2].content == "Message 4"

    # Restore
    settings.memory_max_history = original_history


def test_memory_clear_session():
    memory = InMemoryBackend()
    session_id = "test-session"

    memory.add_message(session_id, Message(role="user", content="Hello"))
    assert len(memory.get_messages(session_id)) == 1

    memory.clear_session(session_id)
    assert len(memory.get_messages(session_id)) == 0


def test_memory_list_sessions():
    memory = InMemoryBackend()

    memory.add_message("session1", Message(role="user", content="A"))
    memory.add_message("session2", Message(role="user", content="B"))

    sessions = memory.list_sessions()
    assert set(sessions) == {"session1", "session2"}
