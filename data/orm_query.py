from sqlalchemy import select, delete

from data.models import Question

async def create_question(chat_id, text, session):
    obj = Question(
        chat_id=chat_id,
        question=text
    )
    session.add(obj)
    await session.commit()


async def create_answer(text, session):
    query = select(Question.chat_id).where(Question.question == text)
    data = await session.execute(query)
    chat_id = data.scalar()

    query_2 = delete(Question).where(Question.question == text)
    data = await session.execute(query_2)
    await session.commit()

    return chat_id