# P2P Terminal Chat in Python

Simple P2P (peer-to-peer) chat for the terminal, made in Python.

I put this together mostly to practice and get a good handle on how low-level sockets work, without a server in the middle. The idea was for two people to connect directly to send messages and files. 
I know it could use some colour, but again, this is just a learning project.

I also added a file transfer feature, originally you just sended raw text but bc of this feature i needed a way to know if im sending a file or just a message, so i just used json to format messages and get to specify a type,
which also allowed me to use usernames for each user.

Also, the credit for the `get_download_path` function goes to [this Stack Overflow answer](https://stackoverflow.com/a/48706260).

## How to Use.

1.  Clone the repo.
2.  Run the script in your terminal: `python main.py` (or whatever you named the file).
3.  Select a username, it can be whatever.
4.  One person needs to choose the "Host" option. The script will provide an IP address and a port.
5.  The other person chooses "Connect" and enters the details provided by the host.


## Commands
* Just type and send to chat normally
* `/filesend <full_path_to_file>`: To start sending a file.
* `exit`: Closes the connection.

---

**Disclaimer:** this is a learning project. It has no encryption whatsoever, so it's not secure at all.
