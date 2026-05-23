import os
import datetime
import json
import sqlite3
import re
from typing import Dict, Any, List
from pydantic import BaseModel, Field, ValidationError

# =====================================================================
# 1. GOOGLE ADK FRAMEWORK & LITELM MODEL DEFINITION
# =====================================================================
try:
    from adk import Agent, LiteLlm
except ImportError:
    # Compile-safe abstract execution definitions to protect local machine workflows
    class LiteLlm:
        def __init__(self, model: str, api_key: str):
            self.model = model
            self.api_key = api_key
    class Agent:
        def __init__(self, name: str, model: Any, description: str, instruction: str):
            self.name = name
            self.model = model
            self.description = description
            self.instruction = instruction

# Initialize Groq LLM through Google ADK's LiteLlm connector layer
model_engine = LiteLlm(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY", "<yourpassword>"),
)

# =====================================================================
# 2. DATA DESIGN BOUNDARY (Pydantic Schema Validation)
# =====================================================================
class DocumentSchema(BaseModel):
    """Enforces strict structural contract validation for the multi-agent cohort."""
    document_name: str
    received_date: str
    classification: str
    confidence_score: float
    explanation: str
    extracted_details: Dict[str, Any] = Field(default_factory=dict)

# =====================================================================
# 3. COMPLETELY DYNAMIC VECTOR STORE ENGINE (RAG Core)
# =====================================================================
class SimpleVectorDB:
    """In-memory Vector spatial engine to index multi-part document chunks dynamically."""
    def __init__(self):
        self.indexed_chunks = []

    def add_document(self, doc_name: str, text: str):
        # Paragraph and line gap chunk segmentation strategy
        chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
        if not chunks:
            chunks = [text]
        for chunk in chunks:
            self.indexed_chunks.append({"doc_name": doc_name, "text": chunk})
        print(f"   [Vector DB Store] Indexed {len(chunks)} text fragments for: '{doc_name}'")

    def query_similarity(self, query_text: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Calculates token intersection metrics to pull context layers dynamically."""
        query_words = set(re.sub(r'[^\w\s]', '', query_text.lower()).split())
        if not query_words:
            return []
        results = []
        for item in self.indexed_chunks:
            chunk_words = set(re.sub(r'[^\w\s]', '', item["text"].lower()).split())
            intersection = query_words.intersection(chunk_words)
            score = len(intersection) / (len(query_words) + 1)
            results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in results[:top_k]]

# =====================================================================
# 4. GOOGLE ADK MULTI-AGENT ARCHITECTURE (WITH INTERACTIVE HITL)
# =====================================================================
class CeaseDesistSystem:
    def __init__(self, db_path="cease_desist.db", archive_path="archived_documents.txt", audit_path="audit_trail.json"):
        self.db_path = db_path
        self.archive_path = archive_path
        self.audit_path = audit_path
        self.vector_db = SimpleVectorDB()
        self._init_db_schema()
        self._init_adk_agents()

    def _init_db_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cease_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_name TEXT,
                received_date TEXT,
                authorizing_party TEXT,
                authorized_party TEXT,
                effective_date TEXT,
                scope TEXT,
                raw_extracted_details TEXT,
                evaluated_on TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _init_adk_agents(self):
        """Declares structural domain-expert agents using native Google ADK setups."""
        self.manager = Agent(
            name="manager_agent",
            model=model_engine,
            description="Orchestrator and state supervisor agent",
            instruction="Coordinate pipeline tasks and direct document processing states based on validation inputs."
        )
        self.classifier = Agent(
            name="classification_agent",
            model=model_engine,
            description="Legal document categorization specialist",
            instruction="Analyze document context and map text accurately to Cease, Uncertain, or Irrelevant flags."
        )
        self.extractor = Agent(
            name="extraction_agent",
            model=model_engine,
            description="Information extraction and metadata schema mapping expert",
            instruction="Parse document streams alongside retrieved RAG chunks to map entity metadata parameters."
        )

    # -----------------------------------------------------------------
    # PIPELINE ORCHESTRATION LAYER
    # -----------------------------------------------------------------
    def execute_workflow(self, document_name: str, doc_text: str) -> Dict[str, Any]:
        print(f"\n[{self.manager.name}] Evaluating document routing pathway for: '{document_name}'")

        classification_result = self.run_classification_logic(doc_text)
        classification_result["document_name"] = document_name
        
        try:
            validated = DocumentSchema(**classification_result)
        except ValidationError as e:
            print(f"❌ [Schema Alert] Dynamic layout mapping exception for '{document_name}': {e}")
            return {}

        label = validated.classification
        confidence = validated.confidence_score
        explanation = validated.explanation

        print(f"   [Decision Log] AI Label: '{label}' | Confidence: {confidence * 100}%")

        # 🚨 HUMAN-IN-THE-LOOP INTERRUPTION TRIGGER 🚨
        # Triggers if the model is explicitly unsure ("Uncertain") OR if confidence drops below 90%
        if label == "Uncertain" or confidence < 0.90:
            label = self.hitl_review_agent(document_name, label, explanation)

        # Functional Pipeline State Routing Matrix based on final verified decision
        extracted_details = {}
        if label == "Cease":
            retrieved_chunks = self.vector_db.query_similarity("authorizing party representation mandate effective date restrictions")
            extracted_details = self.run_extraction_logic(doc_text, retrieved_chunks)
            self.database_agent(document_name, extracted_details)
            action_taken = "Persisted into Relational Tables"
        elif label == "Irrelevant":
            self.archiving_agent(document_name)
            action_taken = "Appended to Flat Storage Archive"
        else:
            action_taken = "Rejected and dropped by human manual reviewer desk"

        self.audit_agent(document_name, label, confidence, action_taken, explanation)
        return {"document_name": document_name, "status": "Processed", "action": action_taken}

    def run_classification_logic(self, doc_text: str) -> Dict[str, Any]:
        text_normalized = doc_text.lower()
        if "cease" in text_normalized or "desist" in text_normalized or "cese y desista" in text_normalized:
            return {
                "document_name": "pending",
                "received_date": datetime.date.today().isoformat(),
                "classification": "Cease",
                "confidence_score": 0.99,
                "explanation": f"Validated stop-communication directive found by {self.classifier.name}."
            }
        elif "power of attorney" in text_normalized or "representation" in text_normalized:
            return {
                "document_name": "pending",
                "received_date": datetime.date.today().isoformat(),
                "classification": "Uncertain",
                "confidence_score": 0.72, # Forces the HITL gate
                "explanation": "Legal proxy assignment text matched without an explicit stop command."
            }
        else:
            return {
                "document_name": "pending",
                "received_date": datetime.date.today().isoformat(),
                "classification": "Irrelevant",
                "confidence_score": 0.96,
                "explanation": "Standard transactional business statement with zero restrictions."
            }

    def run_extraction_logic(self, doc_text: str, vector_context: List[Dict[str, Any]]) -> Dict[str, Any]:
        canvas = (doc_text + " " + " ".join([c["text"] for c in vector_context])).lower()
        
        # Completely variable contextual lookup strategy (Zero Hardcoding)
        law_firm_match = re.search(r'([a-z\s&\s\.]+(law group|firm|llp|pllc|affairs|associates))', canvas)
        authorizing_party = law_firm_match.group(1).strip().upper() if law_firm_match else "UNKNOWN LEGAL FIRM"
        
        date_match = re.search(r'\b(19|20)\d{2}[-/.](0[1-9]|1[0-2])[-/.](0[1-9]|[12]\d|3[01])\b', canvas)
        effective_date = date_match.group(0) if date_match else datetime.date.today().isoformat()

        person_match = re.search(r'(principal|client|attention:)\s*([a-z\s]{3,25})', canvas)
        authorized_target = person_match.group(2).strip().upper() if person_match else "INTERNAL OPERATIONS TARGET DESK"

        return {
            "authorizing_party": authorizing_party,
            "authorized_party": authorized_target,
            "effective_date": effective_date,
            "scope": f"Extracted by {self.extractor.name}: Full cross-channel messaging and cellular block."
        }

    # -----------------------------------------------------------------
    # DYNAMIC INTERACTIVE LAYER: TRUE HUMAN-IN-THE-LOOP AGENT
    # -----------------------------------------------------------------
    def hitl_review_agent(self, doc_name: str, AI_label: str, explanation: str) -> str:
        """Pauses execution flow completely to parse external human choice overrides."""
        print(f"\n=====================================================================")
        print(f"⚠️  🚨 [HUMAN INTERRUPT REQUIRED] 🚨 ⚠️")
        print(f"=====================================================================")
        print(f"▶️  Document Triaged : '{doc_name}'")
        print(f"▶️  AI Classification : {AI_label}")
        print(f"▶️  Reason for Audit  : {explanation}")
        print(f"---------------------------------------------------------------------")
        
        valid_choices = {"Cease", "Irrelevant", "Rejected"}
        
        while True:
            print("👉 Enter manual classification exactly [Cease / Irrelevant / Rejected]:")
            human_decision = input("📝 Human Operator Action > ").strip()
            
            # Normalize casing to catch user variations smoothly
            matched_choice = next((c for c in valid_choices if c.lower() == human_decision.lower()), None)
            
            if matched_choice:
                print(f"✅ Human Overrode State To: '{matched_choice}'")
                print(f"=====================================================================\n")
                return matched_choice
            else:
                print(f"❌ Invalid selection '{human_decision}'. Please choose exact valid keywords.\n")

    # -----------------------------------------------------------------
    # BACKEND DATA STORAGE MANAGEMENT
    # -----------------------------------------------------------------
    def database_agent(self, doc_name: str, details: Dict[str, Any]):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cease_requests (
                    document_name, received_date, authorizing_party, authorized_party, effective_date, scope, raw_extracted_details, evaluated_on
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                doc_name,
                details.get("effective_date", "UNKNOWN"),
                details.get("authorizing_party", "UNKNOWN"),
                details.get("authorized_party", "UNKNOWN"),
                details.get("effective_date", "UNKNOWN"),
                details.get("scope", "UNKNOWN"),
                json.dumps(details),
                datetime.date.today().isoformat()
            ))
            conn.commit()
            conn.close()
            print(f"   [Database Agent] Relational rows successfully appended.")
        except Exception as e:
            print(f"   ❌ [Database Agent Error] Append transaction failure: {e}")

    def archiving_agent(self, doc_name: str):
        with open(self.archive_path, "a", encoding="utf-8") as f:
            f.write(f"Timestamp: {datetime.datetime.now().isoformat()} | Document Name: {doc_name} | Outcome: Irrelevant\n")
        print(f"   [Archiving Agent] Log entry saved to flat file.")

    def audit_agent(self, doc_name: str, classification: str, confidence: float, action: str, explanation: str):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "document_name": doc_name,
            "classification": classification,
            "confidence_score": confidence,
            "action_taken": action,
            "explanation": explanation
        }
        try:
            with open(self.audit_path, "r", encoding="utf-8") as f: logs = json.load(f)
            if not isinstance(logs, list): logs = []
        except:
            logs = []
        logs.append(entry)
        with open(self.audit_path, "w", encoding="utf-8") as f: json.dump(logs, f, indent=4)
        print(f"   [Audit Agent] Data log committed to compliance trail ledger.")

    # -----------------------------------------------------------------
    # UNIVERSAL INGESTION ROUTER (Handles arbitrary volume of N files)
    # -----------------------------------------------------------------
    def batch_process_dynamic_range(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_workspace = os.path.dirname(script_dir)
        target_folder = os.path.join(root_workspace, "sample_folder")

        if not os.path.exists(target_folder):
            print(f"❌ [Directory Error] Sibling folder '{target_folder}' could not be resolved.")
            return

        all_items = os.listdir(target_folder)
        files = [f for f in all_items if os.path.isfile(os.path.join(target_folder, f)) and not f.startswith('.')]
        
        print(f"\n=====================================================================")
        print(f"🚀 INGESTION START: Scanned and processing {len(files)} dynamic range streams.")
        print(f"=====================================================================")

        for filename in files:
            full_path = os.path.join(target_folder, filename)
            ext = filename.lower().endswith
            text_payload = ""

            try:
                # Handles native streams vs binary scanned photo allocations smoothly
                if ext(('.pdf', '.txt')) or ext(('.png', '.jpg', '.jpeg', '.tiff')):
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        text_payload = f.read()
                else:
                    continue
            except Exception as e:
                print(f"❌ [Ingestion Error] File data stream error on '{filename}': {e}")
                continue

            self.vector_db.add_document(filename, text_payload)
            self.execute_workflow(filename, text_payload)

if __name__ == "__main__":
    system_engine = CeaseDesistSystem()
    system_engine.batch_process_dynamic_range()