# Set of events that require immediate attention from the system.
IMPORTANT_EVENTS = {
    "payment_failed",
    "customer_message",
    "refund_requested",
    "refund_resolved",
    "delivered",
    "manual_stop"         
}



def wake_policy(event):
    """
    Determines whether an incoming event should activate
    the decision-making system.

    Parameters:
        event -> Event object containing details like:
                 event.type, event.id, event.time, etc.

    Returns:
        Tuple containing:
        - Boolean value indicating whether action is required
        - Reason explaining the decision
    """
    # Check whether the event type exists in the IMPORTANT_EVENTS set
    if event.type in IMPORTANT_EVENTS:
        # Return True because this is a business-critical event
        return True, "Important business event"
    # If the event is not important
    return False, "No immediate action required"