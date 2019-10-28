# Flow Char example

```sequence
Note left of Server: I am listening
Client->Server:Nice to meet you, I am "ZPZ"
Note right of Client: SYN
Server->Client: Nice to meet you too, "ZPZ", I am "LDH". 
Note left of Server: ACK,SYN
Client->Server: Nice to meet you too, "LDH"
Note right of Client: ACK
Client->Server: Shall we talk more detail
Server->Client: Sure, Please.
Client->Server: I have a story. blablabla
Server->Client: You are right
Client->Server: Blablabla
Server->Client: Uh-huh
Client->Server: Blablabla
Server->Client: I can agree any more
```