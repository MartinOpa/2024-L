for ((i=0; i<50; i++)); do U="user$i"; useradd -m -s /bin/bash -p "password" $U ; passwd -d -e $U; done

groupadd tisk
mkdir /tisk
chown :tisk /tisk
chmod 770 /tisk
chmod g+s /tisk
