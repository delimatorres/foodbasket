### Lifesum Food Calculator API


This project was created to address the lifesum challenge. The task was basically to create an application that reads an API with almost 500 million entries and create a map/reduce to return the entries in a structured way. 

How it works?
----

I tried some multiprocessing approaches to complete this task, and to achieve the final result I used Python without frameworks and also chose some libraries to help on the development such as Requests, Six and Kombu.

This client contains a main process and other processes (workers). These other processes call the lifesum API, make the sum and then send it for the main process. After receiving the result, the main process makes the reduce. It is also possible to quit the application using a keyboard interrupt (ctrl + c) and finish all the work gracefully before leaving. I used the session feature from the Requests library to improve how the application makes the requests, reducing the network latency because it doesn’t require a new connection to be established upon each request.

What could I have done better? 
----

There are a few things that could have been improved:

* The main process could send some statistics while it was waiting for the workers.
* I should have written the test for the code and documented my process while I was working on the task. 


How to use
----


First of all install the dependencies:
----

    $ make install

After that to run it:
----

    $ make run

and after all CTRL+C to finish

