"""
Base Agent Class for MisterHR AI Agents

All agents inherit from this base class which provides:
- Common LangChain integration
- Error handling and logging
- Configuration management
- Performance tracking
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union
import logging
import time
from datetime import datetime
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentConfig(BaseModel):
    """Base configuration for all agents."""
    name: str
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 60

class AgentMetrics(BaseModel):
    """Performance metrics for agent operations."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    average_response_time: float = 0.0
    last_call_time: Optional[datetime] = None

class BaseAgent(ABC):
    """
    Abstract base class for all MisterHR AI agents.

    This class provides:
    - LangChain integration setup
    - Error handling and retries
    - Response validation
    - Metrics collection
    - Configuration management
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.metrics = AgentMetrics()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Initialize LLM (will be set up during orchestration)
        self.llm = None

        self.logger.info(f"Initialized agent: {self.config.name}")

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the agent's primary function.

        Args:
            **kwargs: Agent-specific parameters

        Returns:
            Dict containing agent results
        """
        pass

    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """
        Validate input parameters for this agent.

        Returns:
            bool: True if valid, False if invalid
        """
        pass

    async def _execute_with_metrics(self, **kwargs) -> Dict[str, Any]:
        """
        Execute agent operation with performance tracking.

        Returns:
            Dict with results and metadata
        """
        start_time = time.time()
        call_id = f"{self.config.name}_{int(start_time)}"

        try:
            # Validate input
            if not self.validate_input(**kwargs):
                raise ValueError("Invalid input parameters")

            # Execute agent logic
            result = await self.execute(**kwargs)

            # Update metrics
            execution_time = time.time() - start_time
            self._update_metrics(success=True, execution_time=execution_time)

            self.logger.info(f"Agent {self.config.name} completed successfully in {execution_time:.2f}s")

            return {
                "success": True,
                "data": result,
                "metadata": {
                    "agent": self.config.name,
                    "call_id": call_id,
                    "execution_time": execution_time,
                    "timestamp": datetime.now()
                }
            }

        except Exception as e:
            execution_time = time.time() - start_time
            self._update_metrics(success=False, execution_time=execution_time)

            error_msg = f"Agent {self.config.name} failed: {str(e)}"
            self.logger.error(error_msg)

            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "agent": self.config.name,
                    "call_id": call_id,
                    "execution_time": execution_time,
                    "timestamp": datetime.now(),
                    "error_type": type(e).__name__
                }
            }

    def _update_metrics(self, success: bool, execution_time: float):
        """Update performance metrics."""
        self.metrics.total_calls += 1

        if success:
            self.metrics.successful_calls += 1
        else:
            self.metrics.failed_calls += 1

        # Update average response time (running average)
        if self.metrics.total_calls == 1:
            self.metrics.average_response_time = execution_time
        else:
            self.metrics.average_response_time = (
                (self.metrics.average_response_time * (self.metrics.total_calls - 1)) +
                execution_time
            ) / self.metrics.total_calls

        self.metrics.last_call_time = datetime.now()

    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health and performance status."""
        success_rate = (
            self.metrics.successful_calls / self.metrics.total_calls
            if self.metrics.total_calls > 0 else 0
        )

        return {
            "agent_name": self.config.name,
            "status": "healthy" if success_rate >= 0.8 else "degraded",
            "success_rate": success_rate,
            "total_calls": self.metrics.total_calls,
            "average_response_time": self.metrics.average_response_time,
            "last_call": self.metrics.last_call_time
        }

    def reset_metrics(self):
        """Reset performance metrics."""
        self.metrics = AgentMetrics()
        self.logger.info(f"Metrics reset for agent: {self.config.name}")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass
