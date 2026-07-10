# Order Supervisor Agent


## Setup


Create conda environment:



conda create -n order-supervisor python=3.11



Activate:



conda activate order-supervisor



Install dependencies:



pip install google-genai python-dotenv certifi



Run:



python main.py




## Sample Output



EVENT:
order_created

WAKE:
STAY_ASLEEP

EVENT:
payment_failed

WAKE:
WAKE_NOW

ACTION:
retry_payment

EVENT:
customer_message

WAKE:
WAKE_NOW

ACTION:
notify_customer

EVENT:
delivered

WAKE:
WAKE_NOW

ACTION:
update_order_status

========== FINAL SUMMARY ==========

Activity Log:

retry_payment ORD100

notify_customer

update_order_status completed

Learnings:

Important failures wake supervisor immediately




# Temporal Production Mapping


| This Project | Temporal Concept |
|---|---|
| JSON events | Signal |
| scheduled_wakeup() | Timer |
| memory.context() | Query |
| Tools methods | Activity |
| Memory compression | Continue-As-New |



# Where Gemini LLM Helps


Rules work for simple cases.

Gemini improves:


- understanding customer messages
- selecting the best action
- handling multiple competing events



The exact prompt sent to Gemini:



Event:

{
"type":"customer_message",
"message":"My payment failed and I need help"
}

Memory:

{
"summary":[
"payment failure happened"
]
}

Available actions:

retry_payment

notify_customer

escalate_support

update_order_status

Choose one action.



Example Gemini response:



retry_payment




# Production Architecture



Temporal Workflow

    |
    |
 Signals
    |
    |

Order Events

    |
    |
  Timer
    |
    |

Scheduled Supervisor Wake

    |
    |
Activities
    |
    |

Payment API
Notification API

    |
    |

Continue-As-New

Memory Cleanup

https://docs.google.com/document/d/1XaZH3M7RjswKlLORNZagEnhXd98Tt2UGyIchuIoX3P8/edit?tab=t.0