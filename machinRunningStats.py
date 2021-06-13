import psutil
import platform,sys
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

f = open('output.txt','w')


print("="*40, "System Information", "="*40, file=f)
uname = platform.uname()
print(f"System: {uname.system}", file=f)
print(f"Node Name: {uname.node}", file=f)
print(f"Release: {uname.release}", file=f)
print(f"Version: {uname.version}", file=f)
print(f"Machine: {uname.machine}", file=f)
print(f"Processor: {uname.processor}", file=f)

# Boot Time
print("="*40, "Boot Time", "="*40, file=f)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}", file=f)

# let's print CPU information
print("="*40, "CPU Info", "="*40, file=f)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False), file=f)
print("Total cores:", psutil.cpu_count(logical=True), file=f)
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz", file=f)
print(f"Min Frequency: {cpufreq.min:.2f}Mhz", file=f)
print(f"Current Frequency: {cpufreq.current:.2f}Mhz", file=f)
# CPU usage
print("CPU Usage Per Core:", file=f)
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%", file=f)
print(f"Total CPU Usage: {psutil.cpu_percent()}%", file=f)

# Memory Information
print("="*40, "Memory Information", "="*40, file=f)
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}", file=f)
print(f"Available: {get_size(svmem.available)}", file=f)
print(f"Used: {get_size(svmem.used)}", file=f)
print(f"Percentage: {svmem.percent}%", file=f)
print("="*20, "SWAP", "="*20, file=f)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}", file=f)
print(f"Free: {get_size(swap.free)}", file=f)
print(f"Used: {get_size(swap.used)}", file=f)
print(f"Percentage: {swap.percent}%", file=f)


# Disk Information
print("="*40, "Disk Information", "="*40, file=f)
print("Partitions and Usage:", file=f)
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===", file=f)
    print(f"  Mountpoint: {partition.mountpoint}", file=f)
    print(f"  File system type: {partition.fstype}", file=f)
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}", file=f)
    print(f"  Used: {get_size(partition_usage.used)}", file=f)
    print(f"  Free: {get_size(partition_usage.free)}", file=f)
    print(f"  Percentage: {partition_usage.percent}%", file=f)
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}", file=f)
print(f"Total write: {get_size(disk_io.write_bytes)}", file=f)

# Network information
print("="*40, "Network Information", "="*40, file=f)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===", file=f)
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}", file=f)
            print(f"  Netmask: {address.netmask}", file=f)
            print(f"  Broadcast IP: {address.broadcast}", file=f)
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}", file=f)
            print(f"  Netmask: {address.netmask}", file=f)
            print(f"  Broadcast MAC: {address.broadcast}", file=f)
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}", file=f)
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}", file=f)

#f.close()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail_content = '''Hello,
This is a test mail.
In this mail we are sending some attachments.
The mail is sent using Python SMTP library.
Thank You
'''
#The mail addresses and password
sender_address = 'ankitalex@gmail.com'
sender_pass = 'Alexagra!12'
receiver_address = 'ankitalex@gmail.com'
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'
#The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
attach_file_name = r'C:\Users\user\PycharmProjects\pythonProject\machinStats\output.txt'
attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
payload = MIMEBase('application', 'octate-stream')
payload.set_payload((attach_file).read())
encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
message.attach(payload)
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')