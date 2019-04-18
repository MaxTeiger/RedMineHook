#!/home/coopengo/.local/lib/python2.7
import config
#import library to use Redmine API
from redminelib import Redmine

# function called when a pull request was validated (don't know if it is by someone or by Coog Drone)
def updateIssueOnRedMineFromGit(pullBody, pullURL):

    print("Tokenize the comment retieve from git...")
    issueID = int(pullBody.split('#')[1])
    print("Issue ID : " +str(issueID))

    print("Trying to connect to RedMine...")
    # Connect to redmine deposit of the project 
    ## If posible, use the bot's apikey to identify
    redmine = Redmine(config.REDMINE_URL, key=config.REDMINE_API_KEY)
    print("Connected ! ")
    print("Trying to read issue " +str(issueID) +"..." )

    # read the issue (if the issue exists)
    issue = redmine.issue.get(issueID)
     
    # If the issue exists on RedMine, 
    print("Issue exists !\nUpdate ticket...")
    print("Current status : " + str(issue.status))
    print("Current done ratio : " + str(issue.done_ratio))


    # if it is a pull request 
    redmine.issue.update(issueID, done_ratio=99, notes=pullURL, status_id=7)

    print("New status : " + str(issue.status))
    print("New done ratio : " + str(issue.done_ratio))

    print("Ticket updated")
    return "Ok"