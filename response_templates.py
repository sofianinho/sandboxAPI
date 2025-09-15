import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models import *

class ResponseTemplateManager:
    def __init__(self):
        self.scenario_index = 0
        self.base_time = datetime.utcnow()
        self.regions = [
            "region-northwest-01", "region-northeast-02", "region-southwest-03",
            "region-southeast-04", "region-central-05", "region-west-06"
        ]
        self.components = [
            "base-station-downtown-001", "base-station-suburbs-002", "core-node-alpha-001",
            "edge-compute-beta-001", "router-gamma-001", "switch-delta-001"
        ]

    def _rotate_scenario(self):
        self.scenario_index = (self.scenario_index + 1) % 5
        return self.scenario_index

    def _get_random_region(self):
        return random.choice(self.regions)

    def _get_random_component(self):
        return random.choice(self.components)

    def _get_time_offset(self, minutes=0, hours=0, days=0):
        return self.base_time + timedelta(minutes=minutes, hours=hours, days=days)

    # Network Status Templates
    def get_network_status_response(self) -> NetworkStatus:
        scenario = self._rotate_scenario()
        scenarios = [
            # Scenario 0: Excellent Health
            {
                "overall_health": HealthStatus.excellent,
                "uptime_percentage": 99.98,
                "active_regions": 6,
                "total_base_stations": 1547,
                "connected_devices": 2847291,
                "current_throughput_gbps": 847.3,
                "prediction_confidence": 0.95
            },
            # Scenario 1: Good with Minor Issues
            {
                "overall_health": HealthStatus.good,
                "uptime_percentage": 99.85,
                "active_regions": 6,
                "total_base_stations": 1543,
                "connected_devices": 2834567,
                "current_throughput_gbps": 823.7,
                "prediction_confidence": 0.87
            },
            # Scenario 2: Degraded Performance
            {
                "overall_health": HealthStatus.degraded,
                "uptime_percentage": 98.92,
                "active_regions": 5,
                "total_base_stations": 1489,
                "connected_devices": 2675432,
                "current_throughput_gbps": 756.4,
                "prediction_confidence": 0.73
            },
            # Scenario 3: Maintenance Window
            {
                "overall_health": HealthStatus.good,
                "uptime_percentage": 99.45,
                "active_regions": 6,
                "total_base_stations": 1523,
                "connected_devices": 2789456,
                "current_throughput_gbps": 812.9,
                "prediction_confidence": 0.91
            },
            # Scenario 4: Critical Issues
            {
                "overall_health": HealthStatus.critical,
                "uptime_percentage": 95.67,
                "active_regions": 4,
                "total_base_stations": 1342,
                "connected_devices": 2234567,
                "current_throughput_gbps": 634.2,
                "prediction_confidence": 0.65
            }
        ]

        data = scenarios[scenario]
        data["last_updated"] = self._get_time_offset(minutes=-random.randint(1, 5))
        return NetworkStatus(**data)

    def get_regions_response(self):
        scenario = self._rotate_scenario()

        base_regions = [
            {"region_id": "region-northwest-01", "name": "Pacific Northwest", "base_stations": 127, "connected_devices": 234891},
            {"region_id": "region-northeast-02", "name": "New England", "base_stations": 156, "connected_devices": 398456},
            {"region_id": "region-southwest-03", "name": "Southwest", "base_stations": 189, "connected_devices": 567234},
            {"region_id": "region-southeast-04", "name": "Southeast", "base_stations": 201, "connected_devices": 645123},
            {"region_id": "region-central-05", "name": "Central Plains", "base_stations": 98, "connected_devices": 123789},
            {"region_id": "region-west-06", "name": "West Coast", "base_stations": 234, "connected_devices": 789456}
        ]

        status_scenarios = [
            [RegionStatus.operational] * 6,  # All operational
            [RegionStatus.operational, RegionStatus.operational, RegionStatus.degraded, RegionStatus.operational, RegionStatus.operational, RegionStatus.operational],
            [RegionStatus.operational, RegionStatus.degraded, RegionStatus.degraded, RegionStatus.operational, RegionStatus.degraded, RegionStatus.operational],
            [RegionStatus.operational, RegionStatus.maintenance, RegionStatus.operational, RegionStatus.operational, RegionStatus.operational, RegionStatus.operational],
            [RegionStatus.degraded, RegionStatus.offline, RegionStatus.offline, RegionStatus.degraded, RegionStatus.operational, RegionStatus.degraded]
        ]

        load_scenarios = [
            [0.65, 0.72, 0.58, 0.69, 0.43, 0.81],  # Normal loads
            [0.67, 0.74, 0.85, 0.71, 0.45, 0.83],  # One high load
            [0.89, 0.76, 0.95, 0.73, 0.67, 0.91],  # Multiple high loads
            [0.45, 0.32, 0.67, 0.71, 0.44, 0.79],  # Maintenance reduced load
            [0.95, 0.87, 0.00, 0.82, 0.67, 0.88]   # Critical scenario
        ]

        regions = []
        for i, region in enumerate(base_regions):
            region_data = region.copy()
            region_data["status"] = status_scenarios[scenario][i]
            region_data["current_load"] = load_scenarios[scenario][i]
            regions.append(NetworkRegion(**region_data))

        return {"regions": regions}

    def get_telemetry_response(self, region_id: str, metrics: Optional[str], granularity: Optional[str]) -> TelemetryData:
        scenario = self._rotate_scenario()

        metric_scenarios = [
            # Excellent performance
            {
                "throughput_mbps": random.uniform(850, 950),
                "latency_ms": random.uniform(1.2, 3.5),
                "packet_loss_percent": random.uniform(0.001, 0.01),
                "error_rate": random.uniform(0.0001, 0.001),
                "cpu_utilization": random.uniform(45, 65),
                "memory_utilization": random.uniform(50, 70),
                "active_sessions": random.randint(15000, 25000),
                "signal_strength_dbm": random.uniform(-70, -60)
            },
            # Good performance
            {
                "throughput_mbps": random.uniform(700, 850),
                "latency_ms": random.uniform(3.5, 8.0),
                "packet_loss_percent": random.uniform(0.01, 0.05),
                "error_rate": random.uniform(0.001, 0.01),
                "cpu_utilization": random.uniform(65, 80),
                "memory_utilization": random.uniform(70, 85),
                "active_sessions": random.randint(12000, 20000),
                "signal_strength_dbm": random.uniform(-80, -70)
            },
            # Degraded performance
            {
                "throughput_mbps": random.uniform(400, 700),
                "latency_ms": random.uniform(8.0, 25.0),
                "packet_loss_percent": random.uniform(0.05, 0.2),
                "error_rate": random.uniform(0.01, 0.05),
                "cpu_utilization": random.uniform(80, 95),
                "memory_utilization": random.uniform(85, 95),
                "active_sessions": random.randint(8000, 15000),
                "signal_strength_dbm": random.uniform(-90, -80)
            },
            # Maintenance mode
            {
                "throughput_mbps": random.uniform(600, 800),
                "latency_ms": random.uniform(2.0, 6.0),
                "packet_loss_percent": random.uniform(0.005, 0.02),
                "error_rate": random.uniform(0.0005, 0.005),
                "cpu_utilization": random.uniform(40, 60),
                "memory_utilization": random.uniform(45, 65),
                "active_sessions": random.randint(10000, 18000),
                "signal_strength_dbm": random.uniform(-75, -65)
            },
            # Critical issues
            {
                "throughput_mbps": random.uniform(100, 400),
                "latency_ms": random.uniform(25.0, 80.0),
                "packet_loss_percent": random.uniform(0.2, 2.0),
                "error_rate": random.uniform(0.05, 0.2),
                "cpu_utilization": random.uniform(95, 99),
                "memory_utilization": random.uniform(95, 99),
                "active_sessions": random.randint(3000, 8000),
                "signal_strength_dbm": random.uniform(-100, -90)
            }
        ]

        base_metrics = metric_scenarios[scenario]

        # Filter metrics if specified
        if metrics:
            requested_metrics = [m.strip() for m in metrics.split(',')]
            # Map request metric names to response metric names
            metric_mapping = {
                'throughput': 'throughput_mbps',
                'latency': 'latency_ms',
                'packet_loss': 'packet_loss_percent',
                'error_rate': 'error_rate',
                'cpu_utilization': 'cpu_utilization',
                'memory_utilization': 'memory_utilization',
                'active_sessions': 'active_sessions',
                'signal_strength': 'signal_strength_dbm'
            }
            filtered_metrics = {}
            for req_metric in requested_metrics:
                mapped_metric = metric_mapping.get(req_metric, req_metric)
                if mapped_metric in base_metrics:
                    filtered_metrics[mapped_metric] = base_metrics[mapped_metric]
        else:
            filtered_metrics = base_metrics

        return TelemetryData(
            region_id=region_id,
            timestamp=self._get_time_offset(minutes=-random.randint(0, 2)),
            metrics=TelemetryMetrics(**filtered_metrics)
        )

    def get_component_status_response(self, component_id: str) -> ComponentStatus:
        scenario = self._rotate_scenario()

        component_types = [ComponentType.base_station, ComponentType.core_node, ComponentType.edge_compute, ComponentType.router, ComponentType.switch]
        component_type = random.choice(component_types)

        status_scenarios = [
            # Operational
            {
                "status": ComponentStatusEnum.operational,
                "health_score": random.uniform(85, 100),
                "predicted_failure_probability": random.uniform(0.01, 0.05),
                "performance_metrics": {
                    "uptime_hours": random.uniform(2000, 8760),
                    "error_count_24h": random.randint(0, 5),
                    "temperature_celsius": random.uniform(35, 45),
                    "power_consumption_watts": random.uniform(150, 250)
                }
            },
            # Warning
            {
                "status": ComponentStatusEnum.warning,
                "health_score": random.uniform(65, 85),
                "predicted_failure_probability": random.uniform(0.05, 0.15),
                "performance_metrics": {
                    "uptime_hours": random.uniform(1000, 3000),
                    "error_count_24h": random.randint(5, 20),
                    "temperature_celsius": random.uniform(45, 60),
                    "power_consumption_watts": random.uniform(200, 300)
                }
            },
            # Critical
            {
                "status": ComponentStatusEnum.critical,
                "health_score": random.uniform(20, 45),
                "predicted_failure_probability": random.uniform(0.25, 0.45),
                "performance_metrics": {
                    "uptime_hours": random.uniform(100, 1000),
                    "error_count_24h": random.randint(50, 200),
                    "temperature_celsius": random.uniform(70, 85),
                    "power_consumption_watts": random.uniform(300, 400)
                }
            },
            # Maintenance
            {
                "status": ComponentStatusEnum.maintenance,
                "health_score": random.uniform(75, 95),
                "predicted_failure_probability": random.uniform(0.02, 0.08),
                "performance_metrics": {
                    "uptime_hours": random.uniform(500, 2000),
                    "error_count_24h": random.randint(0, 3),
                    "temperature_celsius": random.uniform(30, 40),
                    "power_consumption_watts": random.uniform(100, 200)
                }
            },
            # Offline
            {
                "status": ComponentStatusEnum.offline,
                "health_score": 0.0,
                "predicted_failure_probability": 1.0,
                "performance_metrics": {
                    "uptime_hours": 0,
                    "error_count_24h": 0,
                    "temperature_celsius": 25,
                    "power_consumption_watts": 0
                }
            }
        ]

        data = status_scenarios[scenario]

        return ComponentStatus(
            component_id=component_id,
            component_type=component_type,
            last_maintenance=self._get_time_offset(days=-random.randint(7, 90)),
            **data
        )

    def get_health_forecast_response(self, request: HealthForecastRequest) -> HealthForecast:
        scenario = self._rotate_scenario()

        forecast_scenarios = [
            # Low risk scenario
            {
                "overall_risk_score": random.uniform(15, 25),
                "confidence": random.uniform(0.9, 0.98),
                "incident_count": random.randint(0, 2),
                "peak_utilization": random.uniform(0.65, 0.75)
            },
            # Medium risk scenario
            {
                "overall_risk_score": random.uniform(35, 55),
                "confidence": random.uniform(0.8, 0.9),
                "incident_count": random.randint(2, 5),
                "peak_utilization": random.uniform(0.75, 0.85)
            },
            # High risk scenario
            {
                "overall_risk_score": random.uniform(65, 85),
                "confidence": random.uniform(0.7, 0.85),
                "incident_count": random.randint(5, 10),
                "peak_utilization": random.uniform(0.85, 0.95)
            },
            # Planned maintenance
            {
                "overall_risk_score": random.uniform(25, 40),
                "confidence": random.uniform(0.85, 0.95),
                "incident_count": random.randint(1, 3),
                "peak_utilization": random.uniform(0.6, 0.8)
            },
            # Critical scenario
            {
                "overall_risk_score": random.uniform(85, 95),
                "confidence": random.uniform(0.6, 0.8),
                "incident_count": random.randint(8, 15),
                "peak_utilization": random.uniform(0.9, 0.99)
            }
        ]

        scenario_data = forecast_scenarios[scenario]

        # Generate predicted incidents
        incidents = []
        for i in range(scenario_data["incident_count"]):
            incident = PredictedIncident(
                incident_id=f"incident-{uuid.uuid4().hex[:8]}",
                predicted_time=self._get_time_offset(hours=random.randint(1, 168)),  # 1 hour to 1 week
                probability=random.uniform(0.3, 0.9),
                severity=random.choice(list(Severity)),
                affected_components=[self._get_random_component() for _ in range(random.randint(1, 3))],
                root_cause_hypothesis=random.choice([
                    "High traffic load exceeding capacity",
                    "Hardware degradation detected",
                    "Network congestion in core nodes",
                    "Environmental factors affecting performance",
                    "Configuration drift causing instability"
                ]),
                estimated_impact=ImpactEstimate(
                    customers_affected=random.randint(1000, 50000),
                    revenue_at_risk=random.uniform(10000, 500000),
                    service_degradation_minutes=random.uniform(5, 240),
                    sla_violations=random.sample(["availability", "latency", "throughput"], random.randint(1, 3))
                ),
                recommended_actions=random.sample([
                    "Scale up resources in affected region",
                    "Redistribute traffic load",
                    "Schedule preventive maintenance",
                    "Update configuration parameters",
                    "Increase monitoring frequency"
                ], random.randint(2, 4))
            )
            incidents.append(incident)

        return HealthForecast(
            forecast_id=str(uuid.uuid4()),
            generated_at=self._get_time_offset(minutes=-1),
            time_horizon=request.time_horizon,
            overall_risk_score=scenario_data["overall_risk_score"],
            predicted_incidents=incidents,
            capacity_forecast=CapacityForecast(
                peak_utilization=scenario_data["peak_utilization"],
                bottleneck_regions=random.sample(self.regions, random.randint(0, 2))
            ),
            confidence=scenario_data["confidence"]
        )

    def get_anomalies_response(self, severity: Optional[str], confidence: Optional[float], region: Optional[str]) -> AnomalyList:
        scenario = self._rotate_scenario()

        anomaly_counts = [2, 5, 12, 3, 18]  # Number of anomalies per scenario
        high_priority_ratios = [0.0, 0.2, 0.6, 0.1, 0.8]  # Ratio of high priority anomalies

        count = anomaly_counts[scenario]
        high_priority_count = int(count * high_priority_ratios[scenario])

        anomalies = []
        for i in range(count):
            is_high_priority = i < high_priority_count

            anomaly = Anomaly(
                anomaly_id=f"anomaly-{uuid.uuid4().hex[:8]}",
                detected_at=self._get_time_offset(minutes=-random.randint(5, 120)),
                component_id=self._get_random_component(),
                anomaly_type=random.choice(list(AnomalyType)),
                severity=random.choice([Severity.high, Severity.critical]) if is_high_priority else random.choice([Severity.low, Severity.medium]),
                confidence=random.uniform(0.7, 0.95),
                description=random.choice([
                    "Unusual spike in response time detected",
                    "Memory utilization exceeding normal patterns",
                    "Irregular network traffic pattern observed",
                    "Component temperature rising above threshold",
                    "Connection timeout rate increased significantly"
                ]),
                affected_metrics=random.sample(["latency", "throughput", "cpu_utilization", "memory_utilization", "error_rate"], random.randint(1, 3)),
                correlation_score=random.uniform(0.4, 0.9)
            )

            # Apply filters
            if severity and anomaly.severity != severity:
                continue
            if confidence and anomaly.confidence < confidence:
                continue
            if region and not anomaly.component_id.startswith(region):
                continue

            anomalies.append(anomaly)

        return AnomalyList(
            anomalies=anomalies,
            total_count=len(anomalies),
            high_priority_count=sum(1 for a in anomalies if a.severity in [Severity.high, Severity.critical])
        )

    def get_failure_risk_response(self, request: FailureRiskRequest) -> FailureRiskAssessment:
        scenario = self._rotate_scenario()

        risk_levels = [
            [0.02, 0.08],  # Low risk
            [0.08, 0.20],  # Medium risk
            [0.25, 0.50],  # High risk
            [0.05, 0.15],  # Maintenance window
            [0.40, 0.80]   # Critical
        ]

        risk_range = risk_levels[scenario]

        components = []
        for component_id in request.components:
            risk_factors = random.sample([
                "High CPU utilization trending upward",
                "Memory leaks detected in system logs",
                "Hardware temperature exceeding normal range",
                "Increasing error rates in recent operations",
                "Component age approaching replacement cycle",
                "Environmental stress factors present",
                "Configuration drift from baseline"
            ], random.randint(2, 4))

            recommended_actions = random.sample([
                "Schedule preventive maintenance",
                "Update firmware to latest version",
                "Increase monitoring frequency",
                "Prepare backup component for hot swap",
                "Review and optimize configuration",
                "Implement redundancy measures",
                "Plan capacity upgrade"
            ], random.randint(2, 3))

            components.append(ComponentRisk(
                component_id=component_id,
                failure_probability=random.uniform(risk_range[0], risk_range[1]),
                risk_factors=risk_factors,
                recommended_actions=recommended_actions
            ))

        return FailureRiskAssessment(
            assessment_id=str(uuid.uuid4()),
            components=components
        )

    # Healing Actions Templates
    def get_healing_actions_catalog(self) -> HealingActionsCatalog:
        actions = [
            HealingActionCatalog(
                action_type="load_balance",
                description="Redistribute network traffic across available resources",
                required_parameters=["target_regions", "traffic_percentage"],
                risk_level=Severity.low,
                estimated_duration="5-15 minutes"
            ),
            HealingActionCatalog(
                action_type="scale_resources",
                description="Automatically scale compute resources up or down",
                required_parameters=["component_types", "scale_factor"],
                risk_level=Severity.medium,
                estimated_duration="10-30 minutes"
            ),
            HealingActionCatalog(
                action_type="restart_service",
                description="Restart specific network services or components",
                required_parameters=["service_names", "restart_sequence"],
                risk_level=Severity.medium,
                estimated_duration="2-10 minutes"
            ),
            HealingActionCatalog(
                action_type="reroute_traffic",
                description="Redirect traffic through alternative network paths",
                required_parameters=["source_regions", "destination_regions"],
                risk_level=Severity.high,
                estimated_duration="1-5 minutes"
            ),
            HealingActionCatalog(
                action_type="update_config",
                description="Apply configuration updates to resolve issues",
                required_parameters=["config_templates", "target_components"],
                risk_level=Severity.medium,
                estimated_duration="15-45 minutes"
            ),
            HealingActionCatalog(
                action_type="emergency_maintenance",
                description="Trigger emergency maintenance procedures",
                required_parameters=["maintenance_type", "affected_components"],
                risk_level=Severity.high,
                estimated_duration="1-6 hours"
            )
        ]

        return HealingActionsCatalog(actions=actions)

    def get_healing_action_response(self, request: HealingActionRequest) -> HealingActionResponse:
        scenario = self._rotate_scenario()

        action_id = str(uuid.uuid4())
        workflow_id = str(uuid.uuid4())

        # Generate workflow steps based on action type
        steps_templates = {
            "load_balance": [
                "Analyze current traffic distribution",
                "Calculate optimal load distribution",
                "Update load balancer configuration",
                "Verify traffic redistribution",
                "Monitor system stability"
            ],
            "scale_resources": [
                "Assess current resource utilization",
                "Calculate required scaling factor",
                "Provision additional resources",
                "Update service configuration",
                "Validate scaled deployment"
            ],
            "restart_service": [
                "Prepare service for restart",
                "Gracefully stop service",
                "Restart service components",
                "Verify service health",
                "Resume normal operations"
            ],
            "reroute_traffic": [
                "Identify alternative paths",
                "Update routing tables",
                "Redirect traffic flows",
                "Monitor path performance",
                "Confirm traffic stability"
            ],
            "update_config": [
                "Backup current configuration",
                "Validate new configuration",
                "Apply configuration updates",
                "Restart affected services",
                "Verify configuration success"
            ],
            "emergency_maintenance": [
                "Activate emergency protocols",
                "Isolate affected components",
                "Perform emergency repairs",
                "Test component functionality",
                "Restore to operational state"
            ]
        }

        step_descriptions = steps_templates.get(request.action_type, ["Execute action", "Verify results"])

        steps = []
        for i, description in enumerate(step_descriptions):
            status = StepStatus.completed if i == 0 else StepStatus.pending
            step = WorkflowStep(
                step_id=f"step-{i+1}",
                description=description,
                status=status,
                started_at=self._get_time_offset(minutes=-1) if status == StepStatus.completed else None,
                completed_at=self._get_time_offset() if status == StepStatus.completed else None,
                output={"step_result": "success"} if status == StepStatus.completed else None
            )
            steps.append(step)

        # Set first pending step to running
        for step in steps:
            if step.status == StepStatus.pending:
                step.status = StepStatus.running
                step.started_at = self._get_time_offset()
                break

        status_options = [JobStatus.running, JobStatus.completed, JobStatus.requires_approval]
        action_status = random.choice(status_options) if scenario != 4 else JobStatus.requires_approval

        return HealingActionResponse(
            action_id=action_id,
            workflow_id=workflow_id,
            status=action_status,
            estimated_completion=self._get_time_offset(minutes=random.randint(10, 60)),
            steps=steps
        )

    def get_workflows_list(self) -> WorkflowsList:
        scenario = self._rotate_scenario()

        workflow_counts = [1, 2, 4, 2, 6]  # Number of active workflows per scenario
        count = workflow_counts[scenario]

        workflows = []
        for i in range(count):
            workflows.append(WorkflowSummary(
                workflow_id=str(uuid.uuid4()),
                status=random.choice(["running", "completed", "pending"]),
                started_at=self._get_time_offset(minutes=-random.randint(10, 240)),
                estimated_completion=self._get_time_offset(minutes=random.randint(5, 60))
            ))

        return WorkflowsList(workflows=workflows)

    def get_workflow_details(self, workflow_id: str) -> WorkflowDetails:
        # Generate sample workflow steps
        steps = []
        for i in range(random.randint(3, 6)):
            status = random.choice(list(StepStatus))
            step = WorkflowStep(
                step_id=f"step-{i+1}",
                description=f"Execute workflow step {i+1}",
                status=status,
                started_at=self._get_time_offset(minutes=-random.randint(5, 30)) if status != StepStatus.pending else None,
                completed_at=self._get_time_offset(minutes=-random.randint(1, 10)) if status == StepStatus.completed else None,
                output={"result": "success"} if status == StepStatus.completed else None
            )
            steps.append(step)

        return WorkflowDetails(
            workflow_id=workflow_id,
            status=random.choice(["running", "completed", "failed"]),
            steps=steps,
            metadata={
                "action_type": random.choice(list(ActionType)),
                "target_components": [self._get_random_component()],
                "created_by": "system",
                "priority": random.choice(["low", "medium", "high"])
            }
        )

    def get_rollback_response(self, action_id: str) -> RollbackResponse:
        return RollbackResponse(
            rollback_id=str(uuid.uuid4()),
            original_action_id=action_id,
            status="running",
            estimated_completion=self._get_time_offset(minutes=random.randint(5, 30))
        )

    # Analytics Templates
    def get_historical_data_response(self, start_time: str, end_time: str, metrics: Optional[str], aggregation: Optional[str]) -> HistoricalData:
        scenario = self._rotate_scenario()

        # Parse time range
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

        # Generate data points based on aggregation
        aggregation_minutes = {
            "raw": 1, "1min": 1, "5min": 5, "15min": 15, "1hour": 60, "1day": 1440
        }

        interval = aggregation_minutes.get(aggregation, 60)
        current_time = start_dt
        data_points = []

        while current_time <= end_dt and len(data_points) < 1000:  # Limit to 1000 points
            metrics_data = {
                "throughput": random.uniform(500, 1000),
                "latency": random.uniform(1, 20),
                "error_rate": random.uniform(0.001, 0.05),
                "cpu_utilization": random.uniform(30, 90),
                "memory_utilization": random.uniform(40, 85)
            }

            data_points.append(HistoricalDataPoint(
                timestamp=current_time,
                metrics=metrics_data
            ))

            current_time += timedelta(minutes=interval)

        return HistoricalData(
            query_id=str(uuid.uuid4()),
            time_range=TimeRange(start_time=start_dt, end_time=end_dt),
            data_points=data_points
        )

    def get_incident_history_response(self, severity: Optional[str], category: Optional[str], resolved: Optional[bool]) -> IncidentHistory:
        scenario = self._rotate_scenario()

        incident_counts = [3, 7, 15, 5, 25]  # Number of incidents per scenario
        count = incident_counts[scenario]

        incidents = []
        for i in range(count):
            occurred_at = self._get_time_offset(days=-random.randint(1, 90))
            is_resolved = resolved if resolved is not None else random.choice([True, True, True, False])  # 75% resolved

            incident = IncidentDetails(
                incident_id=f"incident-{uuid.uuid4().hex[:8]}",
                occurred_at=occurred_at,
                resolved_at=occurred_at + timedelta(hours=random.randint(1, 8)) if is_resolved else None,
                severity=severity or random.choice(["low", "medium", "high", "critical"]),
                category=category or random.choice(["connectivity", "performance", "hardware", "configuration"]),
                root_cause=random.choice([
                    "Hardware failure in core network",
                    "Software bug causing memory leak",
                    "Network congestion during peak hours",
                    "Configuration error after maintenance",
                    "Environmental factors (power outage)",
                    "DDoS attack on network infrastructure"
                ]),
                resolution_actions=[
                    random.choice([
                        "Replaced faulty hardware component",
                        "Applied software patch",
                        "Increased network capacity",
                        "Corrected configuration settings",
                        "Implemented traffic filtering",
                        "Restored from backup"
                    ])
                ] if is_resolved else []
            )
            incidents.append(incident)

        return IncidentHistory(incidents=incidents)

    # Business Intelligence Templates
    def get_impact_assessment_response(self, request: ImpactAssessmentRequest) -> BusinessImpactAssessment:
        scenario = self._rotate_scenario()

        impact_multipliers = [0.5, 1.0, 2.5, 0.8, 4.0]  # Impact severity per scenario
        multiplier = impact_multipliers[scenario]

        base_customers = sum([100000 for region in request.scenario.affected_regions])  # 100k per region
        affected_customers = int(base_customers * request.scenario.service_degradation * multiplier)

        return BusinessImpactAssessment(
            assessment_id=str(uuid.uuid4()),
            scenario=f"Service degradation in {len(request.scenario.affected_regions)} regions",
            total_revenue_impact=affected_customers * 0.05 * request.scenario.duration_hours,  # $0.05 per customer per hour
            customers_affected=affected_customers,
            service_credits_exposure=affected_customers * 2.50,  # $2.50 per affected customer
            reputation_risk_score=min(100, request.scenario.service_degradation * 100 * multiplier),
            recovery_time_estimate=f"{random.randint(1, 6)} hours",
            mitigation_costs=random.uniform(10000, 100000) * multiplier
        )

    def get_sla_status_response(self, customer_tier: Optional[str], service_type: Optional[str]) -> SLAStatus:
        scenario = self._rotate_scenario()

        # SLA targets based on customer tier
        targets = {
            "enterprise": 0.9999,  # 99.99%
            "premium": 0.999,     # 99.9%
            "standard": 0.995     # 99.5%
        }

        compliance_scenarios = [0.95, 0.88, 0.75, 0.92, 0.65]  # Overall compliance per scenario
        overall_compliance = compliance_scenarios[scenario]

        service_levels = []
        services = ["5G Core Network", "Edge Computing", "IoT Platform", "Enterprise VPN"]

        for service in services:
            if service_type and service.lower().replace(" ", "_") not in service_type:
                continue

            tier = customer_tier or random.choice(["enterprise", "premium", "standard"])
            target = targets[tier]

            # Actual availability varies based on scenario
            actual = target * random.uniform(0.98, 1.002)  # Slight variation around target

            if scenario >= 2:  # Degraded scenarios
                actual *= random.uniform(0.95, 0.99)

            status = ComplianceStatus.compliant
            if actual < target * 0.98:
                status = ComplianceStatus.violated
            elif actual < target * 0.995:
                status = ComplianceStatus.at_risk

            service_levels.append(ServiceLevel(
                service_name=service,
                target_availability=target,
                actual_availability=min(1.0, actual),
                compliance_status=status
            ))

        return SLAStatus(
            overall_compliance=overall_compliance,
            service_levels=service_levels
        )

    # Configuration Templates
    def get_threshold_configuration(self) -> ThresholdConfiguration:
        return ThresholdConfiguration(
            performance_thresholds=PerformanceThresholds(
                latency_warning_ms=50.0,
                latency_critical_ms=100.0,
                throughput_warning_percent=80.0,
                packet_loss_warning_percent=0.1
            ),
            prediction_thresholds=PredictionThresholds(
                anomaly_confidence=0.75,
                failure_probability=0.20
            )
        )

    # Async Job Templates
    def get_async_job_response(self, job_id: str) -> AsyncJobStatus:
        return AsyncJobStatus(
            job_id=job_id,
            status=JobStatus.queued,
            progress=0.0,
            created_at=self._get_time_offset(),
            started_at=None,
            completed_at=None,
            result=None,
            error=None
        )

    def get_async_job_status(self, job_id: str) -> AsyncJobStatus:
        scenario = self._rotate_scenario()

        statuses = [JobStatus.completed, JobStatus.running, JobStatus.failed, JobStatus.running, JobStatus.queued]
        status = statuses[scenario]

        progress = 1.0 if status == JobStatus.completed else random.uniform(0.1, 0.9) if status == JobStatus.running else 0.0

        return AsyncJobStatus(
            job_id=job_id,
            status=status,
            progress=progress,
            created_at=self._get_time_offset(minutes=-random.randint(10, 120)),
            started_at=self._get_time_offset(minutes=-random.randint(5, 60)) if status != JobStatus.queued else None,
            completed_at=self._get_time_offset(minutes=-random.randint(1, 10)) if status == JobStatus.completed else None,
            result={"forecast_id": str(uuid.uuid4())} if status == JobStatus.completed else None,
            error="Insufficient data for long-term prediction" if status == JobStatus.failed else None
        )