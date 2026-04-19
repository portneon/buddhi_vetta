import os
from dotenv import load_dotenv
load_dotenv('.env')

from langchain_community.vectorstores.upstash import UpstashVectorStore
from langchain_core.documents import Document

UPSTASH_VECTOR_REST_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")

# Data to be indexed
KNOWLEDGE_BASE = [
    {
        "id": "warn-lights",
        "problem": "Warning Lights",
        "symptoms": "Check engine light or other warning light on dashboard.",
        "causes": "ECU detects an error code triggered by a sensor.",
        "fix": "Professional diagnostic inspection to identify error code."
    },
    {
        "id": "sputter-eng",
        "problem": "Sputtering Engine",
        "symptoms": "Engine misfiring or running poorly, loss of power.",
        "causes": "Worn spark plugs, dirty fuel system, or clogged air filter.",
        "fix": "Replace spark plugs, fuel system cleaning, or air filter replacement."
    },
    {
        "id": "poor-fuel",
        "problem": "Poor Fuel Economy",
        "symptoms": "Noticing fewer miles per gallon (MPG).",
        "causes": "Dirty air filter, aged spark plugs, or faulty O2 sensors.",
        "fix": "Professional tune-up, replacing filters and old ignition parts."
    },
    {
        "id": "dead-batt",
        "problem": "Dead Battery",
        "symptoms": "Car won't start, clicking sound when turning key.",
        "causes": "Leaving lights on, old battery (3-6 years), or alternator issues.",
        "fix": "Jump start, cleaning connections, or battery replacement."
    },
    {
        "id": "flat-tire",
        "problem": "Flat Tires",
        "symptoms": "Tire visually flat, low pressure light on, pulling to one side.",
        "causes": "Wear and tear, puncture from nails/debris, or valve stem leak.",
        "fix": "Tire repair (patch/plug) or complete tire replacement."
    },
    {
        "id": "sq-brakes",
        "problem": "Brakes Squeaking/Grinding",
        "symptoms": "High-pitched squeak or grinding metal sound when braking.",
        "causes": "Worn brake pads or warped rotors.",
        "fix": "Replace brake pads and/or resurface or replace rotors."
    },
    {
        "id": "alt-fail",
        "problem": "Alternator Failure",
        "symptoms": "Dimming headlights, battery light on, car stalling while driving.",
        "causes": "Internal alternator failure, unable to charge battery.",
        "fix": "Replace alternator and potentially the battery if it was drained."
    },
    {
        "id": "start-fail",
        "problem": "Broken Starter Motor",
        "symptoms": "Single click when turning key, lights on but engine doesn't crank.",
        "causes": "Failing starter solenoid or motor components.",
        "fix": "Replace starter motor assembly."
    },
    {
        "id": "sh-wheel",
        "problem": "Steering Wheel Shaking",
        "symptoms": "Vibration felt through the wheel, especially at high speeds.",
        "causes": "Unbalanced tires, poor wheel alignment, or suspension wear.",
        "fix": "Tire balancing, wheel alignment, or suspension repair."
    },
    {
        "id": "emiss-fail",
        "problem": "Failed Emissions Test",
        "symptoms": "Failing a mandatory state emissions/smog test.",
        "causes": "Faulty O2 sensor, bad catalytic converter, or EVAP system leak.",
        "fix": "Repair specific emissions component identified by diagnostic scan."
    },
    {
        "id": "overheat",
        "problem": "Overheating",
        "symptoms": "Temperature gauge in the red, steam from under hood.",
        "causes": "Coolant leak, malfunctioning thermostat, or broken water pump.",
        "fix": "Flush radiator, replace thermostat, or replace water pump."
    },
    {
        "id": "slip-trans",
        "problem": "Slipping Transmission",
        "symptoms": "Engine revs but car doesn't speed up, delayed shifts.",
        "causes": "Low transmission fluid, damaged seals, gaskets, or clogged lines.",
        "fix": "Transmission service, fluid top-off, or seal/gasket replacement."
    },
    # Common DTC Codes
    {
        "id": "dtc-p0300",
        "problem": "P0300: Random/Multiple Cylinder Misfire Detected",
        "symptoms": "Engine shaking, hesitating, or loss of power.",
        "causes": "Worn spark plugs, faulty ignition coils, fuel system issues.",
        "fix": "Inspect and replace spark plugs and ignition coils."
    },
    {
        "id": "dtc-p0420",
        "problem": "P0420: Catalyst System Efficiency Below Threshold",
        "symptoms": "Check engine light, failed emissions test.",
        "causes": "Damaged catalytic converter, exhaust leak, faulty O2 sensor.",
        "fix": "Identify exhaust leaks or replace the catalytic converter."
    }
]

def init_vector_db():
    if not UPSTASH_VECTOR_REST_URL or not UPSTASH_VECTOR_REST_TOKEN:
        print("Error: UPSTASH_VECTOR_REST_URL or UPSTASH_VECTOR_REST_TOKEN not set.")
        return

    # Initialize the Vector Store
    # We use embedding=True because Upstash handles embeddings on their side
    vector_store = UpstashVectorStore(
        index_url=UPSTASH_VECTOR_REST_URL,
        index_token=UPSTASH_VECTOR_REST_TOKEN,
        embedding=True
    )

    documents = []
    for item in KNOWLEDGE_BASE:
        # Create a searchable text representation
        searchable_text = f"Problem: {item['problem']}. Symptoms: {item['symptoms']}. Causes: {item['causes']}. Fix: {item['fix']}"
        
        doc = Document(
            page_content=searchable_text,
            metadata=item
        )
        documents.append(doc)

    print(f"Upserting {len(documents)} documents into Upstash using LangChain...")
    
    try:
        # Clear existing data first by using a new collection or just adding
        # LangChain doesn't have a simple "clear" for Upstash yet, so we just add.
        # Upstash Vector REST API can handle multiple upserts to same ID.
        vector_store.add_documents(documents)
        print("Successfully initialized vector database with LangChain!")
    except Exception as e:
        print(f"Failed to upsert data: {e}")

if __name__ == "__main__":
    init_vector_db()
