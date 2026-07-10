class Tools:


    def __init__(self):
        # Stores a history of all actions performed by the system.
        # Each action is saved as a dictionary containing details
        # about what operation was executed.
        self.activity_log = []

    def notify_customer(self, message):
        """
        Sends a notification message to the customer.
        Parameters:
            message -> Text that should be sent to the customer
        """

        # Record the customer notification activity
        # Instead of actually sending a message,
        # this stores the action for tracking/auditing.
        self.activity_log.append({
            "activity": "notify_customer",
            "details": message
        })




    def retry_payment(self, order):
        """
        Attempts to retry payment for an order.
        Parameters:
            order -> Order ID for which payment should be retried
        """
        # Store payment retry action in activity history
        self.activity_log.append({
            "activity": "retry_payment",
            "order": order
        })




    def escalate_support(self, order):
        """
        Escalates an order issue to the support team.

        Parameters:
            order -> Order ID that requires human attention
        """
        # Log escalation request
        self.activity_log.append({
            "activity": "escalate_support",
            "order": order
        })




    def update_order_status(self, order, status):
        """
        Updates the status of an order.
        Parameters:
            order  -> Order ID whose status needs updating
            status -> New status value
                     Example: "completed"
        """
        # Store order status update activity
        self.activity_log.append({
            "activity": "update_order_status",
            "order": order,
            "status": status
        })