1. Create an account on [NGC](https://bc.ngc.nvidia.com/jobs) where you can access clusters and launch training jobs. 
2. Log into NGC account. Then click on **user** on top right corner, then **Setup**
   ![ngc-apikey-1.jpg]({{"/assets/images/ngc-apikey-1.jpg" | prepend: site.baseurl}})
2. Click on **Generate API Key**
   ![ngc-apikey-2.jpg]({{"/assets/images/ngc-apikey-2.jpg" | prepend: site.baseurl}})
3. Copy the API key. 
4. Install NGC CLI from [here](https://ngc.nvidia.com/setup/installers/cli)
3. Open a terminal from your local machine, run `ngc config set`
   4. `API key`: enter API key, 
   5. `CLI output`: accept default (ascii) by pressing `Enter`
   6. `org`: Choose from the list the NGC org that you have access to. 
   7. `team`: Choose from the NGC team you're assigned with
   8. `ace`: choose a ACE, otherwise press `Enter`