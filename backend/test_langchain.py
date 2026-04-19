import os
import asyncio
from dotenv import load_dotenv
load_dotenv('.env')

from rag_service import get_chat_response

async def main():
    try:
        res = await get_chat_response("Hello", [])
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())
