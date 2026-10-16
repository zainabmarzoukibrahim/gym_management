R1. ERPNext Subscription vs. Custom Logic
Decision: I chose custom membership management logic using the Gym Membership DocType and ERPNext's Sales Invoice  instead of using ERPNext Subscription.
   Reason: Gym memberships should not renew automatically. A new membership is created during renewal to preserve membership history and allow renewal to be handled explicitly.


R2 How did you model trainers: custom fields on Employee, a
separate Gym Trainer, or something else? Why?

I created a separate custom DocType called "Gym Trainer" and added a Link field to the standard "Employee" DocType.
I chose this design because trainers have gym-specific information, such as specialties, that should be managed separately from general employee data. Linking to "Employee" allows us to reuse the existing employee record without duplicating employee information, while keeping the trainer-specific logic independent.






R3. Pro-rated Refunds for Midway Cancellation
    Design: Since the system records attendance and the original amount paid is available from the Sales Invoice, I would calculate the refund based on the membership's daily cost.
    First, divide the original amount paid by the total number of days in the membership plan to determine the cost per day. Then, calculate the cost of the used period and subtract it from the amount paid. The remaining amount is refunded to the member.
    During my research, I found that ERPNext supports Credit Notes, which can record a full or partial reduction of an original Sales Invoice and can be used as part of the refund process. I would use this built-in functionality for the accounting part, while implementing custom logic to calculate the refundable amount based on the membership period. The refund would then be processed through ERPNext's accounting workflow, subject to the gym's refund policy.


R4. Safe Class Booking Under Concurrent Requests
Design: To prevent two members from booking the last available spot at the same time, I would use database transactions and row-level locking.
Frappe supports database transactions, and its database API provides a for_update option for locking records during updates.


R5. References and Resources

Frappe Framework Documentation: Used the documentation provided for the assessment to understand DocTypes, controllers, document events, database operations, and framework features.

Frappe Forum:Consulted a community discussion 

JavaScript Guide and Reference: 
Used to remember some JavaScript syntax 

ChatGPT and Claude: Used as supplementary learning and clarification tools to understand technical concepts, explore implementation approaches, and troubleshoot code.

Search about services and buildin features that introduced by frappe framework.
