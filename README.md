### Assignment: Implement a REST API web application for option pricing and market data storage
(recommended timing: 2-3 hours)

Features:
1. Upload market data required for option pricing
2. Retrieve previously uploaded market data
3. Calculate PV of options with Black76 formula using previously uploaded market data

Examples of options:
BRN Jan24 Call Strike 100 USD/BBL
HH Mar24 Put Strike 10 USD/MMBTu

A note on the contract notation. A BRN Jan-24 option is a European option with underlying ICE Brent
Jan-24 Future. BRN option expiry will be the last business day of the 2 nd month before the delivery month.
For example, BRN Jan-24 expiry date is 2023-11-30.
HH Mar24 option is a European option with underlying Henry Hub Gas March 24 Future contract. HH
option expiry is the last business day of the month before the delivery month. For example, HH Mar-24
expiry date is 2022-02-29.
You have a freedom to choose technology stack, architecture, input/output schemas to best fit the
requirements.

The code and design should meet these requirements, but be sufficiently flexible to allow future changes.
The code should be well structured, commented, have error handling and be tested.

* Produce working, object-oriented source code.
* Provide as a GitHub project or send back in electronic format.
* We will walk through your code together in the next session, answering questions on the code
and programming/design choices you made.
* At the interview you will be asked to present an end-to-end demo of the application.
