git commit -a -m "deploy dev"
git push origin
ssh -i ~/VMKey/myVMKey.pem azureuser@ss32vm.eastus.cloudapp.azure.com 'cd ~/REST_API_server_prod/scripts && sh build.sh'