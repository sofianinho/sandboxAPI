# Network Intelligence Sandbox API

A comprehensive mock server implementing the Network Intelligence Sandbox API for the **Predictive Network Intelligence & Self-Healing Platform Challenge**.

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t network-intelligence-api .
docker run -p 8000:8000 network-intelligence-api
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## 🏗️ Architecture

### Key Features

- **5 Response Scenarios**: Each endpoint rotates through 5 different realistic scenarios
- **Dynamic Network State**: Background simulation evolves network conditions over time
- **Realistic Telco Data**: Authentic telecommunications metrics and patterns
- **Challenge-Aligned**: Supports all use cases from the challenge document
- **Production-Like**: Proper error handling, authentication, and async patterns

### Response Scenarios

1. **Excellent Health** - All systems operating optimally
2. **Good Performance** - Minor issues, generally stable
3. **Degraded State** - Performance issues requiring attention
4. **Maintenance Mode** - Planned maintenance activities
5. **Critical Issues** - Major problems requiring immediate action

## 🔧 API Endpoints

### Network Status & Telemetry
- `GET /network/status` - Overall network health
- `GET /network/regions` - Regional status information
- `GET /network/regions/{regionId}/telemetry` - Real-time metrics
- `GET /network/components/{componentId}/status` - Component details

### Predictive Analytics
- `POST /predictions/health-forecast` - Generate health forecasts
- `GET /predictions/anomalies` - Current anomaly detections
- `POST /predictions/failure-risk` - Component failure risk assessment

### Healing Actions & Orchestration
- `GET /healing/actions` - Available healing actions catalog
- `POST /healing/actions` - Execute healing action
- `GET /healing/workflows` - Active healing workflows
- `GET /healing/workflows/{workflowId}` - Workflow details
- `POST /healing/rollback/{actionId}` - Rollback healing action

### Historical Data & Analytics
- `GET /analytics/historical` - Historical performance data
- `GET /analytics/incidents` - Historical incident data

### Business Intelligence
- `POST /business/impact-assessment` - Business impact analysis
- `GET /business/sla-status` - SLA compliance status

### Configuration & Management
- `GET /config/thresholds` - Current threshold configuration
- `PUT /config/thresholds` - Update thresholds
- `GET /system/jobs/{jobId}` - Async job status

## 🔐 Authentication

The API uses Bearer token authentication. Include an `Authorization` header:

```bash
Authorization: Bearer your-jwt-token-here
```

**Note**: The mock server accepts any valid-looking JWT token for testing purposes.

## 📊 Challenge Use Cases

### Financial District Conference
```bash
# Monitor capacity and predict spikes
curl -H "Authorization: Bearer test-token" \
  "http://localhost:8000/network/regions/region-northeast-02/telemetry?metrics=throughput,latency,cpu_utilization"

# Generate traffic forecast
curl -X POST -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "time_horizon": "24hours",
    "scope": {"regions": ["region-northeast-02"]},
    "confidence_threshold": 0.8
  }' \
  "http://localhost:8000/predictions/health-forecast"
```

### Northwest Region Anomaly Detection
```bash
# Check for anomalies
curl -H "Authorization: Bearer test-token" \
  "http://localhost:8000/predictions/anomalies?region=region-northwest-01&severity=high"

# Assess component failure risk
curl -X POST -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "components": ["base-station-01-001", "core-node-01-01"],
    "time_horizon": "1week"
  }' \
  "http://localhost:8000/predictions/failure-risk"
```

### Executive Health Assessment
```bash
# Get overall network status
curl -H "Authorization: Bearer test-token" \
  "http://localhost:8000/network/status"

# Generate business impact assessment
curl -X POST -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": {
      "affected_regions": ["region-northwest-01", "region-northeast-02"],
      "service_degradation": 0.3,
      "duration_hours": 4
    },
    "customer_segments": ["enterprise", "premium"]
  }' \
  "http://localhost:8000/business/impact-assessment"
```

### Automated Healing
```bash
# Get available healing actions
curl -H "Authorization: Bearer test-token" \
  "http://localhost:8000/healing/actions"

# Execute load balancing action
curl -X POST -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "load_balance",
    "target_components": ["region-northwest-01"],
    "parameters": {"traffic_percentage": 30},
    "approval_level": "automatic"
  }' \
  "http://localhost:8000/healing/actions"
```

## 🎯 Challenge-Specific Features

### Multi-Horizon Predictions
- **Short-term** (1-6 hours): High confidence, detailed predictions
- **Medium-term** (24 hours - 3 days): Moderate confidence, trend analysis
- **Long-term** (1 week - 1 month): Lower confidence, strategic planning

### Realistic Network Components
- **RAN**: 5G base stations with varying health and performance
- **Core Network**: Control plane functions with high reliability
- **Edge Computing**: Distributed processing with dynamic scaling
- **Transport**: Fiber links and routing infrastructure

### Business Impact Modeling
- **Revenue Impact**: Per-customer hourly loss calculations
- **SLA Violations**: Service level breach tracking
- **Customer Segments**: Differentiated impact by tier
- **Reputation Risk**: Quantified brand impact scoring

## 🔧 Configuration

### Environment Variables
- `LOG_LEVEL`: Logging level (default: info)
- `PYTHONUNBUFFERED`: Python output buffering (default: 1)

### Response Timing
- Simple GET requests: 50-200ms
- Complex predictions: 200-500ms
- Async job initiation: 100-300ms
- Historical queries: 300-800ms

## 🚦 Health Monitoring

The API includes comprehensive health checks:

```bash
# Basic health check
curl http://localhost:8000/health

# Network state summary
curl -H "Authorization: Bearer test-token" \
  "http://localhost:8000/network/status"
```

## 📈 Performance

- **Concurrent Requests**: Supports up to 100 concurrent connections
- **Memory Usage**: ~256MB typical, 512MB recommended
- **CPU Usage**: 0.5 cores minimum
- **Response Times**: Sub-second for all endpoints

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change port mapping in docker-compose.yml
2. **Authentication errors**: Ensure Bearer token is provided
3. **Slow responses**: Check if background simulation is running

### Debug Mode

For development, run with debug logging:

```bash
LOG_LEVEL=debug uvicorn main:app --reload
```

## 🤝 Contributing

This mock server is designed to support the LabLabee challenge. For issues or enhancements:

1. Review the API specification in `NetworkIntelligenceSandboxAPI.yaml`
2. Check the challenge requirements in `challenge.pdf`
3. Test changes against all use cases

## 📄 License

Apache 2.0 License - See the API specification for details.

---

**Built for the LabLabee Predictive Network Intelligence & Self-Healing Platform Challenge** 🚀