# txttransmitter
Network Project


High-level Architecture:
From a high-level perspective, our program works using three applications each running on a separate host: Server, Controller, and Renderer. The Controller application serves as the point of contact for the end user, and communicates the users commands to both the Server and the Renderer (whichever is relevant for the command). The Server hosts and provides access to the files to be rendered, communicating file info to the controller and file data to the renderer. The renderer receives commands from the controller and communicates between the server for streaming. The applications should be started in the order of Server, Renderer, and Controller due to the order of connections.

Controller Architecture:
The controller begins by requesting a list of files from the server, and then presenting it to the user. It accepts input from the user about which file to render. Once the file has been chosen, the user may start inputting the commands: “Start”, “Pause”, “Resume”, & “Restart”. “Start” will begin streaming the file. “Pause” will pause the streaming of the file, while “Resume” will resume the streaming of the file after pausing. “Restart” will restart the streaming of the file from the beginning of the file.

Renderer Architecture:
The renderer initially waits for the start command from the controller. Upon receiving this, the renderer begins communication with the server by sending a chunk request for the first chunk (100 bytes) of the file. When it receives the response from the server, it “renders” the text and sends it to the controller to present to the user. The renderer then checks for any requests from the controller. After checking for requests, the renderer will send another chunk request to the server to continue rendering the file on the next chunk. To keep track of pause status and its place in the file, the renderer store the current chunkID that it has rendered as well as a boolean pause value, which is set to either 0 or 1 to represent whether rendering is paused; the variable’s checked when deciding to send a chunk request or not.

Server Architecture:
The server functions from start to end waiting for requests from the other modules. If a file request is received from the controller, the server replies with the list to the controller. If a chunk request is sent to the server from the renderer, the server will retrieve the specified chunk from the file and send it back to the renderer for processing.

