from src.proposal_writer import schemas
import src.proposal_writer.prompts as prompts
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import uuid

class BusinessPlanWriter:
    PROMPTS = {
        "system": prompts.system_prompt.prompt,
        schemas.GeneralInfo: prompts.general_prompt.prompt,
        schemas.ProblemPointsInfo: prompts.problempoints_prompt.prompt,
        schemas.SolutionPointsInfo: prompts.solutionpoints_prompt.prompt,
        schemas.BudgetInfo: prompts.budget_prompt.prompt,
        schemas.StrategyInfo: prompts.strategy_prompt.prompt,
        schemas.TeamInfo: prompts.team_prompt.prompt,
        schemas.Summary: prompts.summary_prompt.prompt,
    }

    _store = {}

    # _default_llm = ChatOpenAI(model="gpt-5")
    _default_llm = ChatOpenAI(
        openai_api_key="EMPTY",
        openai_api_base="http://localhost:8000/v1",
        model="K-intelligence/Midm-2.0-Base-Instruct",
    )

    def __init__(self, llm=None, session_id=None):
        self.llm = llm or self._default_llm
        self.session_id = session_id or str(uuid.uuid4())
        self.history = self._get_session_history()

        self.general_chain = self._make_chain(schemas.GeneralInfo)
        self.problem_chain = self._make_chain(schemas.ProblemPointsInfo)
        self.solution_chain = self._make_chain(schemas.SolutionPointsInfo)
        self.budget_chain = self._make_chain(schemas.BudgetInfo)
        self.scaleup_chain = self._make_chain(schemas.StrategyInfo)
        self.team_chain = self._make_chain(schemas.TeamInfo)
        self.summary_chain = self._make_chain(schemas.Summary)

    def _get_session_history(self) -> ChatMessageHistory:
        if self.session_id not in self._store:
            self._store[self.session_id] = ChatMessageHistory()
        return self._store[self.session_id]

    def _make_chain(self, schema):
        system_msg = self.PROMPTS["system"]["system"]
        user_msg = self.PROMPTS[schema]["user"]
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", system_msg
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "user", user_msg
                ), 
            ]
        )
        return prompt | self.llm.with_structured_output(schema)

    def write_general_status(self):
        request = f"{list(schemas.GeneralInfo.model_fields.keys())} 항목을 작성하라."
        out = self.general_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out

    def write_problem(self):
        request = f"{list(schemas.ProblemPointsInfo.model_fields.keys())} 항목을 작성하라."
        out = self.problem_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out

    def write_solution(self):
        request = f"{list(schemas.SolutionPointsInfo.model_fields.keys())} 항목을 작성하라."
        out = self.solution_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out

    def write_budget(self):
        request = f"{list(schemas.BudgetInfo.model_fields.keys())} 항목을 작성하라."
        out = self.budget_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out

    def write_scaleup(self):
        request = f"{list(schemas.StrategyInfo.model_fields.keys())} 항목을 작성하라."
        out = self.scaleup_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out

    def write_team(self):
        request = f"{list(schemas.TeamInfo.model_fields.keys())} 항목을 작성하라."
        out = self.team_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out

    def write_summary(self):
        request = f"{list(schemas.Summary.model_fields.keys())} 항목을 작성하라."
        out = self.summary_chain.invoke({"request": request, "chat_history": self.history.messages})
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        return out
    
writer = BusinessPlanWriter()
problem = {}
problem.update(writer.write_general_status().model_dump())
print(problem)