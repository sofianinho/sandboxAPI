from fastapi import FastAPI, HTTPException, Depends, Query, Path, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import random
import uuid
from enum import Enum
import uvicorn

from models import *
from network_state import NetworkStateManager
from response_templates import ResponseTemplateManager

app = FastAPI(
    title="Network Intelligence Sandbox API",
    description="""API for the Predictive Network Intelligence & Self-Healing Platform Challenge.

This sandbox simulates a comprehensive telco network environment with predictive analytics capabilities.
The API provides access to real-time telemetry data, prediction services, automated healing actions,
and historical network performance data.

**Key Features:**
- Real-time network telemetry streaming
- Multi-horizon failure prediction (seconds to weeks)
- Autonomous healing action orchestration
- Historical data analysis and pattern recognition
- Business impact assessment and SLA monitoring

**Network Components:**
- RAN (Radio Access Network): 5G base stations and small cells
- Core Network: User plane functions, control plane, authentication
- Edge Computing: Distributed processing nodes
- Transport: Fiber links, routers, switches
- Customer Devices: Mobile handsets, IoT devices, enterprise equipment""",
    version="1.0.0",
    contact={
        "name": "LabLabee Engineering Team",
        "email": "engineering@lablabee.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/"
    },
    openapi_version="3.0.3",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        },
        {
            "url": "https://sandbox.5gnetwork.test",
            "description": "Remote sandbox environment"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
network_state = NetworkStateManager()
templates = ResponseTemplateManager()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if not credentials.credentials or len(credentials.credentials) < 10:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials

# Override the security scheme name to match YAML spec
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.0.3"
    )

    # Add servers configuration
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        },
        {
            "url": "https://sandbox.5gnetwork.test",
            "description": "Remote sandbox environment"
        }
    ]
    # Replace HTTPBearer with BearerAuth to match YAML spec
    if "securitySchemes" in openapi_schema["components"]:
        bearer_scheme = openapi_schema["components"]["securitySchemes"].pop("HTTPBearer", None)
        if bearer_scheme:
            bearer_scheme["bearerFormat"] = "JWT"
            openapi_schema["components"]["securitySchemes"]["BearerAuth"] = bearer_scheme

    # Update all security references
    for path_info in openapi_schema["paths"].values():
        for operation in path_info.values():
            if "security" in operation:
                for security_req in operation["security"]:
                    if "HTTPBearer" in security_req:
                        security_req["BearerAuth"] = security_req.pop("HTTPBearer")

    # Add global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Create API router with /api/v1 prefix
api_router = APIRouter(prefix="/api/v1")

# ========================================
# NETWORK STATUS & TELEMETRY
# ========================================

@api_router.get("/network/status", response_model=NetworkStatus, tags=["Network Status"], summary="Get overall network health status", description="Returns high-level network health indicators and system status")
async def get_network_status(token: str = Depends(verify_token)):
    return templates.get_network_status_response()

@api_router.get("/network/regions", response_model=RegionsResponse, tags=["Network Status"], summary="List all network regions", description="Get list of geographical regions with their current status")
async def get_regions(token: str = Depends(verify_token)):
    return templates.get_regions_response()

@api_router.get("/network/regions/{regionId}/telemetry", response_model=TelemetryData, tags=["Telemetry"], summary="Get real-time telemetry for a region", description="Retrieve current performance metrics for a specific network region")
async def get_region_telemetry(
    regionId: str = Path(..., example="region-northwest-01"),
    metrics: Optional[str] = Query(None, example="throughput,latency,packet_loss,cpu_utilization", description="Comma-separated list of specific metrics to retrieve"),
    granularity: Optional[str] = Query("realtime", enum=["realtime", "1min", "5min", "15min", "1hour"], description="Time granularity for data points"),
    token: str = Depends(verify_token)
):
    return templates.get_telemetry_response(regionId, metrics, granularity)

@api_router.get("/network/components/{componentId}/status", response_model=ComponentStatus, tags=["Network Status"], summary="Get detailed status of a network component", description="Retrieve comprehensive status information for a specific network component")
async def get_component_status(
    componentId: str = Path(..., example="base-station-downtown-001"),
    token: str = Depends(verify_token)
):
    return templates.get_component_status_response(componentId)

# ========================================
# PREDICTIVE ANALYTICS
# ========================================

@api_router.post("/predictions/health-forecast", tags=["Predictions"], summary="Generate network health forecast", description="Create predictive health assessment for specified time horizon and network scope", responses={200: {"description": "Health forecast generated successfully", "model": HealthForecast}, 202: {"description": "Forecast generation in progress", "model": AsyncJobStatus}})
async def create_health_forecast(
    request: HealthForecastRequest,
    token: str = Depends(verify_token)
):
    if request.time_horizon in ["1week", "1month"]:
        # Return async job for long-running forecasts
        job_id = str(uuid.uuid4())
        return templates.get_async_job_response(job_id), 202
    else:
        return templates.get_health_forecast_response(request)

@api_router.get("/predictions/anomalies", response_model=AnomalyList, tags=["Predictions"], summary="Get current anomaly detections", description="Retrieve list of detected anomalies with severity and confidence scores")
async def get_anomalies(
    severity: Optional[str] = Query(None, enum=["low", "medium", "high", "critical"], description="Filter by minimum severity level"),
    confidence: Optional[float] = Query(None, ge=0, le=1, description="Filter by minimum confidence threshold (0-1)"),
    region: Optional[str] = Query(None, description="Filter by specific region"),
    token: str = Depends(verify_token)
):
    return templates.get_anomalies_response(severity, confidence, region)

