git commit -a -m "deploy dev"
git push
ssh -i ~/VMKey/myVMKey.pem azureuser@ss32vm.eastus.cloudapp.azure.com 'cd ~/REST_API_server_dev/scripts && sh build.sh'
