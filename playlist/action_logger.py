"""
Action Logger module for PlayWise Music Engine.

Implements the Command pattern and stack-based undo functionality for playlist edits.
"""

from typing import List, Any, Callable
from collections import deque


class Action:
    """
    Represents a reversible playlist action.
    
    Time Complexity:
        - All operations: O(1)
    
    Space Complexity:
        - O(1) for the action object itself
        - Additional space depends on the data stored in action_params
    """
    
    def __init__(self, action_type: str, undo_func: Callable, action_params: dict):
        """
        Initialize an action.
        
        Args:
            action_type (str): Type of action (e.g., 'add', 'delete', 'move')
            undo_func (Callable): Function to execute for undoing this action
            action_params (dict): Parameters needed to execute the undo function
        """
        self.action_type = action_type
        self.undo_func = undo_func
        self.action_params = action_params


class ActionLogger:
    """
    Manages a stack of reversible actions for playlist edits using the Command pattern.
    
    Uses a stack (deque with maxlen) for O(1) push/pop operations.
    
    Time Complexity:
        - log_action: O(1)
        - undo_last_n_actions: O(n) where n is the number of actions to undo
        - get_action_history: O(k) where k is the number of actions in history
        - clear_history: O(1)
    
    Space Complexity:
        - O(n) where n is the number of actions in the history stack
    """
    
    def __init__(self, max_history: int = 50):
        """
        Initialize the action logger with a maximum history size.
        
        Args:
            max_history (int): Maximum number of actions to keep in history (default: 50)
        """
        self._action_history = deque(maxlen=max_history)
        self._max_history = max_history
    
    def log_action(self, action_type: str, undo_func: Callable, **kwargs) -> None:
        """
        Log a reversible action.
        
        Time Complexity: O(1) amortized
        Space Complexity: O(1) for the action object
        
        Args:
            action_type (str): Type of action (e.g., 'add', 'delete', 'move')
            undo_func (Callable): Function to execute for undoing this action
            **kwargs: Parameters needed to execute the undo function
        """
        action = Action(action_type, undo_func, kwargs)
        self._action_history.append(action)
    
    def undo_last_n_actions(self, n: int) -> List[str]:
        """
        Undo the last N actions.
        
        Time Complexity: O(n) where n is the number of actions to undo
        Space Complexity: O(n) for the result list
        
        Args:
            n (int): Number of actions to undo
            
        Returns:
            List[str]: List of action types that were undone
        """
        if n <= 0:
            return []
        
        # Limit n to the actual number of available actions
        n = min(n, len(self._action_history))
        
        undone_actions = []
        for _ in range(n):
            if self._action_history:
                action = self._action_history.pop()
                # Execute the undo function with its parameters
                action.undo_func(**action.action_params)
                undone_actions.append(action.action_type)
        
        return undone_actions
    
    def get_action_history(self) -> List[str]:
        """
        Get a list of action types in the current history (oldest to newest).
        
        Time Complexity: O(k) where k is the number of actions in history
        Space Complexity: O(k) for the returned list
        
        Returns:
            List[str]: List of action types in chronological order
        """
        return [action.action_type for action in self._action_history]
    
    def clear_history(self) -> None:
        """
        Clear all actions from the history.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._action_history.clear()
    
    def get_history_size(self) -> int:
        """
        Get the current number of actions in the history.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Returns:
            int: Number of actions in history
        """
        return len(self._action_history)
    
    def set_max_history(self, max_history: int) -> None:
        """
        Set a new maximum history size.
        
        Time Complexity: O(min(current_size, new_size))
        Space Complexity: O(min(current_size, new_size))
        
        Args:
            max_history (int): New maximum history size
        """
        if max_history <= 0:
            raise ValueError("max_history must be positive")
        
        # Create a new deque with the new maxlen
        new_history = deque(maxlen=max_history)
        
        # Copy existing actions, respecting the new maxlen
        # If new maxlen is smaller, only copy the most recent actions
        if len(self._action_history) > max_history:
            # Keep only the most recent max_history actions
            actions_to_keep = list(self._action_history)[-max_history:]
            new_history.extend(actions_to_keep)
        else:
            # Copy all actions
            new_history.extend(self._action_history)
        
        self._action_history = new_history
        self._max_history = max_history