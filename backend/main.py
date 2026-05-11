from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import pydantic

from database import get_db, Business, Analysis, Strategy, Proposal
from agents.business_agent import BusinessDiscoveryAgent
from agents.analysis_agent import DigitalAnalysisAgent
from agents.strategy_agent import StrategyAgent
from agents.proposal_agent import ProposalAgent

app = FastAPI(title="Autonomous Multi-Agent AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas for request/response
class BusinessCreate(pydantic.BaseModel):
    name: str
    category: str
    location: str

class WorkflowResponse(pydantic.BaseModel):
    business_id: int
    message: str

# Initialize Agents
discovery_agent = BusinessDiscoveryAgent()
analysis_agent = DigitalAnalysisAgent()
strategy_agent = StrategyAgent()
proposal_agent = ProposalAgent()

@app.post("/api/analyze-business", response_model=WorkflowResponse)
def analyze_business(req: BusinessCreate, db: Session = Depends(get_db)):
    # 1. Discovery
    discovery_results = discovery_agent.execute(req.name, req.category, req.location)
    
    # Save Business
    db_business = Business(**discovery_results)
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    
    # 2. Analysis
    analysis_results = analysis_agent.execute(discovery_results)
    db_analysis = Analysis(business_id=db_business.id, **analysis_results)
    db.add(db_analysis)
    
    # 3. Strategy
    strategy_results = strategy_agent.execute(discovery_results, analysis_results)
    db_strategy = Strategy(business_id=db_business.id, **strategy_results)
    db.add(db_strategy)
    
    # 4. Proposal
    proposal_results = proposal_agent.execute(discovery_results, analysis_results, strategy_results)
    db_proposal = Proposal(business_id=db_business.id, **proposal_results)
    db.add(db_proposal)
    
    db.commit()
    
    return {"business_id": db_business.id, "message": "Multi-agent workflow completed successfully"}

@app.get("/api/dashboard-summary")
def get_dashboard(db: Session = Depends(get_db)):
    businesses = db.query(Business).all()
    results = []
    for b in businesses:
        results.append({
            "id": b.id,
            "name": b.name,
            "category": b.category,
            "location": b.location,
            "maturity_score": b.analysis.maturity_score if b.analysis else 0,
            "website": b.website
        })
    return results

@app.get("/api/business/{business_id}")
def get_business_details(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return {
        "business": {
            "name": business.name,
            "category": business.category,
            "location": business.location,
            "website": business.website,
            "social_presence": business.social_presence,
            "contact_info": business.contact_info
        },
        "analysis": {
            "score": business.analysis.maturity_score,
            "strengths": business.analysis.strengths,
            "weaknesses": business.analysis.weaknesses,
            "missing_assets": business.analysis.missing_assets
        },
        "strategy": {
            "recommended": business.strategy.recommended_strategy,
            "actions": business.strategy.priority_actions,
            "impact": business.strategy.expected_impact
        },
        "proposal": {
            "text": business.proposal.proposal_text,
            "timeline": business.proposal.timeline,
            "cost": business.proposal.estimated_cost,
            "roi": business.proposal.expected_roi
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
