# app/coreAI/tourism_workflow.py
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

import dlog
from coreAI.agents import (
    supervisor,
    hello_node,
    destination_info_node,
    itinerary_planning_node,
    booking_service_node,
    weather_emergency_node,
    review_feedback_node,
    faq_node,
    human_node,
    other_node
)
from coreAI.agents.agent_supervisor import choose_worker
from dconfig import config_agents
from object_models.tourism_state import TourismState

INTERRUPT_BEFORE_AGENTS = [config_agents.AGENT_HUMAN]


class TourismAgentWorkflow:
    """Workflow quản lý các agent du lịch"""

    def __init__(self):
        self.chain = self.build_graph()

    @staticmethod
    def build_graph():
        """Xây dựng graph workflow"""
        workflow = StateGraph(TourismState)

        # Add nodes
        workflow.add_node(config_agents.AGENT_SUPERVISOR, supervisor)
        workflow.add_node(config_agents.AGENT_HELLO, hello_node)
        workflow.add_node(config_agents.AGENT_DESTINATION_INFO, destination_info_node)
        workflow.add_node(config_agents.AGENT_ITINERARY_PLANNING, itinerary_planning_node)
        workflow.add_node(config_agents.AGENT_BOOKING_SERVICE, booking_service_node)
        workflow.add_node(config_agents.AGENT_WEATHER_EMERGENCY, weather_emergency_node)
        workflow.add_node(config_agents.AGENT_REVIEW_FEEDBACK, review_feedback_node)
        workflow.add_node(config_agents.AGENT_FAQ, faq_node)
        workflow.add_node(config_agents.AGENT_HUMAN, human_node)
        workflow.add_node(config_agents.AGENT_OTHER, other_node)

        # Set entry point
        workflow.set_entry_point(config_agents.AGENT_SUPERVISOR)

        # Supervisor routing
        workflow.add_conditional_edges(
            config_agents.AGENT_SUPERVISOR,
            choose_worker,
            {
                config_agents.AGENT_HELLO: config_agents.AGENT_HELLO,
                config_agents.AGENT_DESTINATION_INFO: config_agents.AGENT_DESTINATION_INFO,
                config_agents.AGENT_ITINERARY_PLANNING: config_agents.AGENT_ITINERARY_PLANNING,
                config_agents.AGENT_BOOKING_SERVICE: config_agents.AGENT_BOOKING_SERVICE,
                config_agents.AGENT_WEATHER_EMERGENCY: config_agents.AGENT_WEATHER_EMERGENCY,
                config_agents.AGENT_REVIEW_FEEDBACK: config_agents.AGENT_REVIEW_FEEDBACK,
                config_agents.AGENT_FAQ: config_agents.AGENT_FAQ,
                config_agents.AGENT_OTHER: config_agents.AGENT_OTHER,
            }
        )

        # Hello -> END
        workflow.add_edge(config_agents.AGENT_HELLO, END)

        # Destination Info routing
        workflow.add_conditional_edges(
            config_agents.AGENT_DESTINATION_INFO,
            choose_worker,
            {
                config_agents.AGENT_ITINERARY_PLANNING: config_agents.AGENT_ITINERARY_PLANNING,
                config_agents.AGENT_BOOKING_SERVICE: config_agents.AGENT_BOOKING_SERVICE,
                config_agents.AGENT_HUMAN: config_agents.AGENT_HUMAN,
                "END": END
            }
        )

        # Itinerary Planning routing
        workflow.add_conditional_edges(
            config_agents.AGENT_ITINERARY_PLANNING,
            choose_worker,
            {
                config_agents.AGENT_BOOKING_SERVICE: config_agents.AGENT_BOOKING_SERVICE,
                config_agents.AGENT_DESTINATION_INFO: config_agents.AGENT_DESTINATION_INFO,
                config_agents.AGENT_HUMAN: config_agents.AGENT_HUMAN,
                "END": END
            }
        )

        # Booking Service routing
        workflow.add_conditional_edges(
            config_agents.AGENT_BOOKING_SERVICE,
            choose_worker,
            {
                config_agents.AGENT_HUMAN: config_agents.AGENT_HUMAN,
                "END": END
            }
        )

        # Weather/Emergency -> END
        workflow.add_edge(config_agents.AGENT_WEATHER_EMERGENCY, END)

        # Review/Feedback -> END
        workflow.add_edge(config_agents.AGENT_REVIEW_FEEDBACK, END)

        # FAQ -> END
        workflow.add_edge(config_agents.AGENT_FAQ, END)

        # Other -> END
        workflow.add_edge(config_agents.AGENT_OTHER, END)

        # Human routing
        workflow.add_conditional_edges(
            config_agents.AGENT_HUMAN,
            choose_worker,
            {
                config_agents.AGENT_DESTINATION_INFO: config_agents.AGENT_DESTINATION_INFO,
                config_agents.AGENT_ITINERARY_PLANNING: config_agents.AGENT_ITINERARY_PLANNING,
                config_agents.AGENT_BOOKING_SERVICE: config_agents.AGENT_BOOKING_SERVICE,
            }
        )

        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(
            checkpointer=memory,
            interrupt_before=INTERRUPT_BEFORE_AGENTS
        )

    def process(self, message: str, history: list, thread_id: str, customer: int, customer_location: str = None):
        """
        Xử lý tin nhắn từ khách hàng

        Args:
            message: Nội dung tin nhắn
            history: Lịch sử chat
            thread_id: ID thread
            customer: ID khách hàng
            customer_location: Vị trí khách hàng

        Returns:
            Response từ agent
        """
        dlog.dlog_i(f"Processing message: {message}")

        from langchain_core.runnables import RunnableConfig

        input_data = {
            "human_message": message,
            "thread_id": thread_id,
            "messages": history,
            "customer": customer,
            "customer_location": customer_location or "Hà Nội, Việt Nam",
            "customer_language": "vi"  # TODO: Detect language
        }

        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

        # Check if need to resume from interrupt
        current_state = self.chain.get_state(config)
        if len(current_state.next) > 0 and current_state.next[0] in INTERRUPT_BEFORE_AGENTS:
            self.chain.update_state(
                config=config,
                values=input_data,
                as_node=current_state.values["current_agent"]
            )
            input_data = None

        # Invoke workflow
        response = self.chain.invoke(input=input_data, config=config, stream_mode="values")

        dlog.dlog_i(f"Agent response: {response.get('ai_message', '')}")
        return response