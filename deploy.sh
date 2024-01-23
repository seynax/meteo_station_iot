git add .
git commit
git push origin api/develop
sshpass -p 'mt_pi_1234' ssh mt_api@192.168.158.254 "cd /home/mt_pi/server/api/ && git pull origin api/develop"

