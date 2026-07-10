# Import json module to read and parse JSON files
import json
# Import time module to work with timers and scheduled wake-ups
import time
# Import Event data model used to represent system events
from supervisor.models import Event
# Import Supervisor agent that manages decision-making and actions
from supervisor.supervisor import Supervisor




def load_events():
    """
    Loads events from events.json file
    and converts each JSON object into an Event object.
    """
    # Open the JSON file containing order events
    with open(
        "events.json"
    ) as file:
        # Convert JSON data into Python objects
        data = json.load(file)
    # Convert every dictionary from JSON into an Event object
    return [
        Event(**item)
        for item in data
    ]





def main():
    """
    Main execution function.

    Workflow:
    1. Create Supervisor agent
    2. Load events
    3. Process events one by one
    4. Display final memory and activity results
    """
    # Create the AI supervisor instance
    # This initializes:
    # - Memory
    # - Tools
    # - Gemini decision engine
    supervisor = Supervisor()
    # Load all events from JSON file
    events = load_events()
    # Store the timestamp of the last scheduled wake-up
    # Used to trigger periodic supervisor checks
    last_wake = time.time()
    # Process each event sequentially
    for event in events:
        # Check if 10 seconds have passed since last timer wake-up
        # This allows the supervisor to wake periodically
        # even when there are no new events
        if time.time() - last_wake >= 10:
            # Trigger scheduled supervisor check
            supervisor.scheduled_wakeup()
            # Reset timer after wake-up
            last_wake = time.time()
        # Send current event to supervisor for processing
        # Supervisor will:
        # - Apply wake policy
        # - Store memory
        # - Decide action
        # - Execute tools if required
        supervisor.process(event)
        # Stop processing if supervisor reaches
        if not supervisor.running:
            break
    print(
        "\n========== FINAL SUMMARY =========="
    )
    # Display current memory state
    print(
        "\nMemory:"
    )
    print(
        supervisor.memory.context()
    )
    # Display all actions performed by tools
    print(
        "\nActivity Log:"
    )
    for activity in supervisor.tools.activity_log:
        print(activity)
    # Display important system learnings
    print(
        "\nLearnings:"
    )
    print(
        "- Important failures wake supervisor immediately"
    )
    print(
        "- Timer allows periodic checking without events"
    )
    print(
        "- Memory does not grow forever"
    )


# This ensures main() runs only when this file
# is executed directly.
if __name__ == "__main__":

    main()