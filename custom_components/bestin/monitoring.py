"""Performance monitoring and health checks for BESTIN integration."""
import asyncio
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from .const import LOGGER


@dataclass
class ComponentMetrics:
    """Component performance metrics."""
    
    connection_attempts: int = 0
    successful_connections: int = 0
    failed_connections: int = 0
    
    commands_sent: int = 0
    commands_successful: int = 0
    commands_failed: int = 0
    
    average_response_time: float = 0.0
    last_error: Optional[str] = None
    last_error_time: Optional[datetime] = None
    
    uptime_start: datetime = field(default_factory=datetime.now)
    
    @property
    def connection_success_rate(self) -> float:
        """Calculate connection success rate."""
        if self.connection_attempts == 0:
            return 0.0
        return (self.successful_connections / self.connection_attempts) * 100
    
    @property
    def command_success_rate(self) -> float:
        """Calculate command success rate."""
        if self.commands_sent == 0:
            return 0.0
        return (self.commands_successful / self.commands_sent) * 100
    
    @property
    def uptime(self) -> timedelta:
        """Calculate uptime."""
        return datetime.now() - self.uptime_start
    
    def record_connection_attempt(self, success: bool) -> None:
        """Record a connection attempt."""
        self.connection_attempts += 1
        if success:
            self.successful_connections += 1
        else:
            self.failed_connections += 1
    
    def record_command(self, success: bool, response_time: float = 0.0, error: Optional[str] = None) -> None:
        """Record a command execution."""
        self.commands_sent += 1
        if success:
            self.commands_successful += 1
            # Update rolling average response time
            if self.commands_successful == 1:
                self.average_response_time = response_time
            else:
                self.average_response_time = (
                    (self.average_response_time * (self.commands_successful - 1) + response_time)
                    / self.commands_successful
                )
        else:
            self.commands_failed += 1
            if error:
                self.last_error = error
                self.last_error_time = datetime.now()


class BestinMonitor:
    """Monitor BESTIN integration health and performance."""
    
    def __init__(self, hass: HomeAssistant, hub_id: str):
        """Initialize the monitor."""
        self.hass = hass
        self.hub_id = hub_id
        self.metrics = ComponentMetrics()
        self._monitoring_task: Optional[asyncio.Task] = None
        self._health_check_interval = timedelta(minutes=5)
        
    async def start(self) -> None:
        """Start monitoring."""
        LOGGER.info(f"Starting performance monitoring for {self.hub_id}")
        
        # Schedule periodic health checks
        self._monitoring_task = self.hass.bus.async_listen(
            EVENT_HOMEASSISTANT_STOP, self._stop_monitoring
        )
        
        # Track health checks every 5 minutes
        async_track_time_interval(
            self.hass, 
            self._periodic_health_check, 
            self._health_check_interval
        )
    
    @callback
    async def _stop_monitoring(self, event) -> None:
        """Stop monitoring."""
        if self._monitoring_task:
            self._monitoring_task.cancel()
        LOGGER.info(f"Stopped monitoring for {self.hub_id}")
    
    async def _periodic_health_check(self, now) -> None:
        """Perform periodic health check."""
        health_status = self.get_health_status()
        
        # Log health summary
        LOGGER.info(
            f"Health Check - {self.hub_id}: "
            f"Conn: {health_status['connection_health']:.1f}%, "
            f"Cmd: {health_status['command_health']:.1f}%, "
            f"Uptime: {health_status['uptime']}"
        )
        
        # Log warnings for poor performance
        if health_status['connection_health'] < 90:
            LOGGER.warning(f"Poor connection health for {self.hub_id}: {health_status['connection_health']:.1f}%")
        
        if health_status['command_health'] < 95:
            LOGGER.warning(f"Poor command success rate for {self.hub_id}: {health_status['command_health']:.1f}%")
        
        if health_status['avg_response_time'] > 2000:  # 2 seconds
            LOGGER.warning(f"Slow response time for {self.hub_id}: {health_status['avg_response_time']:.1f}ms")
    
    def record_connection_attempt(self, success: bool) -> None:
        """Record a connection attempt."""
        self.metrics.record_connection_attempt(success)
        
        if not success:
            LOGGER.debug(f"Connection failed for {self.hub_id}")
    
    def record_command_execution(self, success: bool, response_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """Record command execution metrics."""
        start_time = time.time()
        actual_response_time = response_time or ((time.time() - start_time) * 1000)  # Convert to ms
        
        self.metrics.record_command(success, actual_response_time, error)
        
        if not success:
            LOGGER.debug(f"Command failed for {self.hub_id}: {error}")
        elif actual_response_time > 1000:  # Log slow responses
            LOGGER.debug(f"Slow command response for {self.hub_id}: {actual_response_time:.1f}ms")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        return {
            "hub_id": self.hub_id,
            "connection_health": self.metrics.connection_success_rate,
            "command_health": self.metrics.command_success_rate,
            "avg_response_time": self.metrics.average_response_time,
            "total_connections": self.metrics.connection_attempts,
            "total_commands": self.metrics.commands_sent,
            "uptime": str(self.metrics.uptime),
            "last_error": self.metrics.last_error,
            "last_error_time": self.metrics.last_error_time.isoformat() if self.metrics.last_error_time else None,
        }
    
    def get_prometheus_metrics(self) -> str:
        """Generate Prometheus-style metrics for external monitoring."""
        metrics = []
        
        metrics.append(f'bestin_connection_attempts_total{{hub_id="{self.hub_id}"}} {self.metrics.connection_attempts}')
        metrics.append(f'bestin_connection_success_total{{hub_id="{self.hub_id}"}} {self.metrics.successful_connections}')
        metrics.append(f'bestin_connection_failures_total{{hub_id="{self.hub_id}"}} {self.metrics.failed_connections}')
        
        metrics.append(f'bestin_commands_sent_total{{hub_id="{self.hub_id}"}} {self.metrics.commands_sent}')
        metrics.append(f'bestin_commands_success_total{{hub_id="{self.hub_id}"}} {self.metrics.commands_successful}')
        metrics.append(f'bestin_commands_failed_total{{hub_id="{self.hub_id}"}} {self.metrics.commands_failed}')
        
        metrics.append(f'bestin_response_time_avg_ms{{hub_id="{self.hub_id}"}} {self.metrics.average_response_time}')
        metrics.append(f'bestin_uptime_seconds{{hub_id="{self.hub_id}"}} {self.metrics.uptime.total_seconds()}')
        
        return '\n'.join(metrics)