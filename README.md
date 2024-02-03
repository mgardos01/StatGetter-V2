# StatGetter V2
Discord Bot that fetches and caches e-sport statistics on demand.

## .env file 
Contains 
```
MY_ORACLE_PASSWORD={YOUR PASS HERE}
MY_ORACLE_HOSTNAME={YOUR HOSTNAME HERE}
```

## Setup Process Tutorial/TODO List: 
```
> docker login container-registry.oracle.com
# You'll be prompted for your username + password. 
# you should see "Login Succeeded"

# This will pull the EX Database + ORDS images from Oracle, the initial install may take a few minutes.  

> docker compose up. 

# This will install APEX and the EX Database on your system, which may also take a few minutes.  

# Defaults:
#   - Workspace: Internal
#   - Username: Admin
#   - Password: Welcome_1
# TODO: CHANGE ENV VARIABLES SO THESE ARE REAL

```