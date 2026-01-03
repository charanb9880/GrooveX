"""
Unit tests for the ActionLogger module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from playlist.action_logger import ActionLogger, Action


def test_initialize_action_logger():
    """Test initializing an action logger."""
    logger = ActionLogger()
    assert logger.get_history_size() == 0
    assert logger._max_history == 50


def test_log_action():
    """Test logging actions."""
    logger = ActionLogger()
    
    # Define a simple undo function for testing
    def dummy_undo(param1, param2):
        pass
    
    # Log an action
    logger.log_action("add", dummy_undo, param1="value1", param2="value2")
    
    assert logger.get_history_size() == 1
    history = logger.get_action_history()
    assert len(history) == 1
    assert history[0] == "add"


def test_undo_last_n_actions():
    """Test undoing last N actions."""
    logger = ActionLogger()
    
    # Track calls to undo functions
    undo_calls = []
    
    def undo_add(song_id):
        undo_calls.append(f"undo_add_{song_id}")
    
    def undo_delete(index):
        undo_calls.append(f"undo_delete_{index}")
    
    def undo_move(from_idx, to_idx):
        undo_calls.append(f"undo_move_{from_idx}_to_{to_idx}")
    
    # Log several actions
    logger.log_action("add", undo_add, song_id=1)
    logger.log_action("delete", undo_delete, index=2)
    logger.log_action("move", undo_move, from_idx=0, to_idx=3)
    
    assert logger.get_history_size() == 3
    
    # Undo last 2 actions
    undone = logger.undo_last_n_actions(2)
    assert len(undone) == 2
    assert undone == ["move", "delete"]
    assert logger.get_history_size() == 1
    
    # Check that undo functions were called in reverse order
    assert len(undo_calls) == 2
    assert undo_calls[0] == "undo_move_0_to_3"
    assert undo_calls[1] == "undo_delete_2"


def test_undo_more_than_available():
    """Test undoing more actions than available."""
    logger = ActionLogger()
    
    def dummy_undo():
        pass
    
    # Log only 2 actions
    logger.log_action("add", dummy_undo)
    logger.log_action("delete", dummy_undo)
    
    # Try to undo 5 actions (more than available)
    undone = logger.undo_last_n_actions(5)
    assert len(undone) == 2
    assert undone == ["delete", "add"]
    assert logger.get_history_size() == 0


def test_clear_history():
    """Test clearing all actions from history."""
    logger = ActionLogger()
    
    def dummy_undo():
        pass
    
    # Log some actions
    logger.log_action("add", dummy_undo)
    logger.log_action("delete", dummy_undo)
    logger.log_action("move", dummy_undo)
    
    assert logger.get_history_size() == 3
    
    # Clear history
    logger.clear_history()
    assert logger.get_history_size() == 0
    assert logger.get_action_history() == []


def test_max_history_limit():
    """Test that history respects maximum size limit."""
    # Create logger with small history limit
    logger = ActionLogger(max_history=3)
    
    def dummy_undo():
        pass
    
    # Log more actions than the limit
    logger.log_action("add1", dummy_undo)
    logger.log_action("add2", dummy_undo)
    logger.log_action("add3", dummy_undo)
    logger.log_action("add4", dummy_undo)  # This should evict the oldest action
    
    assert logger.get_history_size() == 3
    history = logger.get_action_history()
    assert history == ["add2", "add3", "add4"]


def test_set_max_history():
    """Test changing the maximum history size."""
    logger = ActionLogger(max_history=5)
    
    def dummy_undo():
        pass
    
    # Log some actions
    for i in range(7):
        logger.log_action(f"action{i}", dummy_undo)
    
    # Should have only the last 5 actions due to maxlen
    assert logger.get_history_size() == 5
    history = logger.get_action_history()
    assert history == ["action2", "action3", "action4", "action5", "action6"]
    
    # Reduce max history
    logger.set_max_history(3)
    assert logger.get_history_size() == 3
    history = logger.get_action_history()
    assert history == ["action4", "action5", "action6"]
    
    # Increase max history
    logger.set_max_history(10)
    assert logger.get_history_size() == 3  # Size shouldn't change, just capacity
    history = logger.get_action_history()
    assert history == ["action4", "action5", "action6"]


def test_invalid_max_history():
    """Test setting invalid maximum history size."""
    logger = ActionLogger()
    
    with pytest.raises(ValueError):
        logger.set_max_history(0)
    
    with pytest.raises(ValueError):
        logger.set_max_history(-1)


if __name__ == "__main__":
    pytest.main([__file__])