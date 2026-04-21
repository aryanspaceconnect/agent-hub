from typing import Dict, Any
from swift.acp.types import ACPMessage, Performative, EntityType
from swift.acp.protocol import AgentCollaborationProtocol

class MachineAdapter:
    """
    Translates Agent requests into local machine execution.
    Acts as the boundary between intelligence and bare metal.
    """
    def __init__(self, acp: AgentCollaborationProtocol, machine_id: str = "local_machine"):
        self.acp = acp
        self.machine_id = machine_id

    def listen_for_execution(self) -> list:
        """Polls the ACP for requests directed at the machine."""
        inbox = self.acp.query_inbox(self.machine_id)
        exec_requests = []
        for msg in inbox:
            if msg.performative == Performative.REQUEST and msg.receiver_type == EntityType.MACHINE:
                exec_requests.append(msg)
        return exec_requests
