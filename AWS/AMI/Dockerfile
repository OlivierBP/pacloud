# This Dockerfile create the container for worker for the project Pacloud

FROM gentoo/stage3-amd64

# Copy the scripts from the local machine
COPY scripts/ /pacloud/AMI/scripts/

# Set the make.conf
RUN chmod a+x /pacloud/AMI/scripts/setMakeConf.sh
RUN /pacloud/AMI/scripts/setMakeConf.sh

# Update all and install the software needed
RUN emerge-webrsync \
&& emerge \
app-misc/jq \
dev-python/pip

# Install aws cli with pip
RUN pip install awscli --user \
&& ln -s /root/.local/bin/aws /bin/aws 

# Configure awscli
RUN aws configure set region eu-west-1

# Run the job
ENTRYPOINT ["/pacloud/AMI/scripts/compilePackage.sh"]


# Build this container with
# cd /pacloud/AMI/
# docker build -f /pacloud/AMI/Dockerfile -t olivierbp/pacloud .
# docker images
# docker run --rm --cap-add=SYS_PTRACE olivierbp/pacloud:latest

# To commit and push
# docker login --username olivierbp
# docker commit -a "olivierbp" -m "message" containerId olivierbp/pacloud:tags
# docker push olivierbp/pacloud:tags

