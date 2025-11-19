from http.client import responses
# 유비콘
from fastapi import FastAPI
from lark.parsers.earley_common import Item # 이거 없으면 왜안됨?
from pydantic import BaseModel
    # 데이터 유효성 검사와 설정 관리에 사용되는 라이브러리(모델링이 쉽고 강력함)
from starlette.middleware.base import BaseHTTPMiddleware
    # 요청과 응답사이에 특정작업 수행
    # 미들웨어는 모든 요청에 대해 실행되며, 요청을 처리하기 전에 응답을 반환하기 전에 특정 작업을 수행할수 있음
    # 예를 들어 로깅, 인증, cors처리, 압축 등
import logging # 로깅 처리용 메서드


app = FastAPI(                      # 앱의 시그니쳐와 환경설정을 담당
    title="My First API",           # 앱의 제목
    description="My First API",     # 앱의 주석(설명)
    version="0.0.1",                # 앱의 버전
    docs_url=None,                  # http://127.0.0.1:8001/docs,http://localhost:8001/docs 보안상 None처리
    redoc_url=None,                 # http://127.0.0.1:8001/redocs, http://localhost:8001/docs 보안상 None처리
) # java -> new FastAPI();

class LoggingMiddleware(BaseHTTPMiddleware):
    logging.basicConfig(level=logging.INFO)
    async def dispatch(self, request, call_next):
        logging.info(f"Req: {request.method}{request.url}")
        response = await call_next(request)
        logging.info(f"Status Code : {response.status_code}")
        return response

class Item(BaseModel):  # Item 객체 todtjd (BaseModel : 객체 연결 -> 상속)
    name: str               # 상품명 : 문자열
    description: str        # 상품설명 : 문자열(null)
    price: float            # 가격 : 실수형
    tax: float = None       # 세금 : 실수형(null)
# rest API : get, post, put, delete, patch

@app.post("/items/")        # post 메서드용 요청 (create)
async def create_item(item: Item):
        # BaseModel은 데이터 모델링을 쉽게 도와주고 유효성 검사도 수행
        # 잘못된 데이터가 들어오면 442 오류코드를 반환
    return item

@app.get("/")       # 웹 브라우져에 http://localhost:8001/ get요청시 처리
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}") # http://localhost:8001/item/1 -> get요청시
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
    # item_id : 상품의 번호 -> 경로 매개변수
    # q: 쿼리 매개변수(기본값none)

# postman은 프론트가 없는 백엔드 테스트용 프로그램으로 활용
# 서버 실행은 > python -m uvicorn main:app --reload --port 8001
# 파이썬 백엔드 가동 서버로 main.py에 app라는 메서드를 사용
#                                           갱신         포트번호 변경 8001



