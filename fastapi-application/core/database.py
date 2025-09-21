from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


async_engine = create_async_engine(
    url=settings.db_url_asyncpg,
    echo=False,
)

async_session_maker = async_sessionmaker(async_engine)

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
            finally:
                await session.close()
    return wrapper

