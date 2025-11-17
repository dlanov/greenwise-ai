import asyncio
import gradio as gr
import numpy as np

from config import GreenWiseConfig
from llm.gemini_client import GeminiClient
from memory.memory_bank import MemoryBank

# Main application class
class GreenWiseApp:
    """Main Hugging Face Spaces Gradio application"""
    
    def __init__(self):
        self.config = GreenWiseConfig()
        self.setup_components()
    
    def setup_components(self):
        """Initialize all system components"""
        # Memory
        self.memory_bank = MemoryBank(self.config.MEMORY_PATH)
        
        # LLM Client
        self.llm_client = GeminiClient(
            api_key=self.config.GEMINI_API_KEY,
            model_name=self.config.MODEL_NAME
        )
        
        # Tools
        from tools.emissions_calculator import EmissionsCalculator
        from tools.iot_simulator import IoTSimulator
        
        self.tools = [
            EmissionsCalculator(),
            IoTSimulator()
        ]
        
        # Agents
        from agents.data_scout_agent import DataScoutAgent
        from agents.ecoplanner_agent import EcoPlannerAgent
        
        self.data_scout = DataScoutAgent(
            name="DataScout",
            llm_client=self.llm_client,
            memory_bank=self.memory_bank,
            tools=self.tools
        )
        
        self.ecoplanner = EcoPlannerAgent(
            name="EcoPlanner",
            llm_client=self.llm_client,
            memory_bank=self.memory_bank,
            tools=self.tools
        )
    
    async def run_orchestration_cycle(self):
        """Execute one complete orchestration cycle"""
        # Step 1: Data Scout gathers context
        context_package = await self.data_scout.execute({})
        
        # Step 2: EcoPlanner generates recommendations
        plan = await self.ecoplanner.execute(context_package)
        
        return plan
    
    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(title="GreenWise AI - Sustainable Operations Orchestrator", 
                      theme=gr.themes.Soft()) as interface:
            
            gr.Markdown("""
            # 🌱 GreenWise AI - Sustainable Operations Orchestrator
            
            AI-powered sustainability recommendations for enterprise operations using multi-agent orchestration.
            """)
            
            with gr.Tabs():
                # Tab 1: Dashboard
                with gr.Tab("📊 Dashboard"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### Current Metrics")
                            energy_display = gr.Number(label="Total Energy (kWh)", interactive=False)
                            emissions_display = gr.Number(label="CO2 Emissions (kg)", interactive=False)
                            anomalies_display = gr.Number(label="Anomalies Detected", interactive=False)
                            
                            refresh_btn = gr.Button("🔄 Refresh Data", variant="primary")
                        
                        with gr.Column(scale=2):
                            gr.Markdown("### Energy Consumption Trends")
                            energy_chart = gr.Plot(label="24-Hour Energy Profile")
                    
                    with gr.Row():
                        gr.Markdown("### Facility Status")
                        status_table = gr.Dataframe(
                            headers=["Facility", "Energy (kWh)", "Status", "Efficiency"],
                            interactive=False
                        )
                
                # Tab 2: Recommendations
                with gr.Tab("💡 Recommendations"):
                    gr.Markdown("### AI-Generated Sustainability Recommendations")
                    
                    generate_btn = gr.Button("🤖 Generate Recommendations", variant="primary", size="lg")
                    
                    with gr.Row():
                        rec_status = gr.Markdown("Status: Ready")
                    
                    recommendations_display = gr.JSON(label="Recommendations")
                    
                    with gr.Accordion("Recommendation Details", open=False):
                        rec_details = gr.Markdown()
                    
                    gr.Markdown("### Impact Summary")
                    with gr.Row():
                        total_co2_savings = gr.Number(label="Total CO2 Savings (kg)", interactive=False)
                        total_energy_savings = gr.Number(label="Total Energy Savings (kWh)", interactive=False)
                
                # Tab 3: Feedback
                with gr.Tab("📝 Feedback"):
                    gr.Markdown("### Provide Feedback on Recommendations")
                    
                    plan_selector = gr.Dropdown(label="Select Plan", choices=[])
                    rec_selector = gr.Dropdown(label="Select Recommendation", choices=[])
                    
                    with gr.Row():
                        feedback_action = gr.Radio(
                            choices=["Accept", "Modify", "Reject"],
                            label="Action"
                        )
                    
                    feedback_notes = gr.Textbox(
                        label="Notes (optional)",
                        placeholder="Explain why you accepted/modified/rejected this recommendation...",
                        lines=3
                    )
                    
                    submit_feedback_btn = gr.Button("Submit Feedback", variant="primary")
                    feedback_result = gr.Markdown()
                
                # Tab 4: History
                with gr.Tab("📜 History"):
                    gr.Markdown("### Past Recommendations & Outcomes")
                    
                    history_display = gr.Dataframe(
                        headers=["Timestamp", "Recommendations", "CO2 Savings", "Status"],
                        interactive=False
                    )
                    
                    load_history_btn = gr.Button("Load History")
                
                # Tab 5: Settings
                with gr.Tab("⚙️ Settings"):
                    gr.Markdown("### Configuration")
                    
                    with gr.Group():
                        emission_factor = gr.Slider(
                            minimum=0.1, maximum=1.0, value=0.475,
                            label="Grid Carbon Intensity (kg CO2/kWh)",
                            info="Adjust based on your region's grid mix"
                        )
                        
                        max_recs = gr.Slider(
                            minimum=1, maximum=20, value=10, step=1,
                            label="Maximum Recommendations per Cycle"
                        )
                        
                        enable_auto_actions = gr.Checkbox(
                            label="Enable Automatic Actions (Low-Risk Only)",
                            value=False
                        )
                    
                    save_settings_btn = gr.Button("Save Settings")
                    settings_status = gr.Markdown()
            
            # Event Handlers
            async def refresh_dashboard():
                """Refresh dashboard metrics"""
                # Get latest context from memory
                context = await self.data_scout.execute({})
                summary = context.get("operational_summary", {})
                
                # Generate chart
                import plotly.graph_objects as go
                hours = list(range(24))
                energy = [np.random.normal(500, 50) for _ in hours]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hours, y=energy, mode='lines+markers', name='Energy'))
                fig.update_layout(
                    title="24-Hour Energy Consumption",
                    xaxis_title="Hour",
                    yaxis_title="Energy (kWh)"
                )
                
                # Facility status
                facilities = [
                    ["Facility A", 520, "Normal", "85%"],
                    ["Facility B", 780, "Alert", "72%"],
                    ["Facility C", 310, "Optimal", "92%"]
                ]
                
                return (
                    summary.get("total_energy_kwh", 0),
                    summary.get("total_emissions_kg_co2", 0),
                    summary.get("anomaly_count", 0),
                    fig,
                    facilities
                )
            
            async def generate_recommendations():
                """Generate new recommendations"""
                status_msg = "🔄 Running orchestration cycle...\n"
                status_msg += "- Data Scout gathering context...\n"
                
                # Run orchestration
                plan = await self.run_orchestration_cycle()
                
                status_msg += "- EcoPlanner generating recommendations...\n"
                status_msg += "✅ Complete!\n"
                
                # Format recommendations for display
                recs = plan.get("recommendations", [])
                
                details = "## Detailed Recommendations\n\n"
                for i, rec in enumerate(recs, 1):
                    details += f"### Recommendation {i}\n"
                    details += f"**Description:** {rec.get('description', 'N/A')}\n\n"
                    details += f"**Impact:** {rec.get('co2_savings_kg', 0):.1f} kg CO2 saved\n\n"
                    details += f"**Complexity:** {rec.get('complexity', 'medium')}\n\n"
                    details += "---\n\n"
                
                return (
                    status_msg,
                    plan,
                    details,
                    plan.get("total_co2_savings_kg", 0),
                    plan.get("total_energy_savings_kwh", 0)
                )
            
            def submit_feedback(plan_id, rec_id, action, notes):
                """Submit user feedback"""
                if not plan_id or not rec_id:
                    return "❌ Please select a plan and recommendation"
                
                self.memory_bank.store_feedback(
                    plan_id=int(plan_id),
                    rec_id=int(rec_id),
                    action=action,
                    notes=notes
                )
                
                return f"✅ Feedback submitted: {action}"
            
            def load_history():
                """Load historical plans"""
                plans = self.memory_bank.get_recent_plans(limit=20)
                
                history_data = []
                for plan in plans:
                    history_data.append([
                        plan["timestamp"],
                        len(plan["recommendations"]),
                        f"{plan['total_co2_savings_kg']:.1f}",
                        plan["status"]
                    ])
                
                return history_data
            
            # Wire up events
            refresh_btn.click(
                fn=refresh_dashboard,
                outputs=[energy_display, emissions_display, anomalies_display,
                        energy_chart, status_table]
            )
            
            generate_btn.click(
                fn=generate_recommendations,
                outputs=[rec_status, recommendations_display, rec_details,
                        total_co2_savings, total_energy_savings]
            )
            
            submit_feedback_btn.click(
                fn=submit_feedback,
                inputs=[plan_selector, rec_selector, feedback_action, feedback_notes],
                outputs=[feedback_result]
            )
            
            load_history_btn.click(
                fn=load_history,
                outputs=[history_display]
            )
            
            # Auto-refresh on load
            interface.load(
                fn=refresh_dashboard,
                outputs=[energy_display, emissions_display, anomalies_display,
                        energy_chart, status_table]
            )
        
        return interface
    
    def launch(self):
        """Launch the Gradio app"""
        interface = self.create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,  # enable Gradio’s tunneling service
        )

if __name__ == "__main__":
    app = GreenWiseApp()
    app.launch()
