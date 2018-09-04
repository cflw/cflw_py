import cflw网络设备_思科 as 思科
def f版本():
	v字符串0 = """
Cisco IOS Software, C3560 Software (C3560-IPSERVICESK9-M), Version 15.0(1)SE2, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Thu 22-Dec-11 00:24 by prod_rel_team

ROM: Bootstrap program is C3560 boot loader
BOOTLDR: C3560 Boot Loader (C3560-HBOOT-M) Version 12.2(50r)SE, RELEASE SOFTWARE (fc1)

Xsdl-FLWW3560-L3 uptime is 33 weeks, 5 days, 18 minutes
System returned to ROM by power-on
System restarted at 14:22:27 beijing Sun Aug 21 2016
System image file is "flash:/c3560-ipservicesk9-mz.150-1.SE2.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco WS-C3560V2-24TS (PowerPC405) processor (revision N0) with 131072K bytes of memory.
Processor board ID FDO1602X266
Last reset from power-on
3 Virtual Ethernet interfaces
24 FastEthernet interfaces
2 Gigabit Ethernet interfaces
The password-recovery mechanism is enabled.

512K bytes of flash-simulated non-volatile configuration memory.
Base ethernet MAC Address       : A4:56:30:6C:FF:80
Motherboard assembly number     : 73-11765-08
Power supply part number        : 341-0328-02
Motherboard serial number       : FDO1602117S
Power supply serial number      : LIT15500QTT
Model revision number           : N0
Motherboard revision number     : B0
Model number                    : WS-C3560V2-24TS-S
System serial number            : FDO1602X266
Top Assembly Part Number        : 800-31050-05
Top Assembly Revision Number    : B0
Version ID                      : V07
CLEI Code Number                : COMP900ARC
Hardware Board Revision Number  : 0x03


Switch Ports Model              SW Version            SW Image                 
------ ----- -----              ----------            ----------               
*    1 26    WS-C3560V2-24TS    15.0(1)SE2            C3560-IPSERVICESK9-M     


Configuration register is 0xF
"""
	v字符串1 = """Cisco IOS Software, 7200 Software (C7200-ADVENTERPRISEK9-M), Version 15.2(4)S7, RELEASE SOFTWARE (fc4)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Wed 01-Apr-15 20:30 by prod_rel_team

ROM: ROMMON Emulation Microcode
BOOTLDR: 7200 Software (C7200-ADVENTERPRISEK9-M), Version 15.2(4)S7, RELEASE SOFTWARE (fc4)

R1 uptime is 5 days, 4 minutes
System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
System image file is "tftp://255.255.255.255/unknown"
Last reload reason: Unknown reason



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco 7206VXR (NPE400) processor (revision A) with 491520K/32768K bytes of memory.
Processor board ID 4279256517
R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
6 slot VXR midplane, Version 2.1

Last reset from power-on

PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
Current configuration on bus mb0_mb1 has a total of 800 bandwidth points. 
The set of PA-2FE, PA-POS-2OC3, and I/O-2FE qualify for "half 
bandwidth points" consideration, when full bandwidth point counting 
results in oversubscription, under the condition that only one of the 
two ports is used. With this adjustment, current configuration on bus 
mb0_mb1 has a total of 400 bandwidth points. 
This configuration is within the PCI bus capacity and is supported 
under the above condition. 

PCI bus mb2 (Slots 2, 4, 6) has a capacity of 600 bandwidth points.
Current configuration on bus mb2 has a total of 0 bandwidth points 
This configuration is within the PCI bus capacity and is supported. 

Please refer to the following document "Cisco 7200 Series Port Adaptor
Hardware Configuration Guidelines" on Cisco.com <http://www.cisco.com>
for c7200 bandwidth points oversubscription and usage guidelines.


4 FastEthernet interfaces
509K bytes of NVRAM.

8192K bytes of Flash internal SIMM (Sector size 256K).
Configuration register is 0x2102"""
	v版本 = 思科.C版本信息(v字符串1)
	print(v版本.fg版权())
	print(v版本.fg序列号())
	print(v版本.fg版本s())
	print(v版本.fg编译日期())
	print(v版本.fg运行时间())
	print(v版本.fg开机日期())
	print(v版本.fg物理地址())
