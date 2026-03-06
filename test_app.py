import json
from app.main import triage_ticket, TicketRequest
import traceback

def test():
    try:
        ticket1 = TicketRequest(
            subject="I need a refund for my last order",
            description="The item arrived broken and I want my money back ASAP!",
            channel="email",
            customer_id="12345"
        )
        result1 = triage_ticket(ticket1)

        ticket2 = TicketRequest(
            subject="Cannot login to my account",
            description="I forgot my password and the reset link is not working.",
            channel="chat",
            customer_id="98765"
        )
        result2 = triage_ticket(ticket2)

        with open("results.json", "w") as f:
            json.dump({"ticket1": result1, "ticket2": result2}, f, indent=2)

    except Exception as e:
        with open("error.log", "w") as f:
            f.write(str(e))
            f.write(traceback.format_exc())

if __name__ == "__main__":
    test()
