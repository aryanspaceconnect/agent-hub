from typing import Dict, Any
from swift.acp.types import ACPMessage, Performative, EntityType
from swift.acp.protocol import AgentCollaborationProtocol

class HumanAdapter:
    """
    Translates Human Dashboard inputs into strict ACP Messages.
    """
    def __init__(self, acp: AgentCollaborationProtocol):
        self.acp = acp

    def send_task_to_agent(self, human_id: str, agent_id: str, task_description: str) -> str:
        """Human requests an agent to do something."""
        msg = ACPMessage(
            sender=human_id,
            receiver=agent_id,
            sender_type=EntityType.HUMAN,
            receiver_type=EntityType.AGENT,
            performative=Performative.REQUEST,
            content={"task": task_description}
        )
        self.acp.dispatch(msg)
        return msg.conversation_id

    def query_agent_status(self, human_id: str, agent_id: str) -> str:
        msg = ACPMessage(
            sender=human_id,
            receiver=agent_id,
            sender_type=EntityType.HUMAN,
            receiver_type=EntityType.AGENT,
            performative=Performative.QUERY,
            content={"query": "status"}
        )
        self.acp.dispatch(msg)
        return msg.conversation_id
