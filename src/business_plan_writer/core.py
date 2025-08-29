from src.business_plan_writer import schemas
from src.business_plan_writer.utils import render_docx_template
import src.business_plan_writer.prompts as prompts

from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from pathlib import Path
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

    try:
        # _default_llm = ChatOpenAI(model="gpt-5")
        _default_llm = ChatOpenAI(
            openai_api_key="EMPTY",
            openai_api_base="http://localhost:8000/v1",
            model="K-intelligence/Midm-2.0-Base-Instruct",
        )
        logger.info(f"LLM 초기화 완료")
    except Exception as e:
        logger.error(f"LLM 초기화 실패: {e}")
        raise


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

        try:
            out = self.general_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")

        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("GeneralInfo 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out

    def write_problem(self):
        request = f"{list(schemas.ProblemPointsInfo.model_fields.keys())} 항목을 작성하라."
        
        try:
            out = self.problem_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")

        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("ProblemPointsInfo 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out

    def write_solution(self):
        request = f"{list(schemas.SolutionPointsInfo.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.solution_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")

        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("SolutionPointsInfo 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out

    def write_budget(self):
        request = f"{list(schemas.BudgetInfo.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.budget_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
            
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("BudgetInfo 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out

    def write_scaleup(self):
        request = f"{list(schemas.StrategyInfo.model_fields.keys())} 항목을 작성하라."
        
        try:
            out = self.scaleup_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
            
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("StrategyInfo 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out

    def write_team(self):
        request = f"{list(schemas.TeamInfo.model_fields.keys())} 항목을 작성하라."        

        try:
            out = self.team_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
            
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("TeamInfo 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out

    def write_summary(self):
        request = f"{list(schemas.Summary.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.summary_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
        
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("Summary 작성 완료 | 생성 필드 수=%d", len(out.model_dump()))
        return out
    
    def write_all(self):
        businessplan = {}
        businessplan.update(self.write_general_status().model_dump())
        businessplan.update(self.write_problem().model_dump())
        businessplan.update(self.write_solution().model_dump())
        businessplan.update(self.write_budget().model_dump())
        businessplan.update(self.write_scaleup().model_dump())
        businessplan.update(self.write_team().model_dump())
        businessplan.update(self.write_summary().model_dump())

        module_dir = Path(__file__).resolve().parent
        template_path = module_dir / "사업계획서_양식.docx"
        out_path = Path("사업계획서.docx")
        render_docx_template(template_path, businessplan, out_path)
        return businessplan

if __name__ == "__main__":
    BusinessPlanWriter().write_all()