#!/bin/bash
#
#multipass shell ubuntu-api-server 'sudo rm -rf /home/ubuntu/bookstore'
#multipass shell ubuntu-api-server 'mkdir bookstore'
#multipass transfer -r ../bookstoreAPI ubuntu-api-server:/home/ubuntu/bookstore
#
#multipass shell ubuntu-api-server 'sudo docker stop bookstore-api'
#multipass shell ubuntu-api-server 'sudo docker rm -f bookstore-api'
#
#multipass shell ubuntu-api-server 'sudo docker build -t bookstore-build . ~/bookstore/bookstoreAPI'
#multipass shell ubuntu-api-server 'sudo docker run -idt -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 --name=bookstore-api bookstore-build ~/bookstore/bookstoreAPI'

# 1. Clean up old folder on the VM
multipass shell ubuntu-api-server 'sudo rm -rf /home/ubuntu/bookstore && mkdir -p /home/ubuntu/bookstore'

# 2. Transfer files (Using "." means "this folder").
# We use quotes to handle the space in your "api app" folder name.
multipass transfer -r . ubuntu-api-server:/home/ubuntu/bookstore/

# 3. Stop and remove old container (Ignore errors if it doesn't exist)
multipass shell ubuntu-api-server 'sudo docker stop bookstore-api || true'
multipass shell ubuntu-api-server 'sudo docker rm -f bookstore-api || true'

# 4. Build the image
# FIXED: Removed the extra "." that caused "Too many arguments"
multipass shell ubuntu-api-server 'sudo docker build -t bookstore-build /home/ubuntu/bookstore'

# 5. Run the container
multipass shell ubuntu-api-server 'sudo docker run -idt -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 --name=bookstore-api bookstore-build'

echo "DONE! Deployment finished."