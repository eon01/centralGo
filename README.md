# CentralGo
CentralGo (CGo) is multithreaded ans user-friendly scheduler for running scripts and routine tasks.
*   CGo works like Linux Crontab

*   The definition of a job is quite easy, just add a similar line to jobs.conf :    

    define \"MyJob\" run \"echo 'I am the job number 0'\" every \"1 seconds\" notify \"me@email.com\";
     OR
    define \"MyJob\" run \"./run.sh\" every \"sunday at 23:55\" notify \"me@email.com\"

*   CGo runs as a daemon

            This could help you to : 

            > Run routine tasks like checking if a website is up or down every 5 minutes
            > Schedule tasks for with email notification
            > Keep logs on scheduled tasks
            > Replace your system crontab with a user-friendly definition language

            Version
               ----
                  1.0.1

                     Utilities
                        -----------

                           CentralGo uses a number of open source projects to work properly:

                              * [Python] - Its built-in packages
                              * [Schedule] - An in-process scheduler for periodic jobs
## License
GNU/GPL V2
Maintainer : amri.aymen@gmail.com / @eon01 (Twitter/Github)
