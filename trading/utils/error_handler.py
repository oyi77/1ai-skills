"""
Error handling utilities for the trading system.

This module provides decorators and utilities for robust error handling,
including retry logic with exponential backoff and jitter.
"""

import functools
import logging
import random
import time
from typing import Callable, Optional, Type, Tuple, Union

# Configure logger
logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    backoff: float = 1.0,
    exponential_jitter: bool = True,
    exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """Retry decorator with exponential backoff and jitter.
    
    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        backoff: Initial wait time in seconds between retries (default: 1.0)
        exponential_jitter: Whether to use exponential backoff with jitter (default: True)
        exceptions: Tuple of exception types to catch and retry on (default: all exceptions)
        on_retry: Optional callback function called on each retry with (exception, attempt_number)
    
    Returns:
        Decorator function that wraps the target function with retry logic
    
    Example:
        @retry(max_attempts=3, backoff=1.0)
        def some_function():
            # This will retry up to 3 times with exponential backoff
            pass
    """
    if exceptions is None:
        exceptions = (Exception,)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_exception = None
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    last_exception = e
                    
                    if attempt >= max_attempts:
                        # Max attempts reached, re-raise the last exception
                        logger.error(
                            f"Function '{func.__name__}' failed after {max_attempts} attempts. "
                            f"Last error: {type(e).__name__}: {e}"
                        )
                        raise
                    
                    # Calculate wait time
                    if exponential_jitter:
                        # Exponential backoff: backoff * 2^(attempt-1) + random jitter
                        wait_time = backoff * (2 ** (attempt - 1))
                        # Add jitter: ±25% of wait time
                        jitter = wait_time * 0.25 * random.uniform(-1, 1)
                        wait_time = max(0, wait_time + jitter)
                    else:
                        wait_time = backoff
                    
                    # Log retry attempt
                    logger.warning(
                        f"Function '{func.__name__}' failed (attempt {attempt}/{max_attempts}). "
                        f"Error: {type(e).__name__}: {e}. "
                        f"Retrying in {wait_time:.2f} seconds..."
                    )
                    
                    # Call optional retry callback
                    if on_retry:
                        try:
                            on_retry(e, attempt)
                        except Exception as callback_error:
                            logger.warning(f"Retry callback failed: {callback_error}")
                    
                    # Wait before next attempt
                    time.sleep(wait_time)
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
            return None
        
        # Store retry configuration on the wrapper for introspection
        wrapper._retry_config = {
            'max_attempts': max_attempts,
            'backoff': backoff,
            'exponential_jitter': exponential_jitter,
            'exceptions': exceptions
        }
        
        return wrapper
    
    return decorator


class RetryContext:
    """Context manager for retry logic around code blocks.
    
    Example:
        with RetryContext(max_attempts=3):
            # Code that might fail
            risky_operation()
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        backoff: float = 1.0,
        exponential_jitter: bool = True,
        exceptions: Optional[Tuple[Type[Exception], ...]] = None
    ):
        self.max_attempts = max_attempts
        self.backoff = backoff
        self.exponential_jitter = exponential_jitter
        self.exceptions = exceptions or (Exception,)
        self.attempt = 0
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True
        
        if not issubclass(exc_type, self.exceptions):
            return False
        
        self.attempt += 1
        
        if self.attempt >= self.max_attempts:
            logger.error(f"Max attempts ({self.max_attempts}) reached. Giving up.")
            return False
        
        # Calculate wait time
        if self.exponential_jitter:
            wait_time = self.backoff * (2 ** (self.attempt - 1))
            jitter = wait_time * 0.25 * random.uniform(-1, 1)
            wait_time = max(0, wait_time + jitter)
        else:
            wait_time = self.backoff
        
        logger.warning(
            f"Attempt {self.attempt}/{self.max_attempts} failed: {exc_val}. "
            f"Retrying in {wait_time:.2f} seconds..."
        )
        
        time.sleep(wait_time)
        
        # Suppress the exception and allow retry
        return True
