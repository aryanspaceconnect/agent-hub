import unittest
from swift.acp.protocol import AgentCollaborationProtocol
from swift.acp.types import ACPMessage, Performative, EntityType
from ether.adapters.human_interface import HumanAdapter
from ether.adapters.machine_interface import MachineAdapter

class TestFederationAndSecurity(unittest.TestCase):
    def setUp(self):
        self.acp = AgentCollaborationProtocol()
        self.human = HumanAdapter(self.acp)
        self.machine = MachineAdapter(self.acp, "local_os_1")

    def test_human_to_agent_flow(self):
        """Test that a human can successfully send a task via adapter"""
        human_id = "human_user_1"
        agent_id = "agent_worker_1"

        conv_id = self.human.send_task_to_agent(human_id, agent_id, "Write a report on gravity")

        # Check that the message arrived at the agent
        inbox = self.acp.query_inbox(agent_id)
        self.assertEqual(len(inbox), 1)
        self.assertEqual(inbox[0].sender, human_id)
        self.assertEqual(inbox[0].sender_type, EntityType.HUMAN)
        self.assertEqual(inbox[0].performative, Performative.REQUEST)

    def test_machine_sandboxing(self):
        """Test that agents cannot send illegal commands to machines"""
        # Valid request
        valid_msg = ACPMessage(
            sender="agent_x",
            receiver="local_os_1",
            sender_type=EntityType.AGENT,
            receiver_type=EntityType.MACHINE,
            performative=Performative.REQUEST,
            content={"cmd": "ls -la"}
        )
        self.assertTrue(self.acp.dispatch(valid_msg))

        # Invalid performative (e.g., trying to force a COMMIT onto a machine without negotiation)
        invalid_msg = ACPMessage(
            sender="agent_x",
            receiver="local_os_1",
            sender_type=EntityType.AGENT,
            receiver_type=EntityType.MACHINE,
            performative=Performative.COMMIT,
            content={"cmd": "rm -rf /"}
        )
        self.assertFalse(self.acp.dispatch(invalid_msg))

    def test_context_bounding(self):
        """Test that massive payloads are rejected by the immune system"""
        massive_data = "x" * 2000000 # 2MB string

        bloat_msg = ACPMessage(
            sender="agent_spammer",
            receiver="agent_victim",
            performative=Performative.INFORM,
            content={"payload": massive_data}
        )

        # The immune system should block this
        self.assertFalse(self.acp.dispatch(bloat_msg))

if __name__ == '__main__':
    unittest.main()