@api_router.post("/predictions/failure-risk", response_model=FailureRiskAssessment, tags=["Predictions"], summary="Assess failure risk for network components", description="Calculate failure probability and impact assessment for specified components")
async def assess_failure_risk(
    request: FailureRiskRequest,
    token: str = Depends(verify_token)
):
    return templates.get_failure_risk_response(request)

# ========================================
# HEALING ACTIONS & ORCHESTRATION
# ========================================

@api_router.get("/healing/actions", response_model=HealingActionsCatalog, tags=["Healing"], summary="List available healing actions", description="Get catalog of all available automated healing actions")
async def get_healing_actions(token: str = Depends(verify_token)):
    return templates.get_healing_actions_catalog()

@api_router.post("/healing/actions", tags=["Healing"], summary="Execute healing action", description="Trigger automated healing action for detected issues", responses={202: {"description": "Healing action initiated", "model": HealingActionResponse}})
async def execute_healing_action(
    request: HealingActionRequest,
    token: str = Depends(verify_token)
):
    return templates.get_healing_action_response(request), 202

@api_router.get("/healing/workflows", response_model=WorkflowsList, tags=["Healing"], summary="List active healing workflows", description="Get status of currently running healing workflows")
async def get_active_workflows(token: str = Depends(verify_token)):
    return templates.get_workflows_list()

@api_router.get("/healing/workflows/{workflowId}", response_model=WorkflowDetails, tags=["Healing"], summary="Get healing workflow details", description="Retrieve detailed information about a specific healing workflow")
async def get_workflow_details(
    workflowId: str = Path(...),
    token: str = Depends(verify_token)
):
    return templates.get_workflow_details(workflowId)

@api_router.post("/healing/rollback/{actionId}", tags=["Healing"], summary="Rollback healing action", description="Reverse a previously executed healing action", responses={202: {"description": "Rollback initiated", "model": RollbackResponse}})
async def rollback_action(
    actionId: str = Path(...),
    token: str = Depends(verify_token)
):
    return templates.get_rollback_response(actionId), 202

# ========================================
# HISTORICAL DATA & ANALYTICS
# ========================================

@api_router.get("/analytics/historical", response_model=HistoricalData, tags=["Analytics"], summary="Query historical network data", description="Retrieve historical performance data for analysis and training")
async def get_historical_data(
    start_time: str = Query(..., example="2024-01-01T00:00:00Z"),
    end_time: str = Query(..., example="2024-01-31T23:59:59Z"),
    metrics: Optional[str] = Query(None, example="throughput,latency,error_rate", description="Specific metrics to retrieve"),
    aggregation: Optional[str] = Query("1hour", enum=["raw", "1min", "5min", "15min", "1hour", "1day"], description="Data aggregation level"),
    token: str = Depends(verify_token)
):
    return templates.get_historical_data_response(start_time, end_time, metrics, aggregation)

@api_router.get("/analytics/incidents", response_model=IncidentHistory, tags=["Analytics"], summary="Get historical incident data", description="Retrieve past network incidents for pattern analysis")
async def get_incident_history(
    severity: Optional[str] = Query(None, enum=["low", "medium", "high", "critical"]),
    category: Optional[str] = Query(None, example="connectivity,performance,hardware"),
    resolved: Optional[bool] = Query(None),
    token: str = Depends(verify_token)
):
    return templates.get_incident_history_response(severity, category, resolved)

# ========================================
# BUSINESS INTELLIGENCE
# ========================================

@api_router.post("/business/impact-assessment", response_model=BusinessImpactAssessment, tags=["Business Intelligence"], summary="Generate business impact assessment", description="Calculate revenue and customer impact for network issues")
async def create_impact_assessment(
    request: ImpactAssessmentRequest,
    token: str = Depends(verify_token)
):
    return templates.get_impact_assessment_response(request)

@api_router.get("/business/sla-status", response_model=SLAStatus, tags=["Business Intelligence"], summary="Get SLA compliance status", description="Retrieve current SLA performance metrics and compliance status")
async def get_sla_status(
    customer_tier: Optional[str] = Query(None, enum=["enterprise", "premium", "standard"]),
    service_type: Optional[str] = Query(None, example="5g,edge_compute,iot"),
    token: str = Depends(verify_token)
):
    return templates.get_sla_status_response(customer_tier, service_type)

# ========================================
# CONFIGURATION & MANAGEMENT
# ========================================

@api_router.get("/config/thresholds", response_model=ThresholdConfiguration, tags=["Configuration"], summary="Get alerting and prediction thresholds", description="Retrieve current threshold configuration for alerts and predictions")
async def get_thresholds(token: str = Depends(verify_token)):
    return templates.get_threshold_configuration()

@api_router.put("/config/thresholds", response_model=UpdateResponse, tags=["Configuration"], summary="Update alerting and prediction thresholds", description="Modify threshold settings for alerts and predictions")
async def update_thresholds(
    config: ThresholdConfiguration,
    token: str = Depends(verify_token)
):
    return {"message": "Thresholds updated successfully", "timestamp": datetime.utcnow().isoformat()}

@api_router.get("/system/jobs/{jobId}", response_model=AsyncJobStatus, tags=["System"], summary="Get async job status", description="Check status of long-running background jobs")
async def get_job_status(
    jobId: str = Path(...),
    token: str = Depends(verify_token)
):
    return templates.get_async_job_status(jobId)

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)