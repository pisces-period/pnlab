### Docker Role (Exercise I)

The objective of this exercise is to deploy a python app inside a docker container that forwards logs to the syslog server. This configuration is to be deployed by Ansible. The app takes parameters from CLI in the form of environment variables.

You can read the [_README.md_](pisces-period/pnlab/master/getweather/README.md) file for specifics on how the app works.

To accomplish this task, I'm dedicating a role for this configuration, along with 4 tasks and a notify-hook to restart services, when appropriate. __*Please notice that I'm NOT creating nor adding a Docker group to sudo list. Make sure you use sudo -i command before running containers*__.

1. The first task installs Docker.io and dependencies.

2. The second task enables the Docker service startup on boot.

3. The third task configures the Docker logging driver.

4. The fourth task uses the _docker_image_ module to build an image based on the Dockerfile. By default, this image is named _getweather:v1.0_. You'll need to use this name when you run your container.

The Dockerfile describes the necessary actions to install the dependencies and copy the /getweather directory into the container and run the app (notice that the app does not run as root, but as a random user ID 5000).

###### For further information regarding security of docker, please check these out:
https://docs.docker.com/engine/security/security/

#### Testing Exercise I

SSH into pan-peter and run the following command, replacing the ${API_KEY} and ${CITY} variables with a valid API key and a city whose weather you would like to inspect:
``` 
vagrant ssh pan-peter
sudo -i
docker run --rm -e OPENWEATHER_API_KEY=="${API_KEY}" -e CITY_NAME="${CITY}" getweather:v1.0
```

Verify the output with the following command:
` cat /var/log/syslog | grep "openweather" `

You should see something like:
```
Oct 13 16:42:16 localhost 50d091e7a6b4[6808]: source:openweathermap,location:New York,description:clear sky,temp:16.58,humidity:45
```
