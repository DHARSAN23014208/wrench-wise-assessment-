import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

# -------------------------------------------------------------------
# 1. FastAPI Application & CORS Setup
# -------------------------------------------------------------------
app = FastAPI(
    title="Apex Enterprise API Engine",
    description="High-performance FastAPI backend serving dynamic JSON endpoints for modern UI.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (ideal for local/hosted UI)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVER_START_TIME = time.time()

# -------------------------------------------------------------------
# 2. Pydantic Models for JSON Validation
# -------------------------------------------------------------------
class ActionRequest(BaseModel):
    user_id: str = Field(..., example="USR-12345", description="Target customer identifier")
    action_type: str = Field(..., example="FREEZE_CARD", description="Operation type to perform")
    reason: Optional[str] = Field(default="User initiated action via console", description="Optional operational reason")
    amount: Optional[float] = Field(default=0.0, description="Amount involved in financial actions")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional payload metadata")

class ActionResponse(BaseModel):
    success: bool
    message: str
    updated_status: str
    timestamp: float
    execution_latency_ms: float
    affected_balance: Optional[float] = None
    transaction_id: Optional[str] = None

class LatencyMetric(BaseModel):
    endpoint: str
    latency_ms: float

class AnalyticsTelemetry(BaseModel):
    total_requests: int
    avg_latency_ms: float
    system_health: str
    active_connections: int
    uptime_seconds: float
    resource_distribution: Dict[str, float]
    route_latencies: Dict[str, float]

class TransactionItem(BaseModel):
    id: str
    date: str
    merchant: str
    amount: float
    flagged: bool
    category: Optional[str] = "General"

class UserAccountBalances(BaseModel):
    checking: float
    savings: float

class UserProfile(BaseModel):
    name: str
    tier: str
    card_status: str
    account_balances: UserAccountBalances
    recent_transactions: List[TransactionItem]

class SystemHealthResponse(BaseModel):
    status: str
    engine: str
    python_runtime: str
    uptime_seconds: float
    timestamp: float
    version: str

# -------------------------------------------------------------------
# 3. Mock Database Engine (JSON Data Store)
# -------------------------------------------------------------------
MOCK_DATABASE = {
    "users": {
        "USR-12345": {
            "name": "Jane Smith",
            "tier": "Platinum Member",
            "card_status": "ACTIVE",
            "account_balances": {
                "checking": 4520.50,
                "savings": 15000.00
            },
            "recent_transactions": [
                {"id": "TXN-101", "date": "2026-10-08", "merchant": "Whole Foods Market", "amount": 45.50, "flagged": False, "category": "Groceries"},
                {"id": "TXN-102", "date": "2026-10-09", "merchant": "Amazon Marketplace", "amount": 120.00, "flagged": False, "category": "Shopping"},
                {"id": "TXN-103", "date": "2026-10-10", "merchant": "Moscow Tech Store", "amount": 850.00, "flagged": True, "category": "Electronics"},
                {"id": "TXN-104", "date": "2026-10-10", "merchant": "Starbucks Reserve", "amount": 14.25, "flagged": False, "category": "Dining"},
                {"id": "TXN-105", "date": "2026-10-10", "merchant": "Cloud Compute Nodes", "amount": 240.00, "flagged": False, "category": "Services"}
            ]
        },
        "USR-67890": {
            "name": "Alex Rivera",
            "tier": "Diamond Executive",
            "card_status": "ACTIVE",
            "account_balances": {
                "checking": 12850.75,
                "savings": 48200.00
            },
            "recent_transactions": [
                {"id": "TXN-201", "date": "2026-10-07", "merchant": "Delta Airlines VIP", "amount": 640.00, "flagged": False, "category": "Travel"},
                {"id": "TXN-202", "date": "2026-10-09", "merchant": "Apple Fifth Ave", "amount": 1299.00, "flagged": False, "category": "Electronics"},
                {"id": "TXN-203", "date": "2026-10-10", "merchant": "Zurich Private Vault", "amount": 5400.00, "flagged": True, "category": "Security"}
            ]
        },
        "USR-99001": {
            "name": "Sarah Chen",
            "tier": "Gold Elite",
            "card_status": "LOCKED",
            "account_balances": {
                "checking": 1950.20,
                "savings": 8400.50
            },
            "recent_transactions": [
                {"id": "TXN-301", "date": "2026-10-09", "merchant": "Tokyo Metro Card", "amount": 35.00, "flagged": False, "category": "Transit"},
                {"id": "TXN-302", "date": "2026-10-10", "merchant": "CyberSec VPN Node", "amount": 99.99, "flagged": True, "category": "Software"}
            ]
        }
    },
    "metrics": {
        "requests_processed": 1420,
        "avg_latency": 38.4,
        "active_nodes": 8,
        "route_latencies": {
            "/api/v1/health": 8.4,
            "/api/v1/data": 28.6,
            "/api/v1/action": 42.1,
            "/api/v1/telemetry": 18.2
        },
        "resource_distribution": {
            "Core Compute Engine": 35.0,
            "Neural Risk Classifier": 28.0,
            "In-Memory Cache Layer": 22.0,
            "Network & RPC Gateways": 15.0
        }
    }
}

# -------------------------------------------------------------------
# 4. RESTful API Endpoints
# -------------------------------------------------------------------
@app.get("/api/v1/health", response_model=SystemHealthResponse, tags=["System"])
async def get_health():
    """Health check endpoint to verify backend connectivity and runtime specs."""
    MOCK_DATABASE["metrics"]["requests_processed"] += 1
    return SystemHealthResponse(
        status="ONLINE",
        engine="FastAPI v0.110+",
        python_runtime="3.10+",
        uptime_seconds=round(time.time() - SERVER_START_TIME, 1),
        timestamp=time.time(),
        version="2.0.0"
    )

@app.get("/api/v1/users", tags=["Data Engine"])
async def get_users_list():
    """Returns a directory of all available user profiles."""
    users_summary = [
        {
            "user_id": uid,
            "name": data["name"],
            "tier": data["tier"],
            "card_status": data["card_status"],
            "total_balance": round(data["account_balances"]["checking"] + data["account_balances"]["savings"], 2)
        }
        for uid, data in MOCK_DATABASE["users"].items()
    ]
    return {
        "status": "SUCCESS",
        "count": len(users_summary),
        "users": users_summary
    }

@app.get("/api/v1/data", tags=["Data Engine"])
async def get_enterprise_data(user_id: str = Query(default="USR-12345", description="User ID to retrieve")):
    """Returns structured enterprise JSON payload for UI rendering."""
    start_time = time.time()
    
    if user_id not in MOCK_DATABASE["users"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User record '{user_id}' not found. Available users: {list(MOCK_DATABASE['users'].keys())}"
        )
    
    MOCK_DATABASE["metrics"]["requests_processed"] += 1
    latency = round((time.time() - start_time) * 1000, 2)
    MOCK_DATABASE["metrics"]["route_latencies"]["/api/v1/data"] = round((MOCK_DATABASE["metrics"]["route_latencies"]["/api/v1/data"] * 0.9) + (latency * 0.1), 1)

    return {
        "status": "SUCCESS",
        "user_id": user_id,
        "data": MOCK_DATABASE["users"][user_id],
        "available_users": list(MOCK_DATABASE["users"].keys()),
        "server_time": time.time(),
        "query_latency_ms": latency
    }

@app.post("/api/v1/action", response_model=ActionResponse, tags=["Actions"])
async def execute_action(payload: ActionRequest):
    """Processes dynamic frontend user actions (e.g. Card Locks, Transfers, Fraud Simulation)."""
    start_time = time.time()
    
    user = MOCK_DATABASE["users"].get(payload.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User '{payload.user_id}' not found."
        )

    action = payload.action_type.upper()
    affected_balance: Optional[float] = None
    txn_id: Optional[str] = None

    if action == "FREEZE_CARD":
        user["card_status"] = "LOCKED"
        message = f"Payment rail for {user['name']} locked successfully. Reason: {payload.reason or 'User requested freeze'}"
    
    elif action == "UNFREEZE_CARD":
        user["card_status"] = "ACTIVE"
        message = f"Card access restored to ACTIVE status for {user['name']}."
    
    elif action == "TRANSFER_CHECKING_TO_SAVINGS":
        transfer_amount = payload.amount if (payload.amount and payload.amount > 0) else 250.0
        if user["account_balances"]["checking"] < transfer_amount:
            raise HTTPException(status_code=400, detail="Insufficient checking funds for transfer.")
        user["account_balances"]["checking"] -= transfer_amount
        user["account_balances"]["savings"] += transfer_amount
        affected_balance = user["account_balances"]["checking"]
        message = f"Successfully transferred ${transfer_amount:.2f} from Checking to Savings."
    
    elif action == "TRANSFER_SAVINGS_TO_CHECKING":
        transfer_amount = payload.amount if (payload.amount and payload.amount > 0) else 250.0
        if user["account_balances"]["savings"] < transfer_amount:
            raise HTTPException(status_code=400, detail="Insufficient savings funds for transfer.")
        user["account_balances"]["savings"] -= transfer_amount
        user["account_balances"]["checking"] += transfer_amount
        affected_balance = user["account_balances"]["checking"]
        message = f"Successfully transferred ${transfer_amount:.2f} from Savings to Checking."
    
    elif action == "SIMULATE_TRANSACTION":
        txn_amount = payload.amount if (payload.amount and payload.amount > 0) else 185.50
        is_high_risk = txn_amount > 500.0 or "suspicious" in (payload.reason or "").lower()
        txn_id = f"TXN-{int(time.time() * 1000) % 100000}"
        
        new_txn = {
            "id": txn_id,
            "date": time.strftime("%Y-%m-%d"),
            "merchant": payload.reason or "Simulated Terminal Gateway",
            "amount": round(txn_amount, 2),
            "flagged": is_high_risk,
            "category": "Simulation"
        }
        user["recent_transactions"].insert(0, new_txn)
        if len(user["recent_transactions"]) > 10:
            user["recent_transactions"].pop()
        
        user["account_balances"]["checking"] = max(0.0, user["account_balances"]["checking"] - txn_amount)
        affected_balance = user["account_balances"]["checking"]
        status_note = "FLAGGED as high-risk" if is_high_risk else "APPROVED"
        message = f"Simulated transaction {txn_id} (${txn_amount:.2f}) processed: {status_note}."

    elif action == "CLEAR_FLAGGED_TRANSACTIONS":
        cleared_count = 0
        for txn in user["recent_transactions"]:
            if txn["flagged"]:
                txn["flagged"] = False
                cleared_count += 1
        message = f"Cleared risk flags from {cleared_count} transaction(s)."

    elif action == "RESET_USER_STATE":
        # Reset to initial profile state
        user["card_status"] = "ACTIVE"
        user["account_balances"]["checking"] = 4520.50
        user["account_balances"]["savings"] = 15000.00
        message = f"State and balances for {user['name']} restored to demo defaults."

    else:
        message = f"Action '{action}' processed successfully via Apex engine."

    MOCK_DATABASE["metrics"]["requests_processed"] += 1
    latency = round((time.time() - start_time) * 1000 + 15.0, 2)
    MOCK_DATABASE["metrics"]["route_latencies"]["/api/v1/action"] = round(latency, 1)

    return ActionResponse(
        success=True,
        message=message,
        updated_status=user["card_status"],
        timestamp=time.time(),
        execution_latency_ms=latency,
        affected_balance=affected_balance,
        transaction_id=txn_id
    )

@app.get("/api/v1/telemetry", response_model=AnalyticsTelemetry, tags=["Analytics"])
async def get_telemetry():
    """Provides system operational metrics for real-time charts."""
    MOCK_DATABASE["metrics"]["requests_processed"] += 1
    # add minor dynamic variations for live chart aesthetics
    now = time.time()
    uptime = round(now - SERVER_START_TIME, 1)
    
    # recalculate average latency smoothly
    latencies = list(MOCK_DATABASE["metrics"]["route_latencies"].values())
    avg_lat = round(sum(latencies) / max(len(latencies), 1), 2)
    MOCK_DATABASE["metrics"]["avg_latency"] = avg_lat

    return AnalyticsTelemetry(
        total_requests=MOCK_DATABASE["metrics"]["requests_processed"],
        avg_latency_ms=avg_lat,
        system_health="OPTIMAL",
        active_connections=24 + int((time.time() % 10) - 5),
        uptime_seconds=uptime,
        resource_distribution=MOCK_DATABASE["metrics"]["resource_distribution"],
        route_latencies=MOCK_DATABASE["metrics"]["route_latencies"]
    )

# Serve Frontend Directly from root
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>index.html not found</h1><p>Please place index.html in the root directory.</p>",
            status_code=404
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
