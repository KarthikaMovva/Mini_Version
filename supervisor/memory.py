class Memory:


    def __init__(self):
        # This keeps short-term memory of the system
        self.timeline = []
        # Stores older events that have been removed from timeline
        # This acts as long-term summarized memory
        self.summary = []



    def add_event(self, event):

        """
        Adds a new event to memory.

        The event object is expected to have:
        - time  -> when the event happened
        - type  -> type/category of event
        """


        # Create a readable event record
        record = f"{event.time} - {event.type}"
        # Add the new event to recent memory
        self.timeline.append(record)
        # Keep only the latest 5 events in timeline
        # If more than 5 events exist, move older events to summary
        if len(self.timeline) > 5:
            # Remove the oldest event (first item)
            removed = self.timeline.pop(0)
            # Store removed event in long-term memory
            self.summary.append(
                removed
            )



    def compress(self):
        """
        Compress old memories when the summary becomes too large.

        This prevents unlimited memory growth.
        """
        # If there are more than 5 summarized events,
        # replace them with a compressed representation
        if len(self.summary) > 5:
            self.summary = [
                f"{len(self.summary)} older events compressed"
            ]



    def context(self):
        """
        Returns the current memory state.

        This context can be passed to an AI model
        or decision-making system.
        """
        return {
            # Contains compressed older events
            "summary": self.summary,
            # Contains the latest 5 events
            "recent_events": self.timeline
        }