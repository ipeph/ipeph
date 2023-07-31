#!/var/venv/bin/python3.8

#####################################################
##### AXA GO - Backup Script
##### Created By
##### Febry Citra Prawira Negara - April 2022
#####################################################

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
    ReadTimeout
)
import os
import shutil
from operator import itemgetter
import csv
import threading

def network_connection_ip(*input):
    return {
        "device_type": input[0],
        "ip": input[1],
        "username": input[2],
        "password": input[3],
        "secret": input[3],
        "fast_cli": input[4],
        "session_log": input[5],
    }

def write_file(hostname, output):
    file = open("/home/svc_netlog_id/code/output/{}".format(hostname),"w")
    file.writelines(output)
    file.close

def convert_input(output,key):
    total = len(output)
    for i in range(0,total):
        output[i][key] = int(output[i][key])
        # print(output[i][key])
    return (output)


def check_devices (inventory, devtype, username, password, session):
    inventory_file = open(inventory,"r")
    for line in inventory_file:
        hostname = line.strip()
        network_devices = network_connection_ip(
            devtype,
            hostname,
            username,
            password,
            True,
            session + line.strip()
        )
        print("Checking Devices .... " + hostname)
        try:
            with ConnectHandler(**network_devices) as net_connect:
                output = net_connect.send_command(
                    "show interfaces | i line|rate | ex fifo",
                    read_timeout=120,
                    use_textfsm=True
                )
                new_output = convert_input(output,"input_rate")
                new_output = sorted(output, key=itemgetter('input_rate'), reverse=True)

                message = ""
                total = len(new_output)
                # total_up = 0
                # print("Total Interface Is : ",str(len(output)))
                for i in range(0,9):
                    print("Interface Name : {} || Status : {} || Input Rate : {} || Output Rate : {} ".format(new_output[i]['interface'],new_output[i]['link_status'],int(new_output[i]['input_rate']),new_output[i]['output_rate']))
                    message +=  "Interface Name : {} || Status : {} || Input Rate : {} || Output Rate : {} \n".format(new_output[i]['interface'],new_output[i]['link_status'],int(new_output[i]['input_rate']),new_output[i]['output_rate'])
                #     if (output[i]['status'] == "up"):
                #         print(output[i])
                #         total_up += 1
                # print("Total Interface Up " + str(total_up))

                write_file(hostname,message)
                # print(output)
        except (NetmikoAuthenticationException, NetmikoTimeoutException, ReadTimeout) as error:
            print(str(error))
            # write_file(hostname,str(error))

def check_devices2(inventory, devtype, username, password, session):
    for line in inventory:
        hostname = line['hostname']
        network_devices = network_connection_ip(
            devtype,
            hostname,
            username,
            password,
            True,
            session + line['hostname']
        )
        print("Checking Devices .... " + hostname)
        try:
            with ConnectHandler(**network_devices) as net_connect:
                output = net_connect.send_command(
                    "show interfaces | i line|rate | ex fifo",
                    read_timeout=120,
                    use_textfsm=True
                )
                new_output = convert_input(output,"input_rate")
                new_output = sorted(output, key=itemgetter('input_rate'), reverse=True)

                message = ""
                total = len(new_output)
                # total_up = 0
                # print("Total Interface Is : ",str(len(output)))
                for i in range(0,9):
                    print("Interface Name : {} || Status : {} || Input Rate : {} || Output Rate : {} ".format(new_output[i]['interface'],new_output[i]['link_status'],int(new_output[i]['input_rate']),new_output[i]['output_rate']))
                    message =+  "Interface Name : {} || Status : {} || Input Rate : {} || Output Rate : {} ".format(new_output[i]['interface'],new_output[i]['link_status'],int(new_output[i]['input_rate']),new_output[i]['output_rate'])
                #     if (output[i]['status'] == "up"):
                #         print(output[i])
                #         total_up += 1
                # print("Total Interface Up " + str(total_up))

                write_file(hostname,message)
                # print(output)
        except (NetmikoAuthenticationException, NetmikoTimeoutException, ReadTimeout) as error:
            print(str(error))
            # write_file(hostname,str(error))

def main():
    print("##########")
    print("Checking Output Directory")
    print("##########")
    shutil.rmtree(
        "/home/svc_netlog_id/code/output",
        ignore_errors=True
    )
    os.makedirs(
        "/home/svc_netlog_id/code/output",
        mode = 0o755,
        exist_ok=True
        )
    print("##########")
    print("Start Checking Network Devices")
    print("##########")
    # check_devices("/home/svc_netlog_id/code/inventory", "cisco_ios", "SVC_NW_BCK_AUTO", "qqNfoM1chMxS8BE", "/home/svc_netlog_id/code/")
    device_list = []
    file = open("/home/svc_netlog_id/code/inventory.csv","r")
    readcsv = csv.DictReader(file)
    for row in readcsv:
        device_dict = {
            "ip": row['ipaddress'],
            "hostname" : row ['hostname']
        }
        device_list.append(device_dict)

    # print(device_list)
    # check_devices2(device_list, "cisco_ios", "SVC_NW_BCK_AUTO", "qqNfoM1chMxS8BE", "/home/svc_netlog_id/code/")

    process_checkdevices1 = threading.Thread(target=check_devices, args=("/home/svc_netlog_id/code/inventory", "cisco_ios", "SVC_NW_BCK_AUTO", "qqNfoM1chMxS8BE", "/home/svc_netlog_id/code/",))
    process_checkdevices1.start()

    process_checkdevices2 = threading.Thread(target=check_devices, args=("/home/svc_netlog_id/code/inventory2", "cisco_ios", "SVC_NW_BCK_AUTO", "qqNfoM1chMxS8BE", "/home/svc_netlog_id/code/",))
    process_checkdevices2.start()

    process_checkdevices1.join()
    process_checkdevices2.join()
    
    
if __name__ == "__main__":
    main()
