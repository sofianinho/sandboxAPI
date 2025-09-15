import random
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum

class NetworkEventType(Enum):
    TRAFFIC_SPIKE = "traffic_spike"
    HARDWARE_FAILURE = "hardware_failure"
    MAINTENANCE = "maintenance"
    CAPACITY_ISSUE = "capacity_issue"
    ENVIRONMENTAL = "environmental"
    CONFIGURATION_CHANGE = "configuration_change"

@dataclass
class NetworkEvent:
    event_id: str
    event_type: NetworkEventType
    timestamp: datetime
    affected_components: List[str]
    severity: str  # low, medium, high, critical
    duration_hours: float
    impact_metrics: Dict[str, float]
    description: str
    resolution_status: str = "active"  # active, resolved, escalated

@dataclass
class ComponentState:
    component_id: str
    component_type: str
    region_id: str
    health_score: float = 100.0
    last_maintenance: datetime = field(default_factory=datetime.utcnow)
    failure_probability: float = 0.01
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    active_events: List[str] = field(default_factory=list)
    degradation_rate: float = 0.1  # Health score degradation per day

@dataclass
class RegionState:
    region_id: str
    name: str
    base_stations: int
    connected_devices: int
    current_load: float = 0.5
    traffic_pattern: str = "normal"  # normal, peak, low, maintenance
    environmental_factors: Dict[str, Any] = field(default_factory=dict)
    active_incidents: List[str] = field(default_factory=list)

