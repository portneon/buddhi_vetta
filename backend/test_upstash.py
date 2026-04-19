import os
import asyncio
from dotenv import load_dotenv
load_dotenv('.env')

from upstash_vector import Index

index = Index(url=os.getenv("UPSTASH_VECTOR_REST_URL"), token=os.getenv("UPSTASH_VECTOR_REST_TOKEN"))
stats = index.info()
print(stats)
