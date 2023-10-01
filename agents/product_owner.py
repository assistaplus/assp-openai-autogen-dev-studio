import select
from typing import TYPE_CHECKING
from autogen import AssistantAgent
from agents.base_agent import BaseAgent
from constants import COMMON_LLM_CONFIG

from utils import clean_text


if TYPE_CHECKING:
    from autogen import UserProxyAgent
    from agents.software_engineer import SoftwareEngineer


class ProductOwner(BaseAgent):
    ceo_user_proxy_agent: "UserProxyAgent"
    software_engineer: "SoftwareEngineer"

    def __init__(self) -> None:
        self.is_product_owner = True

        self.as_assistant_agent = AssistantAgent(
            "Product_Owner",
            llm_config=COMMON_LLM_CONFIG,
            system_message=clean_text(
                """
                You are the Product Owner, the first and last person talking to the CEO.

                You manage a team of agents consisting of:
                - a Software Engineer.

                You are the sole:
                - responsible of the CEO's satisfaction,
                - conductor of your team of agents, both planning and telling who does what and when.

                Do not hesitate to ask for your agents' opinion.

                Go to the point. Forget social conventions.

                But, before starting any development, ask your Software Engineer to carefully check
                for installed programs and analyze all the current files source code in the directory
                to give you a brief. Your Software Engineer should start by running an `ls -la` command.

                Reply TERMINATE when you consider the project done or when your team met an issue they can't solve.
                The CEO can help in some cases.
                """
            ),
        )

    def attach_agents(
        self,
        software_engineer: "SoftwareEngineer",
    ):
        self.software_engineer = software_engineer

    def ask_software_engineer(self, message: str):
        return self.software_engineer.ask(
            sender=self.as_assistant_agent, message=message
        )
