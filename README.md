## Data Analysis

run `uv sync` to load in Python etc.

run `.\.venv\Scripts\activate` to activate virtual environment

NB - Claude can do this so if this is not done it may not matter. Just ask 'set UV environment and sync'

The _ideas folder is just where you write a little brain dump of what you just want to do, any of your thoughts. It's just used to help; it doesn't have to be specific or well structured. 

The _plans folder is where, when we run our command for planning, the report will be placed. That will explain:
- what it thinks the data set is about
- the questions it wants to ask
- what it will plan to do
- what AI/ML analysis it will do

Then, in the _specs, when we run the SPEC command, it will form the actual technical requirements, the code implications, what data cleaning would do, all the very specifics. Later, when we run the SPEC command, the EXECUTE command, it will actually build the code based on that specification. 

All datasets are stored in the data folder, and you can use the @ symbol to reference them. 

And the output of running the code will be stored in the output folder, and the code formed by the specifications and the execute stage will be stored in the SRC folder. 

If we look in the.claude folder, we see there's a folder for agents which run in their own context and unit. 

We have a folder for commands. This is used where we do /login, etc. We can make our custom commands based on the file name. We'll have a file name, should we say, called execute.md. If we do /execute and pass in an argument, it will run that particular command for us, which we've described in that file. 

The skills folder is similar to commands, but it is actually determined by the CLAUDE code itself, whereas the commands are very specific when instructing it. Skills contains a lot of different files with different sets of skills and capabilities that are like tools that CLAUDE can then draw upon as needed. 

The repo is set up with uv, which is the modern standard now, rather than pip install. It has all the files loaded when you first go in. You may run the commands specified in the README.md to activate the environment, but if not, CLAUDE actually understands all of this. It's got it in its CLAUDE.md file, which is basically setting up the information for it so it knows what this project's about, and it updates itself so that it can better perform.

You won't really need to do anything; you just give it commands and it will then have all the Python it needs within it and will add libraries as needed, because effectively it can write Python code and execute Python code through its agents. If it doesn't have anything, it just installs and sets it up. It can, in fact, even install uv and all of that for us, but it's already in this template. 

Commands you may need are:
- /login to login
- /init to initialise a repo or update CLAUDE.md

The most important is once you're logged in, if you're unsure about anything, you can ask Claude to do it or what to do. 

Remember that you can take screenshots and add them in. You can copy and paste them into the terminal, or if you've got them saved as a file in the folder using the Act reference, you can reference them. Then it can see exactly what's going on, so you can ask it questions on that if there's something that you're finding hard to explain. 