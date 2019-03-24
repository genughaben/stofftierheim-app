build:
	docker build -t frank/stofftier:latest .

run:
	docker run -it --rm -d \
                -e NEXTCLOUD_USER=${NEXTCLOUD_USER} \
                -e NEXTCLOUD_PASSWORD=${NEXTCLOUD_PASSWORD} \
		-e NEXTCLOUD_PATH_STOFF=${NEXTCLOUD_PATH_STOFF} \
                -e STOFFTIERHEIM_LOGIN=${STOFFTIERHEIM_LOGIN} \
                -e STOFFTIERHEIM_PASSWORD=${STOFFTIERHEIM_PASSWORD} \
		-v ${shell pwd}:/workdir \
		-p 5000:8000 \
		--name stofftier \
		frank/stofftier:latest

