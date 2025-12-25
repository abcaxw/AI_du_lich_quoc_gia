# app/coreAI/agents/agent_destination_info.py
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

import dlog
from common_utils.datetime_utils import get_current_date_info
from coreAI.agents.agent_base import BaseAgent
from coreAI.tools.destination_tools import (
    retriever_destination_info_tool,
    get_destination_details_tool,
    get_nearby_attractions_tool,
    get_events_and_festivals_tool
)
from dconfig import config_agents, config_prompts_path


class DestinationInfoResponse(BaseModel):
    """Response cho agent thông tin điểm đến"""
    ai_message: str = Field(description="Nội dung trả lời về điểm đến, bao gồm hình ảnh và link")
    next_agent: str = Field(
        description=f"""
        Agent tiếp theo:
        - '{config_agents.AGENT_ITINERARY_PLANNING}': Khách muốn lên lịch trình
        - '{config_agents.AGENT_BOOKING_SERVICE}': Khách muốn đặt dịch vụ
        - 'HUMAN': Tiếp tục tư vấn
        - 'END': Kết thúc
        """,
        examples=[config_agents.AGENT_ITINERARY_PLANNING, config_agents.AGENT_BOOKING_SERVICE, 'HUMAN', 'END']
    )
    destination_details: dict = Field(
        default_factory=dict,
        description="Thông tin chi tiết điểm đến đã tư vấn"
    )


class DestinationInfoAgent(BaseAgent):
    def invoke(self, state):
        dlog.dlog_i("--- DESTINATION_INFO Agent ---")
        current_time, day_of_week = get_current_date_info()
        config: RunnableConfig = {"configurable": {"thread_id": state["thread_id"]}}

        customer_location = state.get("customer_location", "Hà Nội, Việt Nam")

        input_data = {
            "messages": state["messages"],
            "current_time": current_time,
            "day_of_week": day_of_week,
            "customer_location": customer_location
        }

        # Setup agent với tools
        self.setup_agent(
            system_prompt_path=config_prompts_path.DESTINATION_INFO_PROMPT,
            tools=[
                retriever_destination_info_tool,
                get_destination_details_tool,
                get_nearby_attractions_tool,
                get_events_and_festivals_tool
            ],
            variables=input_data,
            response_class=DestinationInfoResponse
        )

        # Invoke agent
        response = self.agent.invoke(input=input_data, config=config)

        # Update state
        ai_message = response["structured_response"].ai_message
        state["messages"].append(AIMessage(content=ai_message))
        state["ai_message"] = ai_message
        state["current_agent"] = config_agents.AGENT_DESTINATION_INFO
        state["next_agent"] = response["structured_response"].next_agent.upper()
        state["destination_details"] = response["structured_response"].destination_details

        return state


def destination_info_node(state):
    """Node cho agent thông tin điểm đến"""
    agent = DestinationInfoAgent()
    return agent.invoke(state)