def f接口():
	v字符串0 = """
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        unassigned      YES unset  administratively down down    
FastEthernet0/1        10.0.0.1        YES manual administratively down down    
FastEthernet1/0        unassigned      YES unset  administratively down down    
FastEthernet1/1        unassigned      YES unset  administratively down down    
"""
	v字符串1 = """
Interface              IP-Address      OK? Method Status                Protocol
Vlan1                  unassigned      YES NVRAM  administratively down down    
Vlan11                 unassigned      YES NVRAM  up                    up      
Vlan100                172.17.20.90    YES NVRAM  up                    up      
FastEthernet0/1        unassigned      YES unset  down                  down    
FastEthernet0/2        unassigned      YES unset  down                  down    
FastEthernet0/3        unassigned      YES unset  down                  down    
FastEthernet0/4        unassigned      YES unset  down                  down    
FastEthernet0/5        unassigned      YES unset  down                  down    
FastEthernet0/6        unassigned      YES unset  down                  down    
FastEthernet0/7        unassigned      YES unset  down                  down    
FastEthernet0/8        unassigned      YES unset  down                  down    
FastEthernet0/9        unassigned      YES unset  up                    up      
FastEthernet0/10       unassigned      YES unset  up                    up      
FastEthernet0/11       unassigned      YES unset  down                  down    
FastEthernet0/12       unassigned      YES unset  down                  down    
FastEthernet0/13       unassigned      YES unset  down                  down    
FastEthernet0/14       unassigned      YES unset  down                  down    
FastEthernet0/15       unassigned      YES unset  down                  down    
FastEthernet0/16       unassigned      YES unset  down                  down    
FastEthernet0/17       unassigned      YES unset  down                  down    
FastEthernet0/18       unassigned      YES unset  up                    up      
FastEthernet0/19       unassigned      YES unset  down                  down    
FastEthernet0/20       unassigned      YES unset  down                  down    
FastEthernet0/21       unassigned      YES unset  down                  down    
FastEthernet0/22       unassigned      YES unset  down                  down    
FastEthernet0/23       unassigned      YES unset  down                  down    
FastEthernet0/24       unassigned      YES unset  down                  down    
GigabitEthernet0/1     unassigned      YES unset  up                    up      
GigabitEthernet0/2     unassigned      YES unset  down                  down    
"""
	v接口表 = 思科.C三层接口表(v字符串1)
	for v行 in v接口表:
		print(v行)
