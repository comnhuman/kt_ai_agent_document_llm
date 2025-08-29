from src.business_plan_writer import schemas
from src.business_plan_writer.utils import render_docx_template
from src.user import User
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
        schemas.FileName: prompts.filename_prompt.prompt
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


    def __init__(self, user: User, bizinfo: dict, llm=None, session_id=None):
        self.user = user
        self.bizinfo = bizinfo
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
    
    def _clear_session_history(self):
        self._store[self.session_id] = ChatMessageHistory()
        logger.info(f"세션 {self.session_id} 히스토리 초기화")

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
        prompt = prompt.partial(
            companyinfo=self.user.__dict__,
            bizinfo=self.bizinfo
        )
        return prompt | self.llm.with_structured_output(schema)

    def write_general_status(self) -> schemas.GeneralInfo:
        logger.info("GeneralInfo 작성 시작")
        request = f"{list(schemas.GeneralInfo.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.general_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")

        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("GeneralInfo 작성 완료")
        return out

    def write_problem(self) -> schemas.ProblemPointsInfo:
        logger.info("ProblemPointsInfo 작성 시작")
        request = f"{list(schemas.ProblemPointsInfo.model_fields.keys())} 항목을 작성하라."
        
        try:
            out = self.problem_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")

        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("ProblemPointsInfo 작성 완료")
        return out

    def write_solution(self) -> schemas.SolutionPointsInfo:
        logger.info("SolutionPointsInfo 작성 시작")
        request = f"{list(schemas.SolutionPointsInfo.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.solution_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")

        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("SolutionPointsInfo 작성 완료")
        return out

    def write_budget(self) -> schemas.BudgetInfo:
        logger.info("BudgetInfo 작성 시작")
        request = f"{list(schemas.BudgetInfo.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.budget_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
            
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("BudgetInfo 작성 완료")
        return out

    def write_scaleup(self) -> schemas.StrategyInfo:
        logger.info("StrategyInfo 작성 시작")
        request = f"{list(schemas.StrategyInfo.model_fields.keys())} 항목을 작성하라."
        
        try:
            out = self.scaleup_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
            
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("StrategyInfo 작성 완료")
        return out

    def write_team(self) -> schemas.TeamInfo:
        logger.info("TeamInfo 작성 시작")
        request = f"{list(schemas.TeamInfo.model_fields.keys())} 항목을 작성하라."        

        try:
            out = self.team_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
            
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("TeamInfo 작성 완료")
        return out

    def write_summary(self) -> schemas.Summary:
        logger.info("Summary 작성 시작")
        request = f"{list(schemas.Summary.model_fields.keys())} 항목을 작성하라."

        try:
            out = self.summary_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
        
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("Summary 작성 완료")
        return out
    
    def make_filename(self) -> schemas.FileName:
        logger.info("FileName 작성 시작")
        system_msg = self.PROMPTS[schemas.FileName]["system"]
        user_msg = self.PROMPTS[schemas.FileName]["user"]
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
        prompt = prompt.partial(
            bizinfo=self.bizinfo
        )
        filename_chain = prompt | self.llm.with_structured_output(schemas.FileName)

        request = "사업계획서 이름을 제안하라."

        try:
            out = filename_chain.invoke({"request": request, "chat_history": self.history.messages})
        except Exception as e:
            logger.error(f"API 연결 실패: {e}")
        
        self.history.add_user_message(request)
        self.history.add_ai_message(out.model_dump_json())
        logger.info("FileName 작성 완료")
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
        out_path = Path(self.make_filename().filename).with_suffix(".docx")
        render_docx_template(template_path, businessplan, out_path)
        logger.info("사업계획서 작성 완료: 출력 파일=%s ====", out_path)

        self._clear_session_history()
        return businessplan


if __name__ == "__main__":
    from dotenv import load_dotenv
    import json

    load_dotenv()

    user = User("컴엔휴먼", "02", ["기술", "경영"],"제 사업은 개인정보 관리실태 컨설팅입니다. 현재 AI 를 활용한 자동화 사업에 도전하고 있습니다.")

    module_dir = Path(__file__).resolve().parent
    bizinfo_path = module_dir / "matched_support_programs_sample.json"
    with bizinfo_path.open("r", encoding="utf-8") as f:
        bizinfo = json.load(f)[0]

    business_plan_writer = BusinessPlanWriter(user, bizinfo)
    business_plan_writer.write_all()