class NetworkStateManager:
    def __init__(self):
        self.current_time = datetime.utcnow()
        self.regions = self._initialize_regions()
        self.components = self._initialize_components()
        self.active_events = {}
        self.event_history = []
        self.state_lock = threading.Lock()
        self.simulation_running = False
        self._start_simulation()

    def _initialize_regions(self) -> Dict[str, RegionState]:
        regions = {
            "region-northwest-01": RegionState(
                region_id="region-northwest-01",
                name="Pacific Northwest",
                base_stations=127,
                connected_devices=234891,
                current_load=0.67,
                environmental_factors={"weather": "cloudy", "temperature": 15.5}
            ),
            "region-northeast-02": RegionState(
                region_id="region-northeast-02",
                name="New England",
                base_stations=156,
                connected_devices=398456,
                current_load=0.72,
                environmental_factors={"weather": "clear", "temperature": 8.2}
            ),
            "region-southwest-03": RegionState(
                region_id="region-southwest-03",
                name="Southwest",
                base_stations=189,
                connected_devices=567234,
                current_load=0.58,
                environmental_factors={"weather": "sunny", "temperature": 28.7}
            ),
            "region-southeast-04": RegionState(
                region_id="region-southeast-04",
                name="Southeast",
                base_stations=201,
                connected_devices=645123,
                current_load=0.69,
                environmental_factors={"weather": "humid", "temperature": 24.1}
            ),
            "region-central-05": RegionState(
                region_id="region-central-05",
                name="Central Plains",
                base_stations=98,
                connected_devices=123789,
                current_load=0.43,
                environmental_factors={"weather": "windy", "temperature": 12.8}
            ),
            "region-west-06": RegionState(
                region_id="region-west-06",
                name="West Coast",
                base_stations=234,
                connected_devices=789456,
                current_load=0.81,
                environmental_factors={"weather": "foggy", "temperature": 18.3}
            )
        }
        return regions

    def _initialize_components(self) -> Dict[str, ComponentState]:
        components = {}

        # Base stations
        for i in range(50):
            region_id = random.choice(list(self.regions.keys()))
            components[f"base-station-{region_id[-2:]}-{i+1:03d}"] = ComponentState(
                component_id=f"base-station-{region_id[-2:]}-{i+1:03d}",
                component_type="base_station",
                region_id=region_id,
                health_score=random.uniform(85, 100),
                last_maintenance=datetime.utcnow() - timedelta(days=random.randint(1, 180)),
                failure_probability=random.uniform(0.01, 0.05),
                performance_metrics={
                    "uptime_hours": random.uniform(1000, 8760),
                    "error_count_24h": random.randint(0, 10),
                    "temperature_celsius": random.uniform(35, 50),
                    "power_consumption_watts": random.uniform(150, 300)
                },
                degradation_rate=random.uniform(0.05, 0.15)
            )

        # Core nodes
        for i in range(12):
            region_id = random.choice(list(self.regions.keys()))
            components[f"core-node-{region_id[-2:]}-{i+1:02d}"] = ComponentState(
                component_id=f"core-node-{region_id[-2:]}-{i+1:02d}",
                component_type="core_node",
                region_id=region_id,
                health_score=random.uniform(90, 100),
                last_maintenance=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
                failure_probability=random.uniform(0.005, 0.02),
                performance_metrics={
                    "uptime_hours": random.uniform(2000, 8760),
                    "error_count_24h": random.randint(0, 5),
                    "temperature_celsius": random.uniform(40, 60),
                    "power_consumption_watts": random.uniform(500, 1000)
                },
                degradation_rate=random.uniform(0.02, 0.08)
            )

        # Edge compute nodes
        for i in range(25):
            region_id = random.choice(list(self.regions.keys()))
            components[f"edge-compute-{region_id[-2:]}-{i+1:02d}"] = ComponentState(
                component_id=f"edge-compute-{region_id[-2:]}-{i+1:02d}",
                component_type="edge_compute",
                region_id=region_id,
                health_score=random.uniform(80, 100),
                last_maintenance=datetime.utcnow() - timedelta(days=random.randint(1, 120)),
                failure_probability=random.uniform(0.02, 0.08),
                performance_metrics={
                    "uptime_hours": random.uniform(500, 5000),
                    "error_count_24h": random.randint(0, 15),
                    "temperature_celsius": random.uniform(30, 70),
                    "power_consumption_watts": random.uniform(200, 500)
                },
                degradation_rate=random.uniform(0.08, 0.20)
            )

        return components

    def _start_simulation(self):
        """Start the background simulation thread"""
        if not self.simulation_running:
            self.simulation_running = True
            simulation_thread = threading.Thread(target=self._simulation_loop, daemon=True)
            simulation_thread.start()

    def _simulation_loop(self):
        """Background simulation loop that evolves network state"""
        while self.simulation_running:
            try:
                self._evolve_state()
                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                print(f"Simulation error: {e}")
                time.sleep(60)  # Wait longer on error

    def _evolve_state(self):
        """Evolve the network state over time"""
        with self.state_lock:
            current_time = datetime.utcnow()
            time_delta = current_time - self.current_time

            if time_delta.total_seconds() < 10:  # Don't update too frequently
                return

            # Update component health scores
            self._update_component_health(time_delta)

            # Update region loads based on time of day
            self._update_region_loads(current_time)

            # Generate random events
            self._generate_random_events(current_time)

            # Resolve expired events
            self._resolve_expired_events(current_time)

            # Update environmental factors
            self._update_environmental_factors(current_time)

            self.current_time = current_time

    def _update_component_health(self, time_delta: timedelta):
        """Update component health scores based on time passage"""
        hours_passed = time_delta.total_seconds() / 3600

        for component in self.components.values():
            # Natural degradation
            health_loss = component.degradation_rate * hours_passed / 24  # Per day rate
            component.health_score = max(0, component.health_score - health_loss)

            # Update failure probability based on health
            if component.health_score < 50:
                component.failure_probability = min(0.9, component.failure_probability * 1.1)
            elif component.health_score > 90:
                component.failure_probability = max(0.001, component.failure_probability * 0.99)

            # Update performance metrics
            self._update_component_metrics(component)

    def _update_component_metrics(self, component: ComponentState):
        """Update performance metrics for a component"""
        # Temperature varies with load and health
        base_temp = {"base_station": 40, "core_node": 50, "edge_compute": 45}.get(component.component_type, 40)
        health_factor = (100 - component.health_score) / 100
        temp_variation = random.uniform(-5, 15) * (1 + health_factor)
        component.performance_metrics["temperature_celsius"] = max(20, base_temp + temp_variation)

        # Error count increases with poor health
        base_errors = random.randint(0, 3)
        health_errors = int(health_factor * random.randint(0, 20))
        component.performance_metrics["error_count_24h"] = base_errors + health_errors

        # Power consumption varies with temperature and load
        base_power = {"base_station": 200, "core_node": 750, "edge_compute": 350}.get(component.component_type, 200)
        power_variation = random.uniform(-50, 100) * (1 + health_factor)
        component.performance_metrics["power_consumption_watts"] = max(50, base_power + power_variation)

    def _update_region_loads(self, current_time: datetime):
        """Update region loads based on time of day patterns"""
        hour = current_time.hour

        # Peak hours: 8-10 AM, 6-9 PM
        # Low hours: 11 PM - 6 AM
        if 8 <= hour <= 10 or 18 <= hour <= 21:
            pattern = "peak"
            load_multiplier = random.uniform(1.2, 1.5)
        elif 23 <= hour or hour <= 6:
            pattern = "low"
            load_multiplier = random.uniform(0.4, 0.7)
        else:
            pattern = "normal"
            load_multiplier = random.uniform(0.8, 1.1)

        for region in self.regions.values():
            region.traffic_pattern = pattern
            base_load = 0.6  # Base load level

            # Add some randomness and regional variation
            region_factor = random.uniform(0.9, 1.1)
            noise = random.uniform(-0.1, 0.1)

            new_load = min(0.99, max(0.1, base_load * load_multiplier * region_factor + noise))
            region.current_load = new_load

    def _generate_random_events(self, current_time: datetime):
        """Generate random network events"""
        # Low probability of generating new events
        if random.random() < 0.05:  # 5% chance per update cycle
            event_type = random.choice(list(NetworkEventType))

            # Select affected components
            num_affected = random.randint(1, 3)
            affected_components = random.sample(list(self.components.keys()), num_affected)

            # Generate event
            event = NetworkEvent(
                event_id=f"event-{int(current_time.timestamp())}",
                event_type=event_type,
                timestamp=current_time,
                affected_components=affected_components,
                severity=random.choice(["low", "medium", "high", "critical"]),
                duration_hours=random.uniform(0.5, 8.0),
                impact_metrics=self._generate_event_impact(event_type),
                description=self._get_event_description(event_type)
            )

            self.active_events[event.event_id] = event

            # Update affected components
            for comp_id in affected_components:
                if comp_id in self.components:
                    self.components[comp_id].active_events.append(event.event_id)
                    # Apply immediate impact
                    if event.severity == "critical":
                        self.components[comp_id].health_score *= 0.7
                    elif event.severity == "high":
                        self.components[comp_id].health_score *= 0.85
                    elif event.severity == "medium":
                        self.components[comp_id].health_score *= 0.95

    def _generate_event_impact(self, event_type: NetworkEventType) -> Dict[str, float]:
        """Generate impact metrics for an event"""
        impact = {}

        if event_type == NetworkEventType.TRAFFIC_SPIKE:
            impact.update({
                "latency_increase_percent": random.uniform(10, 50),
                "throughput_decrease_percent": random.uniform(5, 25),
                "cpu_increase_percent": random.uniform(20, 60)
            })
        elif event_type == NetworkEventType.HARDWARE_FAILURE:
            impact.update({
                "availability_impact_percent": random.uniform(30, 100),
                "performance_degradation_percent": random.uniform(40, 80),
                "error_rate_increase_percent": random.uniform(100, 500)
            })
        elif event_type == NetworkEventType.CAPACITY_ISSUE:
            impact.update({
                "throughput_decrease_percent": random.uniform(15, 40),
                "latency_increase_percent": random.uniform(20, 80),
                "packet_loss_increase_percent": random.uniform(1, 10)
            })

        return impact

    def _get_event_description(self, event_type: NetworkEventType) -> str:
        """Get description for an event type"""
        descriptions = {
            NetworkEventType.TRAFFIC_SPIKE: "Unexpected traffic surge detected",
            NetworkEventType.HARDWARE_FAILURE: "Hardware component failure detected",
            NetworkEventType.MAINTENANCE: "Scheduled maintenance window active",
            NetworkEventType.CAPACITY_ISSUE: "Network capacity threshold exceeded",
            NetworkEventType.ENVIRONMENTAL: "Environmental factors affecting performance",
            NetworkEventType.CONFIGURATION_CHANGE: "Configuration update applied"
        }
        return descriptions.get(event_type, "Network event detected")

    def _resolve_expired_events(self, current_time: datetime):
        """Resolve events that have exceeded their duration"""
        expired_events = []

        for event in self.active_events.values():
            if (current_time - event.timestamp).total_seconds() / 3600 > event.duration_hours:
                expired_events.append(event.event_id)

        for event_id in expired_events:
            event = self.active_events.pop(event_id)
            event.resolution_status = "resolved"
            self.event_history.append(event)

            # Remove event from affected components
            for comp_id in event.affected_components:
                if comp_id in self.components and event_id in self.components[comp_id].active_events:
                    self.components[comp_id].active_events.remove(event_id)

    def _update_environmental_factors(self, current_time: datetime):
        """Update environmental factors that affect network performance"""
        for region in self.regions.values():
            # Simulate weather changes
            weather_options = ["clear", "cloudy", "rainy", "stormy", "foggy", "sunny"]
            if random.random() < 0.1:  # 10% chance to change weather
                region.environmental_factors["weather"] = random.choice(weather_options)

            # Simulate temperature variations
            current_temp = region.environmental_factors.get("temperature", 20)
            temp_change = random.uniform(-2, 2)
            new_temp = max(-10, min(40, current_temp + temp_change))
            region.environmental_factors["temperature"] = new_temp

    def get_network_health_summary(self) -> Dict[str, Any]:
        """Get overall network health summary"""
        with self.state_lock:
            total_components = len(self.components)
            healthy_components = sum(1 for c in self.components.values() if c.health_score > 80)

            avg_health = sum(c.health_score for c in self.components.values()) / total_components
            active_incidents = len(self.active_events)

            return {
                "timestamp": self.current_time.isoformat(),
                "total_components": total_components,
                "healthy_components": healthy_components,
                "average_health_score": avg_health,
                "active_incidents": active_incidents,
                "regions_status": {r.region_id: r.current_load for r in self.regions.values()}
            }

    def get_component_by_id(self, component_id: str) -> ComponentState:
        """Get component state by ID"""
        with self.state_lock:
            return self.components.get(component_id)

    def get_region_by_id(self, region_id: str) -> RegionState:
        """Get region state by ID"""
        with self.state_lock:
            return self.regions.get(region_id)

    def get_active_events(self) -> List[NetworkEvent]:
        """Get list of active events"""
        with self.state_lock:
            return list(self.active_events.values())

    def get_recent_events(self, hours: int = 24) -> List[NetworkEvent]:
        """Get events from the last N hours"""
        with self.state_lock:
            cutoff_time = self.current_time - timedelta(hours=hours)
            recent_events = [
                event for event in self.event_history
                if event.timestamp >= cutoff_time
            ]
            # Add active events
            recent_events.extend(self.active_events.values())
            return sorted(recent_events, key=lambda x: x.timestamp, reverse=True)

    def trigger_maintenance(self, component_id: str):
        """Trigger maintenance for a component (restores health)"""
        with self.state_lock:
            if component_id in self.components:
                component = self.components[component_id]
                component.health_score = min(100, component.health_score + random.uniform(20, 40))
                component.last_maintenance = self.current_time
                component.failure_probability = max(0.001, component.failure_probability * 0.5)

    def stop_simulation(self):
        """Stop the background simulation"""
        self.simulation_running = False