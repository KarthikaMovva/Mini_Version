import os
from dotenv import load_dotenv
import certifi
from google import genai

# Load environment variables from .env file
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()


class GeminiDecision:

    # Instead of simple rules, these situations will be sent to Gemini LLM
    IMPORTANT_EVENTS = [
        "payment_failed",
        "fraud_detected",
        "refund_requested"
    ]


    def __init__(self):
        # Retrieve Gemini API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")

        # Initialize Gemini client as None initially
        self.client = None

        # Create Gemini client only if API key exists
        if api_key:
            self.client = genai.Client(
                api_key=api_key
            )

    def decide(self, context):

        """
        Main decision-making function.

        It receives the current order context and decides
        which action should be performed.
        """
        # First check whether this situation needs LLM reasoning
        # If not, use simple predefined rules
        if not self.requires_llm(context):
            return self.rule_based_decision(context)
        # If Gemini client is available, use AI reasoning
        if self.client:
            prompt = f"""
You are an Order Supervisor AI.

Choose exactly one action from:

retry_payment
notify_customer
escalate_support
update_order_status

Current order situation:
{context}

Return only one action name.
"""
            try:
                # Send request to Gemini model
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                # Extract AI response
                return response.text.strip()
            except Exception as e:
                # If Gemini fails due to API issues
                print("Gemini unavailable, using fallback")
                print(e)
        # If Gemini is unavailable, use predefined rules
        return self.rule_based_decision(context)



    def requires_llm(self, context):
        """
        Checks whether the given situation requires
        AI-based reasoning.

        Returns:
        True  -> Use Gemini
        False -> Use rule-based logic
        """
        # Check if any important event exists in the order context
        for event in self.IMPORTANT_EVENTS:

            if event in context:
                return True


        # No critical events found
        return False



    def rule_based_decision(self, context):

        """
        Simple rule-based decision system.

        Used when:
        - Gemini is unavailable
        - Situation does not require AI reasoning
        """
        # Convert context to lowercase
        context = context.lower()
        # If payment failed, retry payment
        if "payment_failed" in context:
            return "retry_payment"
        # If customer sent a message, notify customer
        elif "customer_message" in context:
            return "notify_customer"
        # If order is delivered, update order status
        elif "delivered" in context:
            return "update_order_status"
        # Fraud cases require human support escalation
        elif "fraud_detected" in context:
            return "escalate_support"
        # Refund requests are escalated for review
        elif "refund_requested" in context:
            return "escalate_support"
        # Default action when no condition matches
        else:
            return "notify_customer"