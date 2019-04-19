#!/home/coopengo/.local/lib/python2.7
import config
import pprint
#import library to use Redmine API
from redminelib import Redmine

# function called when a pull request was validated (don't know if it is by someone or by Coog Drone)
def updateIssueOnRedMineFromGit(pullBody, pullURL):

    print("Tokenize the comment retrieve from git...")
    # Put the string in lowercase
    pullBody = pullBody.lower()
    
    # Create an array with each element of the pull body
    pullBodyArray = pullBody.split(" ")
    
    # If the pull body contains the word "fix"
    if "fix" in pullBodyArray:
        # We retrieve the fix number identified by '#'
        for issueIDtemp in pullBodyArray:
            if '#' in issueIDtemp:
                issueID = issueIDtemp.split('#')[1]

        print(issueID)
    
    # if the body of the pull do not contains the word 'fix', we do not update anything
    else:
        print("This pull is not for a fix")
        return "Ticket not updated (not a fix pull request)"


    print("Trying to connect to RedMine...")
    # Connect to redmine deposit of the project 
    ## If posible, use the bot's apikey to identify
    redmine = Redmine(config.REDMINE_URL, key=config.REDMINE_API_KEY)
    print("Connected ! ")
    print("Trying to read issue " +str(issueID) +"..." )

    # read the issue (if the issue exists)
    issue = redmine.issue.get(issueID)
    
    print(issue.__dict__)
    print(issue.status['id'])

    if issue.status['id'] == config.REJETE:
        print("This ticket was rejected, imposible to update it")
        return "Ticket deleted"

    # If the issue exists on RedMine, 
    print("Issue exists !\nUpdate ticket...")
    print("Current status : " + str(issue.status))


    # if it is a pull request 
    redmine.issue.update(issueID, notes=pullURL, status_id=config.EN_REVUE)
    issue = redmine.issue.get(issueID)
    print("New status : " + str(issue.status))

    print("Ticket updated")
    return "Ok"

