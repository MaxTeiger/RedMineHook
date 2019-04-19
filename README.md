# RedMine syncronization with GitHub 

## Setup

### On your server 

Go to your server (we assume it has a public ip address). 
*If you want to perform debug/development tests, I advise you to use ngrok*

```bash
$ git clone https://github.com/MaxTeiger/RedMineHook.git
```
Once it's done, you must have a new folder called **RedMineHook**

### On GitHub

* Go to your **GitHub** repository
* Go to settings > Webhooks section
* Create new webhook
* Add the address of the server on which the application will run with "/payload" at the end
> It should look like https://myserveraddress/payload

* Add a **secret key** for the security of the application (upper case, lower case, numbers...). Please note this key, we will use it later
* Select Let me select individual events > Choose the activation mode on "Pull request".
* Save the webhook

### In conf.txt file

* Change GitHub > secret to your **secret key**
* Change RedMine > apikey to your **redmine api key**
* Change RedMine > url to your **RedMine desposit URL**

### On your server
Once everything is done, go to your **RedMineHook** hook folder and you just have to run :

```bash
$ docker-compose up
```
or 
```bash
$ docker-compose up -d
```

For the moment, it performs the same action regardless of the action performed on a pull request (whether it is opened, merged, re-opened, or edited).
Maybe a next version that will change the RedMine status to :

| GitHub                        | RedMine                     |
|-------------------------------|-----------------------------|
| New Pull Request              | En revue                    |
| Pull request closed           | A traiter                   |
| Merge pull request            | Traité                      |

#### Notes :

This application use port 5000 on your host machine, if you want to change this configuration, go to *docker-compose.yml* ang change **5000**:5000 to change the port used by the Docker host.

Pull body must have the form : 
> What you want ... Fix [...] #fixnumber [...]

If the word "Fix" isn't in the body message, the app will return a HTTP response 400
Ticket is not updated if it is "rejected" (Rejeté), app will return HTTP response 404
If the secret is not the good one (specified in conf.txt), app will return HTTP response 403

If path problems to conf.txt occurs in the container, contact me. 

----

