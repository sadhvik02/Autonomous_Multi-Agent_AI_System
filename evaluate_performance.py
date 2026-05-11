import sys
import os
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the project root is in the system path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Use absolute imports from the project root
try:
    from backend.agents.business_agent import BusinessDiscoveryAgent
    from backend.agents.analysis_agent import DigitalAnalysisAgent
    from backend.agents.strategy_agent import StrategyAgent
    from backend.agents.proposal_agent import ProposalAgent
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nDEBUG INFO:")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Root Directory: {ROOT_DIR}")
    print(f"System Path: {sys.path}")
    sys.exit(1)

def run_evaluation():
    print("🚀 Starting Agent Performance Evaluation...")
    
    # Initialize Agents
    agents = {
        "Discovery": BusinessDiscoveryAgent(),
        "Analysis": DigitalAnalysisAgent(),
        "Strategy": StrategyAgent(),
        "Proposal": ProposalAgent()
    }
    
    # Load sample data
    with open('dataset_100.json', 'r') as f:
        data = json.load(f)
    
    samples = data[:20] # Run on first 20 for evaluation
    
    results = []
    
    for i, item in enumerate(samples):
        print(f"Processing sample {i+1}/20: {item['name']}")
        row = {"name": item["name"], "category": item["category"]}
        
        # Measure Discovery Agent
        start = time.time()
        discovery_res = agents["Discovery"].execute(item["name"], item["category"], item["location"])
        row["discovery_latency"] = time.time() - start
        
        # Measure Analysis Agent
        start = time.time()
        analysis_res = agents["Analysis"].execute(discovery_res)
        row["analysis_latency"] = time.time() - start
        row["maturity_score"] = analysis_res["maturity_score"]
        
        # Measure Strategy Agent
        start = time.time()
        strategy_res = agents["Strategy"].execute(discovery_res, analysis_res)
        row["strategy_latency"] = time.time() - start
        
        # Measure Proposal Agent
        start = time.time()
        proposal_res = agents["Proposal"].execute(discovery_res, analysis_res, strategy_res)
        row["proposal_latency"] = time.time() - start
        
        results.append(row)

    df = pd.DataFrame(results)
    
    # Create output directory
    os.makedirs('performance_reports', exist_ok=True)
    
    # 1. Latency Analysis Graph
    plt.figure(figsize=(10, 6))
    latency_cols = [c for c in df.columns if 'latency' in c]
    df[latency_cols].mean().plot(kind='bar', color=['#6366f1', '#a855f7', '#f43f5e', '#10b981'])
    plt.title('Average Agent Latency (Seconds)', fontsize=14, fontweight='bold')
    plt.ylabel('Seconds')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('performance_reports/agent_latency.png')
    
    # 2. Maturity Score Distribution by Industry
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='category', y='maturity_score', data=df, palette='viridis')
    plt.title('Digital Maturity Score Distribution by Industry', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('performance_reports/maturity_distribution.png')
    
    # 3. Overall System Performance (Success vs Score)
    plt.figure(figsize=(8, 8))
    plt.pie([df['maturity_score'].mean(), 100 - df['maturity_score'].mean()], 
            labels=['Avg Maturity', 'Gap'], autopct='%1.1f%%', colors=['#6366f1', '#e2e8f0'])
    plt.title('Systemic Digital Opportunity Gap', fontsize=14, fontweight='bold')
    plt.savefig('performance_reports/opportunity_gap.png')
    
    # Save CSV
    df.to_csv('performance_reports/evaluation_results.csv', index=False)
    print("\n✨ Evaluation Complete! Results saved in 'performance_reports/'")

if __name__ == "__main__":
    run_evaluation()
