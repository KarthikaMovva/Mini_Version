# contextlib is used to manage contexts.
# Here it is used to temporarily suppress error output from Gemini calls.
import contextlib
# Import Memory class to store recent and historical events
from .memory import Memory
# Import Tools class which contains actions the supervisor can execute
from .tools import Tools
# Import wake policy to decide whether an event needs immediate attention
from .policy import wake_policy
# Import Gemini AI decision-maker
from .llm import GeminiDecision




class Supervisor:


    def __init__(self):
        # Initialize memory storage for tracking events
        self.memory = Memory()
        # Initialize available business actions/tools
        self.tools = Tools()
        # Initialize Gemini AI decision engine
        self.llm = GeminiDecision()
        # Controls whether the supervisor agent is active
        self.running = True




    def scheduled_wakeup(self):
        """
        Represents a scheduled wake-up event.

        This can be triggered periodically by a scheduler
        to allow the supervisor to check system state.
        """
        print(
            "\n[TIMER] Scheduled supervisor wake"
        )




    def decide_action(self, event):
        """
        Determines what action should be taken for an event.

        Decision flow:
        1. Send event + memory context to Gemini AI
        2. If Gemini fails, use rule-based fallback
        """
        # Create context containing:
        # - Current event details
        # - Previous memory/history
        context = {
            "event": event.__dict__,
            "memory": self.memory.context()
        }
        # Prevents unnecessary error logs from appearing
        with contextlib.redirect_stderr(lambda x: None):
            try:
                # Ask Gemini to decide the best action
                llm_result = self.llm.decide(
                    context
                )
            # If Gemini fails due to API issues
            # continue with fallback logic
            except Exception:
                llm_result = None
        # If Gemini returned a valid decision,
        # use the AI-generated action
        if llm_result:
            return llm_result



        # Used when AI is unavailable


        # Payment failures require retrying payment
        if event.type == "payment_failed":
            return "retry_payment"
        # Customer messages require a response
        if event.type == "customer_message":
            return "notify_customer"
        # Delivered orders need status updates
        if event.type == "delivered":
            return "update_order_status"
        # Default action for unknown situations
        return "escalate_support"







    def execute(self, event):
        """
        Executes the selected action.

        The action decided by AI/rules is mapped
        to the appropriate business tool.
        """
        # Decide what needs to be done
        action = self.decide_action(event)
        print(
            "ACTION:",
            action
        )
        # Execute payment retry action
        if action == "retry_payment":
            self.tools.retry_payment(
                event.order
            )
        # Send notification to customer
        elif action == "notify_customer":
            self.tools.notify_customer(
                "We are checking your order"
            )
        # Update order status after delivery
        elif action == "update_order_status":
            self.tools.update_order_status(
                event.order,
                "completed"
            )
        # Any other action is treated as escalation
        else:
            self.tools.escalate_support(
                event.order
            )







    def process(self, event):

        """
        Main event processing pipeline.

        Steps:
        1. Check whether event should wake the supervisor
        2. Store event in memory
        3. Execute action if required
        4. Compress old memories
        5. Stop supervisor for completed workflows
        """
        # Check wake policy for this event
        wake, reason = wake_policy(event)
        print(
            "\nEVENT:",
            event.type
        )
        print(
            "WAKE:",
            "WAKE_NOW" if wake else "STAY_ASLEEP",
            reason
        )



        # Store every event in memory,
        # even if no action is required
        self.memory.add_event(event)
        # Only execute actions for important events
        if wake:
            self.execute(event)
        # Compress old memories to avoid unlimited growth
        self.memory.compress()
        # Stop the supervisor when the workflow reaches
        # a final state
        if event.type in [
            "delivered",        # Order completed
            "refund_resolved",  # Refund process finished
            "manual_stop"       # Human requested shutdown
        ]:
            self.running = False