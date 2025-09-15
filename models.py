from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

class HealthStatus(str, Enum):
    excellent = "excellent"
    good = "good"
    degraded = "degraded"
    critical = "critical"

class RegionStatus(str, Enum):
    operational = "operational"
    degraded = "degraded"
    maintenance = "maintenance"
    offline = "offline"

class ComponentType(str, Enum):
    base_station = "base_station"
    core_node = "core_node"
    edge_compute = "edge_compute"
    router = "router"
    switch = "switch"

class ComponentStatusEnum(str, Enum):
    operational = "operational"
    warning = "warning"
    critical = "critical"
    offline = "offline"
    maintenance = "maintenance"

class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class AnomalyType(str, Enum):
    performance = "performance"
    capacity = "capacity"
    connectivity = "connectivity"
    hardware = "hardware"
    pattern = "pattern"

class ActionType(str, Enum):
    load_balance = "load_balance"
    scale_resources = "scale_resources"
    restart_service = "restart_service"
    reroute_traffic = "reroute_traffic"
    update_config = "update_config"
    emergency_maintenance = "emergency_maintenance"

class ApprovalLevel(str, Enum):
    automatic = "automatic"
    supervised = "supervised"
    manual_approval = "manual_approval"

class RollbackPolicy(str, Enum):
    automatic = "automatic"
    manual = "manual"
    time_based = "time_based"

class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    requires_approval = "requires_approval"

class StepStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    skipped = "skipped"

class TimeHorizon(str, Enum):
    one_hour = "1hour"
    six_hours = "6hours"
    twenty_four_hours = "24hours"
    three_days = "3days"
    one_week = "1week"
    one_month = "1month"

class CustomerTier(str, Enum):
    enterprise = "enterprise"
    premium = "premium"
    standard = "standard"

class ComplianceStatus(str, Enum):
    compliant = "compliant"
    at_risk = "at_risk"
    violated = "violated"

# Core Models
class NetworkStatus(BaseModel):
    overall_health: HealthStatus
    uptime_percentage: float = Field(..., ge=0, le=100)
    active_regions: int
    total_base_stations: int
    connected_devices: int
    current_throughput_gbps: float
    prediction_confidence: float = Field(..., ge=0, le=1)
    last_updated: datetime

class NetworkRegion(BaseModel):
    region_id: str
    name: str
    status: RegionStatus
    base_stations: int
    connected_devices: int
    current_load: float = Field(..., ge=0, le=1)

class RegionsResponse(BaseModel):
    regions: List[NetworkRegion]

class TelemetryMetrics(BaseModel):
    throughput_mbps: Optional[float] = None
    latency_ms: Optional[float] = None
    packet_loss_percent: Optional[float] = None
    error_rate: Optional[float] = None
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    active_sessions: Optional[int] = None
    signal_strength_dbm: Optional[float] = None

class TelemetryData(BaseModel):
    region_id: str
    timestamp: datetime
    metrics: TelemetryMetrics

class ComponentStatus(BaseModel):
    component_id: str
    component_type: ComponentType
    status: ComponentStatusEnum
    health_score: float = Field(..., ge=0, le=100)
    last_maintenance: datetime
    predicted_failure_probability: float = Field(..., ge=0, le=1)
    performance_metrics: Dict[str, Any]

# Prediction Models
class HealthForecastScope(BaseModel):
    regions: Optional[List[str]] = None
    component_types: Optional[List[str]] = None

class HealthForecastRequest(BaseModel):
    time_horizon: TimeHorizon
    scope: HealthForecastScope
    confidence_threshold: float = Field(0.8, ge=0, le=1)

class ImpactEstimate(BaseModel):
    customers_affected: int
    revenue_at_risk: float
    service_degradation_minutes: float
    sla_violations: List[str]

class PredictedIncident(BaseModel):
    incident_id: str
    predicted_time: datetime
    probability: float = Field(..., ge=0, le=1)
    severity: Severity
    affected_components: List[str]
    root_cause_hypothesis: str
    estimated_impact: ImpactEstimate
    recommended_actions: List[str]

class CapacityForecast(BaseModel):
    peak_utilization: float
    bottleneck_regions: List[str]

class HealthForecast(BaseModel):
    forecast_id: str
    generated_at: datetime
    time_horizon: str
    overall_risk_score: float = Field(..., ge=0, le=100)
    predicted_incidents: List['PredictedIncident']
    capacity_forecast: CapacityForecast
    confidence: float = Field(..., ge=0, le=1)

