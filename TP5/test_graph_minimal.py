import uuid

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState
from TP5.agent.graph_minimal import build_graph

if __name__ == "__main__":
    emails = load_all_emails()
    e = emails[9]

    run_id = str(uuid.uuid4())
    state = AgentState(
        run_id=run_id,
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )

    print("=== RUN_ID ===")
    print(run_id)

    app = build_graph()
    out = app.invoke(state)

    print("=== DECISION ===")
    print(out["decision"].model_dump_json(indent=2))
    print("\n=== DRAFT_V1 ===")
    print(out["draft_v1"])   # TODO: afficher draft_v1
    print("\n=== DRAFT_V2 ===")
    print(out["draft_v2"])   # TODO: afficher draft_v2
    print("\n=== ACTIONS ===")
    print(out["actions"])   # TODO: afficher actions
    print("\n=== EVIDENCE (n) ===")
    print(len(out["evidence"]))
    print("\n=== EVIDENCE (first) ===")
    print(out["evidence"][0].model_dump() if out["evidence"] else {})
    print("\n=== FINAL ===")
    print("kind =", out["final_kind"])
    print(out["final_text"])
