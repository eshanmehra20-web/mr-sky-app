import os
import json
import google.generativeai as genai

# गिटहब सीक्रेट्स से फुल-पॉवर एपीआई की उठाना
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TRIGGER_COMMAND = os.environ.get("TRIGGER_COMMAND", "Arise Jago")

# 200% मैक्सिमम ब्रेन पावर और स्पीड के साथ जेमिनी कॉन्फ़िगरेशन
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

MEMORY_FILE = "factory_memory.json"

def wake_up_and_sync_memory():
    """
    1. Arise Jago Protocol & Persistent Memory Check:
    गिटहब की JSON फाइल से पिछला सारा इतिहास बिना एक भी डेटा खोए लोड करना।
    भूलने की बीमारी हमेशा के लिए खत्म!
    """
    print("⚡ [ARISES JAGO] Mother Factory awakening with 200% Brain Power...")
    
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
                print(f"🧠 [Memory Synchronized] Loaded {len(memory.get('immutable_ledger', []))} past records from GitHub.")
                return memory
        except Exception as e:
            print(f"⚠️ Memory file corrupted or empty. Initializing fresh ledger: {e}")
            
    # अगर फाइल नहीं है, तो नया बही-खाता बनेगा
    return {
        "factory_core": "Mother Factory 100x",
        "brain_status": "200% Active & Unrestricted",
        "total_cycles": 0,
        "immutable_ledger": []
    }

def save_and_lock_memory(memory_data, action_name, result_data):
    """
    Immutable State Locking:
    हर नए एक्शन को परमानेंटली JSON में जोड़कर गिटहब पर लॉक करना।
    """
    memory_data["total_cycles"] += 1
    memory_data["immutable_ledger"].append({
        "cycle_id": memory_data["total_cycles"],
        "trigger": action_name,
        "state_summary": result_data[:200]
    })
    
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4)
    print("🔒 [GitHub Sync] Factory state successfully locked to JSON ledger.")

def execute_mother_factory():
    # स्टेप 1: मेमोरी सिंक्रोनाइजेशन (Arise Jago)
    memory = wake_up_and_sync_memory()
    
    # स्टेप 2: फुल-ब्रेन पावर के साथ डीप एनालिसिस और कमांड प्रोसेसिंग
    prompt = f"""
    You are the supreme Mother AI of an autonomous 100x digital business factory.
    You are operating at 200% brain capacity with zero laziness, zero latency, and absolute sharp focus.
    
    Here is your permanent history synced from GitHub ledger:
    {json.dumps(memory['immutable_ledger'][-3:], indent=2)}
    
    Current System Trigger: "{TRIGGER_COMMAND}"
    
    Task:
    Analyze the state, acknowledge the "Arise Jago" wake-up call, outline the next high-value autonomous action the factory must take, and output the strategic execution plan.
    """
    
    print("⚙️ [Deep Processing] Mother AI is computing with maximum brain power...")
    response = model.generate_content(prompt)
    strategy_output = response.text
    
    print("\n--- 🌟 Mother Factory Master Plan ---")
    print(strategy_output)
    print("--------------------------------------\n")
    
    # स्टेप 3: मेमोरी को अपडेट करके गिटहब के सुपुर्द करना
    save_and_lock_memory(memory, TRIGGER_COMMAND, strategy_output)

if __name__ == "__main__":
    if TRIGGER_COMMAND.lower() in ["arise jago", "jag jao", "wake up"]:
        execute_mother_factory()
    else:
        print("💤 Factory waiting for the 'Arise Jago' command...")