class Anomaly(BaseModel):
    anomaly_id: str
    detected_at: datetime
    component_id: str
    anomaly_type: AnomalyType
    severity: Severity
    confidence: float = Field(..., ge=0, le=1)
    description: str
    affected_metrics: List[str]
    correlation_score: float = Field(..., ge=0, le=1)

class AnomalyList(BaseModel):
    anomalies: List[Anomaly]
    total_count: int
    high_priority_count: int

class FailureRiskRequest(BaseModel):
    components: List[str]
    time_horizon: str = "24hours"

class ComponentRisk(BaseModel):
    component_id: str
    failure_probability: float = Field(..., ge=0, le=1)
    risk_factors: List[str]
    recommended_actions: List[str]

class FailureRiskAssessment(BaseModel):
    assessment_id: str
    components: List[ComponentRisk]

# Healing Models
class HealingActionRequest(BaseModel):
    action_type: ActionType
    target_components: List[str]
    parameters: Optional[Dict[str, Any]] = None
    approval_level: ApprovalLevel = ApprovalLevel.supervised
    rollback_policy: RollbackPolicy = RollbackPolicy.time_based

class WorkflowStep(BaseModel):
    step_id: str
    description: str
    status: StepStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output: Optional[Dict[str, Any]] = None

class HealingActionResponse(BaseModel):
    action_id: str
    workflow_id: str
    status: JobStatus
    estimated_completion: datetime
    steps: List[WorkflowStep]

class HealingActionCatalog(BaseModel):
    action_type: str
    description: str
    required_parameters: List[str]
    risk_level: Severity
    estimated_duration: str

class HealingActionsCatalog(BaseModel):
    actions: List[HealingActionCatalog]

class WorkflowSummary(BaseModel):
    workflow_id: str
    status: str
    started_at: datetime
    estimated_completion: datetime

class WorkflowsList(BaseModel):
    workflows: List[WorkflowSummary]

class WorkflowDetails(BaseModel):
    workflow_id: str
    status: str
    steps: List[WorkflowStep]
    metadata: Dict[str, Any]

class RollbackResponse(BaseModel):
    rollback_id: str
    original_action_id: str
    status: str
    estimated_completion: datetime

# Analytics Models
class HistoricalDataPoint(BaseModel):
    timestamp: datetime
    metrics: Dict[str, Any]

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime

class HistoricalData(BaseModel):
    query_id: str
    time_range: TimeRange
    data_points: List[HistoricalDataPoint]

class IncidentDetails(BaseModel):
    incident_id: str
    occurred_at: datetime
    resolved_at: Optional[datetime] = None
    severity: str
    category: str
    root_cause: str
    resolution_actions: List[str]

class IncidentHistory(BaseModel):
    incidents: List[IncidentDetails]

# Business Intelligence Models
class ImpactScenario(BaseModel):
    affected_regions: List[str]
    service_degradation: float = Field(..., ge=0, le=1)
    duration_hours: float

class ImpactAssessmentRequest(BaseModel):
    scenario: ImpactScenario
    customer_segments: Optional[List[str]] = None

class BusinessImpactAssessment(BaseModel):
    assessment_id: str
    scenario: str
    total_revenue_impact: float
    customers_affected: int
    service_credits_exposure: float
    reputation_risk_score: float = Field(..., ge=0, le=100)
    recovery_time_estimate: str
    mitigation_costs: float

class ServiceLevel(BaseModel):
    service_name: str
    target_availability: float = Field(..., ge=0, le=1)
    actual_availability: float = Field(..., ge=0, le=1)
    compliance_status: ComplianceStatus

class SLAStatus(BaseModel):
    overall_compliance: float = Field(..., ge=0, le=1)
    service_levels: List[ServiceLevel]

# Configuration Models
class PerformanceThresholds(BaseModel):
    latency_warning_ms: float
    latency_critical_ms: float
    throughput_warning_percent: float
    packet_loss_warning_percent: float

class PredictionThresholds(BaseModel):
    anomaly_confidence: float = Field(..., ge=0, le=1)
    failure_probability: float = Field(..., ge=0, le=1)

class ThresholdConfiguration(BaseModel):
    performance_thresholds: PerformanceThresholds
    prediction_thresholds: PredictionThresholds

# System Models
class AsyncJobStatus(BaseModel):
    job_id: str
    status: JobStatus
    progress: float = Field(..., ge=0, le=1)
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class UpdateResponse(BaseModel):
    message: str
    timestamp: str