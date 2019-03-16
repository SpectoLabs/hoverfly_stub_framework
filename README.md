# Hoverfly Stub Framework

The idea is to provide easy to implement functions, which can be utilised to update Hoverfly Stub Config Json.
The framework is to remove the manual intervention to edit Hoverfly Stub Config (e.g simulation.json).


### Prerequisites


```
Python  >= 2.7
```

### Deploying

```
1. Copy the package to the desired location.
2. Run setup.py - it will download the project dependencies
```

### Framework Structure

```
1. backups              - Contains backup of Postman Collection and Test Run jsons. Besides, recorded Stub Simulation is
                          also kept here for any future reference.
2. data                 - Contains API Collection and Latency CSV. Also repo for default and updated response body.
3. hoverfly_stub        - Contains the updated Hoverfly Stub Config and shell scripts.
4. stub_config_updation - Contains main.py which will edit the stub config.
5. stub_middleware      - Contains the middlewares, which can be used while deploying Hoverfly Webserver
6. global_variables.py  - Contains the variables, which have been used throughoput the framework
7. Jenkinsfile          - Jenkins Pipeline to start/stop/restart webserver.
8. requirements.txt     - Contains the requirements for the framework.
9. setup.py             - Script to resolve dependencied on the new enviornment.
```

### First-Timers

```
If you have absolutely no idea from where to start, you can start with this:

1. Record all your APIs in a Postman Collection.
2. Run hoverfly_stub -> create_stub_config.sh <POSTMAN_Collection.json> <POSTMAN_Env File (optional)>
3. Copy the created file (eg: hoverfly_config_2019_03_15_110823.json) to backups folder.
4. Copy the contents of the above file to hovefly_stub -> stub_final_config.json.
5. Update stub_config_updation -> stub_helpers.py as per your requirements.
6. Update stub_config_updation -> main.py to call functions created in stub_helpers.py
7. Run main.py - stub_final_config.json should get updated accordingly.
8. Update data -> API_Collection_and_Latency.csv with Latency Values.
9. Run main.py again to copy the data -> API_Collection_and_Latency.csv to hoverfly_stub to ensure there's consistency.
10. To Start the server - cd hoverfly_stub; ./start_stub_server.sh
11. To Stop the server - cd hoverfly_stub; ./stop_stub_server.sh

This is a very basic level to start up things.
Please feel free to explore the project to gain more understanding.
```

### Using Framework

```
1. Open global_variables.py and check if all the values are as per current env.
2. Check stub_config_updation -> main.py if it has the required functions which would edit the config as per the
   requirement.
   
NOTE: While adding new APIs to existing postman collection (backups -> CBus Stub - LINK APIs.postman_collection), please
      add the new API always at the end of the collection, else it will stuff up the ordering of APIs which will
      inturn stuff up function, which is editing the APIs with response data.
```

## Authors

* **Navdit Sharma** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