def f物理地址表():
	v字符串0 = """
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
 All    0100.0ccc.cccc    STATIC      CPU
 All    0100.0ccc.cccd    STATIC      CPU
 All    0180.c200.0000    STATIC      CPU
 All    0180.c200.0001    STATIC      CPU
 All    0180.c200.0002    STATIC      CPU
 All    0180.c200.0003    STATIC      CPU
 All    0180.c200.0004    STATIC      CPU
 All    0180.c200.0005    STATIC      CPU
 All    0180.c200.0006    STATIC      CPU
 All    0180.c200.0007    STATIC      CPU
 All    0180.c200.0008    STATIC      CPU
 All    0180.c200.0009    STATIC      CPU
 All    0180.c200.000a    STATIC      CPU
 All    0180.c200.000b    STATIC      CPU
 All    0180.c200.000c    STATIC      CPU
 All    0180.c200.000d    STATIC      CPU
 All    0180.c200.000e    STATIC      CPU
 All    0180.c200.000f    STATIC      CPU
 All    0180.c200.0010    STATIC      CPU
 All    ffff.ffff.ffff    STATIC      CPU
  10    0000.b413.3023    DYNAMIC     Gi0/2
  10    001a.8057.6685    DYNAMIC     Gi0/2
  10    1078.d2a0.8422    DYNAMIC     Gi0/2
  10    24f5.aacd.677c    DYNAMIC     Fa0/9
  10    402c.f4ec.9270    DYNAMIC     Gi0/2
  10    40a8.f062.6b10    DYNAMIC     Gi0/2
  10    4437.e605.dcea    DYNAMIC     Gi0/2
  10    4437.e659.230a    DYNAMIC     Gi0/2
  10    4437.e665.3a3a    DYNAMIC     Gi0/2
  10    4437.e665.9f2a    DYNAMIC     Gi0/2
  10    4439.c452.374e    DYNAMIC     Gi0/2
  10    4439.c452.6bb6    DYNAMIC     Gi0/2
  10    4439.c490.0cfa    DYNAMIC     Gi0/2
  10    4439.c491.ff9c    DYNAMIC     Gi0/2
  10    5866.ba82.dce2    DYNAMIC     Gi0/2
  10    6400.6a5b.cd15    DYNAMIC     Gi0/2
  10    6c0b.843e.aacf    DYNAMIC     Fa0/1
  10    6c0b.84ac.ab51    DYNAMIC     Gi0/2
  10    dc4a.3e72.31a9    DYNAMIC     Gi0/2
  10    dc4a.3e77.2519    DYNAMIC     Gi0/2
  10    fc4d.d42e.e174    DYNAMIC     Gi0/2
  10    fc4d.d44a.0cac    DYNAMIC     Gi0/2
  10    fc4d.d4f7.3818    DYNAMIC     Gi0/2
  10    fc4d.d4f7.3d12    DYNAMIC     Gi0/2
  10    fc4d.d4f7.5e89    DYNAMIC     Gi0/2
  10    fc4d.d4f7.6d66    DYNAMIC     Gi0/2
 100    5866.ba82.dce2    DYNAMIC     Gi0/2
 100    5866.ba86.e0ed    DYNAMIC     Gi0/2
   1    000f.e207.f2e0    DYNAMIC     Gi0/2
   1    a456.3059.9f01    DYNAMIC     Gi0/2
   1    a456.3059.a902    DYNAMIC     Gi0/2
   1    a456.3059.b002    DYNAMIC     Gi0/2
   1    a456.3059.bd82    DYNAMIC     Gi0/2
   1    a456.3059.be02    DYNAMIC     Gi0/2
   1    a456.306c.ac01    DYNAMIC     Gi0/2
   1    a456.306c.ac81    DYNAMIC     Gi0/2
   1    a456.306c.ce01    DYNAMIC     Gi0/2
   1    a456.306c.db02    DYNAMIC     Gi0/2
   1    a456.306c.f482    DYNAMIC     Gi0/2
   1    a456.306c.fd82    DYNAMIC     Gi0/2
   1    a456.306c.ff81    DYNAMIC     Gi0/2
   1    a456.306d.0d02    DYNAMIC     Gi0/2
   1    a456.306d.b681    DYNAMIC     Gi0/2
   1    a456.306d.b802    DYNAMIC     Gi0/2
   1    a456.306d.bf82    DYNAMIC     Gi0/2
   1    a456.306d.d402    DYNAMIC     Gi0/2
   1    a456.306d.d782    DYNAMIC     Gi0/2
   1    a456.3082.5182    DYNAMIC     Gi0/2
Total Mac Addresses for this criterion: 68
"""
	v表 = 思科.C物理地址表(v字符串0)
	for v行 in v表:
		print(v行)
def fospf邻居():
	v字符串0 = """
Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           1   FULL/DR         00:00:30    12.0.0.2        FastEthernet0/0
"""
	v表 = 思科.Cospf邻居表(v字符串0)
	for v行 in v表:
		print(v行)
def main():
  #f物理地址表()
	fospf邻居()
if __name__ == "__main__":
	main()