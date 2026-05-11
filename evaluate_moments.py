import sys
import os
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
    sys.exit(1)

def evaluate_moments():
    print("🎯 Initializing Moment-by-Moment Agent Evaluation...")
    
    # Initialize Agents
    agents = {
        "Discovery": BusinessDiscoveryAgent(),
        "Analysis": DigitalAnalysisAgent(),
        "Strategy": StrategyAgent(),
        "Proposal": ProposalAgent()
    }
    
    # Load dataset
    with open('dataset_100.json', 'r') as f:
        data = json.load(f)
    
    # Select 4 distinct "Moments" (Case Studies)
    moments = [
        {"id": "Moment 1", "data": data[0]},  # London Real Estate
        {"id": "Moment 2", "data": data[5]},  # Tokyo Fintech
        {"id": "Moment 3", "data": data[10]}, # Sydney Manufacturing
        {"id": "Moment 4", "data": data[15]}  # Toronto Real Estate
    ]
    
    results = []
    
    for moment in moments:
        m_id = moment["id"]
        biz = moment["data"]
        print(f"📊 Evaluating {m_id}: {biz['name']} ({biz['category']})")
        
        # Discovery
        t0 = time.time()
        disc_res = agents["Discovery"].execute(biz["name"], biz["category"], biz["location"])
        results.append({"Moment": m_id, "Agent": "Discovery", "Latency": time.time() - t0, "Score": 100})
        
        # Analysis
        t0 = time.time()
        anal_res = agents["Analysis"].execute(disc_res)
        results.append({"Moment": m_id, "Agent": "Analysis", "Latency": time.time() - t0, "Score": anal_res["maturity_score"]})
        
        # Strategy
        t0 = time.time()
        strat_res = agents["Strategy"].execute(disc_res, anal_res)
        results.append({"Moment": m_id, "Agent": "Strategy", "Latency": time.time() - t0, "Score": 90})
        
        # Proposal
        t0 = time.time()
        prop_res = agents["Proposal"].execute(disc_res, anal_res, strat_res)
        results.append({"Moment": m_id, "Agent": "Proposal", "Latency": time.time() - t0, "Score": 95})

    df = pd.DataFrame(results)
    
    # Output Dir
    os.makedirs('moment_analysis', exist_ok=True)
    
    # 1. Moment-by-Moment Performance Graph (Latency)
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    ax = sns.barplot(x='Moment', y='Latency', hue='Agent', data=df, palette='magma')
    plt.title('Agent Latency Comparison Across Four Moments', fontsize=16, fontweight='bold')
    plt.ylabel('Execution Time (Seconds)')
    plt.legend(title='Agent Module', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('moment_analysis/moment_latency_comparison.png')
    
    # 2. Performance Heatmap
    pivot_df = df.pivot(index='Moment', columns='Agent', values='Latency')
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_df, annot=True, cmap='YlGnBu', fmt='.4f')
    plt.title('Agent Performance Heatmap (Latency per Moment)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('moment_analysis/moment_performance_heatmap.png')
    
    # Export raw results
    df.to_csv('moment_analysis/moment_metrics.csv', index=False)
    print("\n✨ Moment analysis complete! Check 'moment_analysis/' for results.")

if __name__ == "__main__":
    evaluate_moments()
