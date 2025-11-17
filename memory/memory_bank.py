import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional

class MemoryBank:
    """Persistent memory storage for context and history"""
    
    def __init__(self, db_path: str = "./data/memory.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Context snapshots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        
        # Plans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                recommendations TEXT NOT NULL,
                total_co2_savings REAL,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER,
                recommendation_id INTEGER,
                action TEXT,
                user_notes TEXT,
                timestamp TEXT,
                FOREIGN KEY (plan_id) REFERENCES plans(id)
            )
        ''')
        
        # Events log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_name TEXT,
                action TEXT,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_context(self, context: Dict[str, Any]):
        """Store current operational context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO context_snapshots (timestamp, data) VALUES (?, ?)',
            (datetime.now().isoformat(), json.dumps(context))
        )
        
        conn.commit()
        conn.close()
    
    def store_plan(self, plan: Dict[str, Any]):
        """Store generated plan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO plans (timestamp, recommendations, total_co2_savings, status)
            VALUES (?, ?, ?, ?)
        ''', (
            plan.get("timestamp"),
            json.dumps(plan.get("recommendations", [])),
            plan.get("total_co2_savings_kg", 0),
            "pending"
        ))
        
        conn.commit()
        conn.close()
    
    def log_event(self, agent_name: str, action: str, details: Dict):
        """Log agent events for observability"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (timestamp, agent_name, action, details)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            agent_name,
            action,
            json.dumps(details)
        ))
        
        conn.commit()
        conn.close()
    
    def get_baseline_metrics(self) -> Dict[str, float]:
        """Retrieve historical baseline metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get average from last 30 days
        cursor.execute('''
            SELECT data FROM context_snapshots
            WHERE timestamp > datetime('now', '-30 days')
            ORDER BY timestamp DESC
        ''')
        
        snapshots = cursor.fetchall()
        conn.close()
        
        if not snapshots:
            return {"energy_kwh": 1000, "emissions_kg": 500}
        
        # Calculate averages
        total_energy = 0
        total_emissions = 0
        count = 0
        
        for (data_json,) in snapshots:
            data = json.loads(data_json)
            summary = data.get("operational_summary", {})
            total_energy += summary.get("total_energy_kwh", 0)
            total_emissions += summary.get("total_emissions_kg_co2", 0)
            count += 1
        
        return {
            "energy_kwh": total_energy / count if count > 0 else 1000,
            "emissions_kg": total_emissions / count if count > 0 else 500
        }
    
    def store_feedback(self, plan_id: int, rec_id: int, action: str, notes: str = ""):
        """Store user feedback on recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (plan_id, recommendation_id, action, user_notes, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (plan_id, rec_id, action, notes, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_recent_plans(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent plans"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, recommendations, total_co2_savings, status
            FROM plans
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        plans = []
        for row in cursor.fetchall():
            plans.append({
                "id": row[0],
                "timestamp": row[1],
                "recommendations": json.loads(row[2]),
                "total_co2_savings_kg": row[3],
                "status": row[4]
            })
        
        conn.close()
        return plans
