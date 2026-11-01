import os
import json
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TRIGGER_COMMAND = os.environ.get("TRIGGER_COMMAND", "Arise Jago")

genai.configure(api_key=GEMINI_API_KEY)

MEMORY_FILE = "factory_memory.json"

def select_optimal_model(command_text):
    """
    कमांड की जटिलता को देखकर सही मॉडल खुद चुनना (Multi-Model Strategy):
    - अगर भारी कोडिंग या आर्किटेक्चर चाहिए -> Pro / Advanced Reasoning
    - अगर तेज रफ्तार रूटीन टास्क चाहिए -> Flash / Flash-Lite
    """
    cmd = command_text.lower()
    if any(keyword in cmd for keyword in ["code", "architect", "complex", "system", "deep"]):
        print("🧠 [Brain Switch] Activating Advanced Reasoning Model for complex task...")
        return genai.GenerativeModel('gemini-3.1-pro') # या आपके हिसाब से एडवांस्ड प्रो मॉडल
    else:
        print("⚡ [Brain Switch] Activating Ultra-Fast Flash Model for lightning speed...")
        return genai.GenerativeModel('gemini-2.5-flash')

def wake_up_and_sync_memory():
    print("⚡ [ARISES JAGO] Mother Factory awakening with Multi-Model Power...")
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
                print(f"🧠 [Memory Synchronized] Loaded {len(memory.get('immutable_ledger', []))} past records.")
                return memory
        except Exception as e:
            print(f"⚠️ Memory error: {e}")
            
    return {
        "factory_core": "Mother Factory Multi-Model 100x",
        "brain_status": "All Models Synchronized",
        "total_cycles": 0,
        "immutable_ledger": []
    }

def save_and_lock_memory(memory_data, action_name, result_data):
    memory_data["total_cycles"] += 1
    memory_data["immutable_ledger"].append({
        "cycle_id": memory_data["total_cycles"],
        "trigger": action_name,
        "state_summary": result_data[:200]
    })
    
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4)
    print("🔒 [GitHub Sync] Multi-Model state securely locked to JSON ledger.")

def execute_mother_factory():
    memory = wake_up_and_sync_memory()
    
    # सही मॉडल का चुनाव
    active_model = select_optimal_model(TRIGGER_COMMAND)
    
    prompt = f"""
    You are the supreme Mother AI of an autonomous 100x digital business factory.
    You are operating with MULTI-MODEL power, zero laziness, and absolute sharp focus.
    
    Synced GitHub Memory:
    {json.dumps(memory['immutable_ledger'][-3:], indent=2)}
    
    Current System Trigger: "{TRIGGER_COMMAND}"
    
    Task:
    Analyze the command, formulate the execution plan using optimal reasoning, and output the master strategy.
    """
    
    print("⚙️ [Deep Processing] Mother AI is computing...")
    response = active_model.generate_content(prompt)
    strategy_output = response.text
    
    print("\n--- 🌟 Mother Factory Master Plan (Multi-Model) ---")
    print(strategy_output)
    print("---------------------------------------------------\n")
    
    save_and_lock_memory(memory, TRIGGER_COMMAND, strategy_output)

if __name__ == "__main__":
    if TRIGGER_COMMAND.lower() in ["arise jago", "jag jao", "wake up"]:
        execute_mother_factory()
    else:
        print("💤 Factory waiting for the 'Arise Jago' command...")
        
