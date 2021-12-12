git commit -am "deploy dev"
git push
ssh -i .\Downloads\myVMKey.pem azureuser@52.168.122.249
cd ~/REST_API_server_prod/scripts
sh build.sh