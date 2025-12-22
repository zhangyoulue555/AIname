from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
import string
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
from aiosmtplib import SMTPResponseException

from dependencies import get_mail,get_session
from repository.user_repo import EmailCodeRepository, UserRepository
from schemas import ResponseOut
from models import AsyncSession
from schemas.user_schemas import RegisterIn, UserCreateSchema

router = APIRouter(prefix="/auth")

@router.get("/code", response_model=ResponseOut)
async def get_email_code(
        email: Annotated[EmailStr, Query(...)],
        mail: FastMail = Depends(get_mail),
        session: AsyncSession = Depends(get_session),
):
    # 生成验证码
    source = string.digits * 4
    code = "".join(random.sample(source, 4))
    message = MessageSchema(
        subject="【AiName起名助手】注册验证码",
        recipients=[email],
        body=f"【AiName起名助手】您的注册验证码为：{code}，5分钟有效。",
        subtype=MessageType.plain
    )
    try:
        print(f"验证码：{code}")
        await mail.send_message(message)
    except SMTPResponseException as e:
        # 检查是否是 QQ 特有的二进制响应错误
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("⚠️ 忽略 QQ 邮箱 SMTP 关闭阶段的非标准响应（邮件已成功发送）")
            email_code_repo = EmailCodeRepository(session)
            await email_code_repo.create(email=str(email), code=code)
            # 可选：记录日志，但不中断流程
        else:
            raise HTTPException(500, "邮件发送失败！")
    return ResponseOut()

@router.post('/register', response_model=ResponseOut)
async def register(data: RegisterIn, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)
    if await user_repo.email_is_exist(str(data.email)):
        raise HTTPException(status_code=400, detail="邮箱已经存在！")
    email_code_repo = EmailCodeRepository(session)
    if not await email_code_repo.check_email_code(email=str(data.email), code=data.code):
        raise HTTPException(status_code=400, detail="邮箱验证码错误！")
    await user_repo.create(UserCreateSchema(email=data.email, username=data.username, password=data.password))
    return ResponseOut()