<h1 align="center">Data Product: IoT Device Behaviour</h1>

This data product includes the traffic behaviour of IoT devices for modelling and machine learning.

**Contents Introduction**
- **data**: the final cleaned and transformed data product for subsequent analysis and modelling.
- **code**: a collection of code used for data processing in the project.
- **process_data**: the record of the detailed process, description, and stage-by-stage code output.
- **visualisation**: provides key insights into dataset characteristics, offering valuable perspectives for subsequent research and modelling.
 
## Table of contents
- [Project description](#project-description)
  - [Overview](#overview)
  - [Importance of Project](#importance-of-project)
  - [Product Advantages](#product-advantages)
- [Background and Context](#background-and-context)
  - [Keywords introduction](#keywords-introduction)
  - [Background](#background)
  - [Relation to Previous Work on This Problem](#relation-to-previous-work-on-this-problem)
- [Sources](#sources)
- [Workflow](#workflow)
- [Data description](#data-description)
- [Usage](#usage)
- [Limitation](#limitation)
- [Support information](#support-information)
- [Contributors](#contributors)
- [How Others Can Get Involved](#how-others-can-get-involved)
- [Reference](#reference)


## Project description 

### Overview
The objective is to produce data for the "behaviour patterns of IoT devices." This project cleans, transforms, and structures the data into CSV by utilising the data collected by KDDI. This product will provide effective and useful features for subsequent machine learning models, enabling the modelling and prediction of IoT device types and their associated traffic patterns.

### Importance of Project
The number of IoT devices in households is rapidly increasing, with around 258 million smart homes globally in 2021 and further growth is expected in the coming years.[3] [4] While these devices offer convenience, they are also vulnerable to cyber-attacks.[2] Understanding the behaviour of IoT devices is essential to address these risks. It supports device visibility, which involves detecting and classifying devices, and security risk management associated with IoT devices. This data product lays the foundation for these studies.

### Product Advantages
- **Simplified and  transformed  data**: ease to use for machine learning.
- **Simplified Variable Names and Content**: We renamed some variables related to device behaviour and provided a simplified introduction to device behaviour to avoid confusion caused by excessive information.
- **Transparent Data Process**: periodic output results, introductions, and other relevant information.
- **Data Checking**: use code to validate the data output in the important step.
- **Preliminary Data Feature Analysis**: Utilise simple modelling, analysis, and visualisation methods to provide further insights.

## Background and Context
### Keywords introduction
- **IoT Devices**: IoT devices are smart devices that connect to other devices or the internet through a network, such as lights, network cameras, and smart speakers.

- **Packet**: A packet is the basic unit of data transmitted over a network, containing the information exchanged between devices.

- **Forward/Reverse Flows**: Flows consist of multiple packets. Forward flow refers to the communication initiated by a device, while reverse flow is the response to that communication. Together, they form the complete communication process of the devices.

- **Broadcast Flows**: a kind of special flows, which is sent from one source device to all devices on a network. This method is often used for tasks like network discovery and updates, ensuring that all nodes receive the same information simultaneously. In this data product, a flow is defined as a broadcast when the `hostIP` is `192.168.1.255`.

- **Source/Destination Device**: The devices that initiate or receive network traffic. IoT devices can act as source devices (sending traffic) or destination devices (receiving traffic).

- **Mac Address**: Every network device has a unique physical address called a MAC address, used to identify the device within a local network.

- **IP Address**: An IP address serves as a "location" for devices on the network, helping them find each other on a local network or the internet. IP addresses beginning with `192.168` are typically used for internal networks, while other types of IP addresses identify devices on the internet.

- **Local and Remote Traffic**:
  - **Remote Communication**: This involves IoT devices communicating with external servers or cloud services, usually for firmware updates, data uploads, or receiving remote instructions.
  
  - **Local Communication**: This is when IoT devices communicate with a router or other devices within the same local network, with traffic transmitted only within the local network without going through the internet. 
  
- **PreNAT & PostNAT**:
  - **NAT (Network Address Translation)** is a privacy protection technique that encrypts communication by hiding the actual IP address of devices. When devices use NAT, the router converts the internal IP address to an external IP address, so the outside world only sees the router's address and not the device's true IP address.
  
  - **PreNAT**: This is the network traffic before NAT conversion, where the device's true internal IP address is visible. In preNAT traffic, communication between IoT devices and local devices or remote servers can be identified.
  
  - **PostNAT**: This is the network traffic after NAT conversion, where the device's internal IP address has been replaced by an external IP address, allowing the outside world to see only the router's address. Communication between the device and remote servers or other devices occurs through the router's address.

- **Services and Protocols**:
  Services and Protocols define how devices exchange data.
  - TCP is reliable, ensuring both forward and reverse flows.
  - UDP is faster but does not always have reverse flows. 


| Service   | Protocol | Condition                                               |
| --------- | -------- | ------------------------------------------------------- |
| HTTP      | TCP      | ipPort = 6 & IoT / Host port = 80, 8080, 8008 or 8888   |
| HTTPS     | TCP      | ipPort = 6 & IoT / Host port = 433, 1443, 8443 or 55443 |
| DNS       | UDP      | ipPort = 17 & IoT / Host port = 53 or 5353              |
| NTP       | UDP      | ipPort = 17 & IoT / Host port = 123                     |
| other TCP | TCP      | ipPort = 6 & not HTTP or HTTPS                          |
| Other UDP | UDP      | ipPort = 17 & not DNS, NTP                              |

### Background
Since the data only focuses on IoT device behaviour, it only includes IoT device-initiated flows, which means the source devices are IoT devices. The figure below illustrates the 2 behaviours of IoT devices: 
<br>
![Local_Remote_Flows](https://github.com/user-attachments/assets/5d9ae9d9-d590-47e7-a114-b56e37b2625e)
<br>
### Relation to Previous Work on This Problem

#### Limitations of Existing Work
Previous research proposed methods to infer device types through network traffic characteristics of IoT devices, but these methods have several limitations:

- Rely on hardware or software modifications of home gateways, which poses challenges for large-scale deployment [1].
- Depends on the MAC address or IP address of the device, but NAT hides the internal network identity of devices, making application difficult [1].
- Signature-based detection methods (such as domain names or IP blocks) are not reliable enough when inferring the behaviour of individual devices [1].
- Most existing work relies on complete visibility of local traffic or device identity (such as IP/MAC address) for traffic feature grouping, which presents practical challenges for ISP service deployment [2].
- Although some methods have developed models that can be measured outside the home gateway, they still face traffic loss issues caused by NAT [2].

#### Innovation in Research on IPFIX Data
Unlike previous work, this study uses IPFIX data to infer IoT device types, which has the following advantages:

- Does not require modification of the home network structure, making it suitable for large-scale ISP deployment [1].
- Does not rely on device identity information (such as MAC address or IP address), making it effective in NAT environments [1].
- IPFIX records do not contain packet payload information, thus eliminating privacy concerns.
- Infers device types through traffic characteristics (such as packet count and inter-arrival time), achieving an accuracy of 96%, significantly higher than previous studies of 70-80% [1].

#### Innovation in IoT Device Inference Using IPFIX
This is the first work to infer IoT device types in home networks by analyzing activity characteristics in IPFIX records, with the main contributions including:

- Extracted 28 features, combined with a multi-classifier model and machine learning techniques, to improve prediction accuracy [1].
- Proposed a dynamic inference strategy for the problem of concept drift in traffic and validated the model's performance with data from various home networks [2].
- Investigated the phenomenon of concept drift in the temporal and spatial domains, especially relying on IPFIX records for inference after NAT, avoiding deep packet inspection [2].

#### Extending the Existing Inference Model
Compared with previous research, this work further innovates and extends the inference model:

- Combines IPFIX records with machine learning models, without relying on DNS data or domain names, focusing on addressing the challenge of concept drift [2].
- Previous studies attempted to infer by utilizing partial information (such as the association between domain names and IP addresses), but this study innovatively combines IPFIX and NetFlow tools to solve practical challenges in IoT traffic inference [2].

#### Challenges of Concept Drift
This study is the first to explore the impact of concept drift on IoT traffic inference in the temporal and spatial domains, especially addressing the drift problem at the ISP scale in the case of scarce labelled data [2]. Concept drift has been widely studied in other fields (such as image recognition, electricity markets, network intrusion detection), but there has been little research in the field of IoT traffic inference, and this work fills this gap [2].

## Sources
The data comes from the traffic log of the KDDI Telecom network, which records the pre-NAT traffic information of IoT devices. All traffic is normal and has not been attacked.<br>
### Key attributes
- Packet capture period: 6/25/2019 - 10/10/2019 (108 days).
- The Dataset include:
  	- IPFIX records of 25 different IoT devices (11 categories).
	- 3 kinds of variables: flows, tombstones, and stats.’ flows’ includes 54 variables.
  	- both IoT-initiated and non-IoT-initiated flows.
 		- the flows include remote and local communication, including broadcast communication.

### Data link
https://github.com/nokuik/KDDI-IoT-2019


## Workflow
### overview

![Work Flow](https://github.com/user-attachments/assets/83cbd854-50d6-4b99-9863-bd52669be8dd)

### details
For ease of reading, the order of some workflow details does not match the actual data processing sequence. Please refer to the relevant code for more information.<br>
For details related to the features, please refer to the data description below.<br>
Here is each step of the process in detail below:

#### Step 1 
[OUTPUT ipfix_0](https://github.com/ConnyClock/data3001-data-cyber-6/tree/main/process_data/ipfix_0)

##### Initial data simplification
Only include flow data; exclude irrelevant records(stats and tombstones).
Convert JSON to CSV.

#### Step 2 
[OUTPUT ipfix_1](https://github.com/ConnyClock/data3001-data-cyber-6/tree/main/process_data/ipfix_1)
##### Data Cleaning
1. Remove irrelevant or invalid rows:
   1. remove non-IoT-initiated flows.
   2. remove rows with IPv6 addresses.
   3. remove rows with missing values in all columns.
   4. remove duplicate rows.
   5. remove rows with missing values in key forward flow features.
   6. remove TCP flows without reverse flows (TCP must always be bidirectional).
2. Fix missing values:
   1. replace missing values in reverse flows with 0.
   2. replace missing values in all Average Packet Size with 0.

##### Features Selecting
In the flows collected by KDDI, there are 54 variables (see the output of `ipfix_0` for details). We selected 34 variables based on variable choices referenced in the 2021 and 2023 reports. These include time-related features, MAC, IP, protocol, and forward and reverse packet features. For more details, refer to the data description below.

##### Features Transformation
1. Create a binary feature for the presence of reverse flow.
2. Create a binary feature to distinguish between local and remote communication.
3. Create a binary feature to distinguish between broadcast and other communication.
4. Create 6 binary features based on protocols and network behaviour, including the services: `HTTP`, `HTTPS`, `DNS`, `NTP`, `other TCP` and `other UDP`.
5. Create 2 new transformed features of the IP address: `IoTIP_int` and `hostIP_int`. <br> This integer format facilitates machine learning.
6. break down `start` into `start_date` and `start_time`. 
#####  Output Checking
- missing values (NA)
- empty strings
- data type consistency
- missing data(using last date table, the last date should reach October)

  
#### Step 3 
[Visualisation](https://github.com/ConnyClock/data3001-data-cyber-6/tree/main/visualisation)
##### Visualisation
In step 3, the team visualized the data output by creating scatter plots, modelling the data, and generating a correlation matrix to identify which features have the highest impact and to assist in data splitting. 
Key Steps:
- Modeled the Data: The data was modeled to understand its structure and identify key relationships between features.
- Created a Correlation Matrix: A correlation matrix was generated to quantify the relationships between different features, highlighting those with the strongest correlations.
- Visualized with Scatter Plots and Histograms: Scatter plots and histograms were created to visually represent the distributions and relationships within the data, providing deeper insights into the feature interactions.
  
#### Step 4
[OUTPUT final data](https://github.com/ConnyClock/data3001-data-cyber-6/tree/main/data)

[CODE data splitting](https://github.com/ConnyClock/data3001-data-cyber-6/tree/main/process_data/Data_Spliting)
##### Data splitting
After all steps, the csv file is still large, which is not conducive to subsequent data modeling and analysis. Therefore, we have splited the data into several parts based on the month to facilitate subsequent operations and be more flexible for the work of data modeling group. 

## Data description
### Overview
- This data product comprises **25 CSV files**.
- All flow records are initiated by IoT devices.
- This data is split by month. (If you prefer a different split method, please use the output in `ipfix_1`)
- There are **25 distinct IoT devices** across **11 categories**.
- The dataset contains **46 features** + **1 special feature for splitting** and **19.12 million rows** in total.
  
| Device                                | Category           | Mac_Address       | row_count    |
| ------------------------------------- | ------------------ | ----------------- | ------------ |
| Amazon Echo gen2                      | Smart speaker      | 4c:ef:c0:17:e0:42 | 368127       |
| au network camera                     | Network camera     | ec:3d:fd:39:6f:98 | 53346        |
| au wireless adapter                   | IoT gateway/hub    | b0:ea:bc:ea:ac:86 | 606248       |
| Bitfinder Awair Breathe Easy          | Environment sensor | 70:88:6b:10:22:83 | 259398       |
| CANDY HOUSE Sesami Wi-Fi access point | Door lock          | 38:56:10:00:1d:8c | 132477       |
| Google Home gen1                      | Smart speaker      | 48:d6:d5:92:96:a2 | 6008890      |
| I-O Data QWatch                       | Network camera     | 34:76:c5:7f:91:07 | 1937200      |
| iRobot Roomba                         | Robot cleaner      | 40:9f:38:e7:7f:09 | 10420        |
| JVC Kenwood CU-HB1                    | IoT gateway/hub    | 00:a2:b2:b9:09:87 | 1094195      |
| JVC Kenwood HDTV IP camera            | Network camera     | e0:b9:4d:5c:cf:c5 | 18936        |
| Line Clova Wave                       | Smart speaker      | a8:1e:84:e8:cc:c3 | 190425       |
| Link Japan eRemote                    | Remote controller  | 34:ea:34:76:ea:68 | 287423       |
| Mouse computer room hub               | IoT gateway/hub    | aa:1e:84:06:1c:b4 | 10708        |
| Nature Remo                           | Remote controller  | 60:01:94:54:6b:e8 | 5844         |
| Panasonic Doorphone                   | Doorphone          | bc:c3:42:dc:24:78 | 942608       |
| Philips Hue Bridge                    | Light              | 00:17:88:47:20:f2 | 316271       |
| PLANEX camera one shot!               | Network camera     | 00:1b:c7:fa:c3:e6 | 1465299      |
| PLANEX SmaCam Outdoor                 | Network camera     | 00:22:cf:fd:c1:08 | 45021        |
| PLANEX SmaCam PanTilt                 | Network camera     | e0:b9:4d:b9:eb:e9 | 27207        |
| PowerElectric Wi-Fi plug              | Plug               | ec:f0:0e:55:25:39 | 220095       |
| Qrio Hub                              | Door lock          | 80:c5:f2:0b:aa:a9 | 40682        |
| Sony Bravia                           | TV                 | 04:5d:4b:a4:d0:2e | 2772646      |
| Sony network camera                   | Network camera     | 70:26:05:73:6e:31 | 25737        |
| Sony smart speaker                    | Smart speaker      | 6c:5a:b5:56:39:3e | 2275382      |
| Xiaomi Mijia LED                      | Light              | 78:11:dc:55:76:4c | 10271        |
| **SUM**                               |                    |                   | **19124856** |

 
### Observations (Rows)
Rows express 2 types of device behaviour:
- Local traffic (features:  remote = 0, IoT -> router or other devices)
   - including special broadcast communication.(`hostIP = 192.168.1.255`)
- Remote traffic (features: remote = 1, IoT -> Server)
	
simple devices such as light produce fewer flows, while devices such as smart speakers produce more flows with more remote communications.
 
![histogram](https://github.com/user-attachments/assets/93b0de1d-6e8f-4e5e-8792-8b6c50a8877b)



### Features (Columns)

The features selection refer to the work of Pashamokhtari, [2]

Total Number of Features:

#### Time related 
| Features     | Description                                                                                     | FeaturesName in KDDI         |
| ------------ | ----------------------------------------------------------------------------------------------- | ---------------------------- |
| start_date   | forward flows start date (e.g. 25/6/2019)                                                       | flowStartMilliseconds        |
| start_time   | forward flows start time (e.g. 8:37:00.037)                                                     | flowStartMilliseconds        |
| duration     | the total time the forward flow lasts in milliseconds                                           | flowDurationMilliseconds     |
| reverseDelta | the delay between the end of the forward flow and the start of the reverse flow in milliseconds | reverseFlowDeltaMilliseconds |

#### Mac, IP and Protocol 

These features interpret the key information of devices and their behaviours.<br>For transforming the IP address into integer form, We used the formula `aaa * 256 ^ 3 + bbb * 256 ^ 2 + cc * 256 ^ 1 + ddd * 256 ^0` for IP `aaa.bbb.ccc.ddd`.[5]<br>

| Features   | Description                                                  | FeaturesName in KDDI     |
| ---------- | ------------------------------------------------------------ | ------------------------ |
| IoTMac     | identify IoT device                                          | sourceMacAddress         |
| hostMac    | identify other devices, router or server                     | destinationMacAddress    |
| IoTIP      | identify source device destination                           | sourceIPv4Address        |
| IoTIP_int  | IoTIP in integer                                             | -                        |
| hostIP     | identify  other devices, router or server device destination | destinationIPv4Address   |
| hostIP_int | IoTIP in integer                                             | -                        |
| ipProto    | identify the protocol                                        | protocolIdentifier       |
| IoTPort    | identify service                                             | sourceTransportPort      |
| hostPort   | identify service                                             | destinationTransportPort |


#### Packet
Since IPFIX records are bi-directional, a corresponding reverse version of each feature reflects the activity of the opposite flow direction.<br>The feature name of reverse flow is adding "reverse" before the following feature name. For example,( "PacketCount" -> "reversePacketCount.")

**Key Packet**

| Features    | Description                                                  | FeaturesName in KDDI |
| ----------- | ------------------------------------------------------------ | -------------------- |
| PacketCount | Total number of packets in the communication flow            | packetTotalCount     |
| BytesCount  | Total number of bytes transferred in the communication flow. | octetTotalCount      |


**Other Packet**

| Features             | Description                      | FeaturesName in KDDI              |
| -------------------- | -------------------------------- | --------------------------------- |
| SmallPktCount        | packet with < 60 bytes payload   | smallPacketCount                  |
| LargePktCount        | packet with >= 200 bytes payload | largePacketCount                  |
| NonEmptyPktCount     | packet with payload              | nonEmptyPacketCount               |
| DataByteCount        | payload size in total            | dataByteCount                     |
| AvgIAT               | packets interval time μ          | averageInterarrivalTime           |
| FirstNonEmptyPktSize | first non-empty payload size     | firstNonEmptyPacketSize           |
| MaxPktSize           | maximum payload size             | maxPacketSize                     |
| StdevPayloadSize     | payload size σ                   | standardDeviationPayloadLength    |
| StdevIAT             | packet inter-arraival time σ     | standardDeviationInterarrivalTime |
| AvgPacketSize        | DataByteCount/PacketCount        | bytesPerPacket                    |

										
#### Binary(Mac, IP and Protocol)

| Features          | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| reverseFlowExists | Indicates whether the reverse flow exist(1 for yes, 0 for no)                |
| remote            | Indicates whether the traffic is remote (1 for yes, 0 for no)                |
| broadcast         | Indicates whether the communication is a broadcast (1 for yes, 0 for no)     |
|                   |                                                                              |
| HTTP              | Indicates whether the protocol is HTTP (1 for yes, 0 for no)                 |
| HTTPS             | Indicates whether the protocol is HTTPS (1 for yes, 0 for no)                |
| DNS               | Indicates whether the protocol is DNS (1 for yes, 0 for no)                  |
| NTP               | Indicates whether the protocol is NTP (1 for yes, 0 for no)                  |
| TCP_others        | Indicates whether the protocol is other service in TCP (1 for yes, 0 for no) |
| UDP_others        | Indicates whether the protocol is other service in UDP (1 for yes, 0 for no) |

#### Special - Splitting
This feature used in step data splitting is retained to streamline future data processing, enabling faster categorization and querying during operations like merging.
| Features          | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| year_month | year and month in chr (e.g. 2019_10)                |

## Usage
This data product is created to help network operators and security teams understand and manage IoT device traffic more effectively. By utilizing smart analytics and machine learning, users can uncover valuable insights into device behaviors and network patterns, making it easier to optimize performance and enhance security.

The primary objective of this data product is to effectively recognize traffic patterns and classify IoT devices within a network. By leveraging a wide range of traffic-related features—such as total packets, protocol types, and source and destination IP addresses—this product supports the training and testing of machine learning models. These models are instrumental for network operators and security teams, enabling them to manage and classify devices with greater accuracy and efficiency. The insights derived from these models can help in optimizing network performance and enhancing security measures against potential threats.

### Simple Analytical Modelling

#### 1) Device Type Classification:

To achieve accurate device classification, we propose utilizing a comprehensive set of network features from the dataset. By applying various classification algorithms, including decision trees, random forests, and support vector machines, we can develop a robust model that predicts the types of devices generating the traffic.

Key features that will be instrumental in this process include:

- **PacketCount**: The total number of packets transmitted, which indicates the level of activity associated with each device type.
- **BytesCount**: The total volume of data (in bytes) sent and received, providing insights into the data usage patterns of different devices.
- **ipProto**: Identifying the specific protocols used can reveal typical behaviors of device types, enhancing the model’s ability to distinguish between them.


#### 2) Protocol Traffic Analysis:

In this section, we delve into the distribution and behavior of various protocols (such as HTTP, TCP, and UDP) utilized in device communications. By analyzing these patterns, network managers can gain deeper insights into inter-device traffic, which is critical for:

Identifying communication patterns: Understanding which protocols are predominantly used by certain devices can inform resource allocation and network configuration strategies.
Optimizing resource allocation: By correlating protocol usage with device behavior, managers can adjust bandwidth and prioritize traffic flows to ensure optimal performance and reliability.
Moreover, protocol-related features, such as **sourceTransportPort** and **destinationTransportPort**, serve to further differentiate the behaviors of various devices. These insights not only enhance network efficiency but also assist in identifying anomalous behavior indicative of potential security threats.

#### 3) Time Series Analysis:

We will employ time series models such as ARIMA (AutoRegressive Integrated Moving Average) to analyse and predict temporal trends in network traffic. This method enables us to capture and forecast fluctuations in network traffic over time, which is crucial for proactive network management.

The features that will be leveraged for modelling include:

- **start_time**: This timestamp indicates when the traffic flow begins, allowing for the assessment of peak usage times and trends.
- **duration**: This measures the length of each traffic flow, providing insights into typical usage patterns and potential anomalies.
  
Through the application of time series analysis, the model can predict both device types and traffic patterns for each traffic record. This capability will greatly assist in classifying and managing network traffic, allowing for effective differentiation between various IoT devices.

## Limitation

- To avoid interference with the data analysis, we remove all records with `hostIP = 255.255.255.255`, which indicates broadcast communication. Most of these records have missing values in `IoTIP` and are concentrated mainly at the beginning and end of the dataset. Specifically, in `planex_smacam_pantilt`, this device only exhibited this behavior from June 25 to July 10. Consequently, the data starts from July 10 in `planex_smacam_pantilt`, and some records end earlier than October 10 for the same reason.
- Due to the large number of IP addresses in the data, we have only transformed the IP address to an integer. This does not show the full details of the behaviour. For example, Amazon Gen2 communicates heavily with the Amazon server, but the integer cannot determine if the IP address belongs to the Amazon server.

## Support information

| Full Name      | University Email                 | zID      |
| -------------- | -------------------------------- | -------- |
| Johnny Zhou    | johnny.zhou1@student.unsw.edu.au | z5417652 |
| Saanvi Yerawar | s.yerawar@student.unsw.edu.au    | z5425350 |
| Wanyun Zhong   | wanyun.zhong@student.unsw.edu.au | z5307005 |
| Zhe Wang       | zhe.wang7@student.unsw.edu.au    | z5339253 |

## Contributors
| Contributor               | Roles           | Contribution in Data Product                                           | Contribution in README wirting                                                                                  |
| ------------------------- | --------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Saanvi Yerawar            | student         | project planning, Visualization, data modelling                        | Project description: other, Usage ,Workflow: Visualisation                                                                                   
| Johnny Zhou               | student         | project planning, Data cleaning, Features selecting and transformation | Project description: other, workflow: feature selection, data cleaning & feature selection                      |
| Zhe Wang                  | student         | project planning, Preliminary data simplification, Data splitting      | Project description: previous related work, Sources, Workflow: Preliminary data simplification & data splitting |
| Wanyun Zhong              | student         | project planning, Data cleaning, Features selecting and transformation | Project description: other, Data description, workflow: feature selection, data cleaning & feature selection     |
| Professor Gustavo Batista | Supervisor      | -                                                                      | -                                                                                                               |
| Professor David Warton    | Course Convener | -                                                                      | -                                                                                                               |

## How Others Can Get Involved
If you have any questions about the data product, please contact the relevant contributors.<br>
If there is any error/problem in the data product, please post an issue.

## Reference
[1] A. Pashamokhtari, N. Okui, Y. Miyake, M. Nakahara and H. H. Gharakheili, "Inferring Connected IoT Devices from IPFIX Records in Residential ISP Networks," 2021 IEEE 46th Conference on Local Computer Networks (LCN), Edmonton, AB, Canada, 2021, pp. 57-64, doi: 10.1109/LCN52139.2021.9524954. keywords: {Performance evaluation;Home automation;Protocols;Telemetry;Object recognition;Security;IP networks;IoT;traffic inferencing;residential networks;IPFIX;machine learning},

[2] A. Pashamokhtari, N. Okui, M. Nakahara, A. Kubota, G. Batista and H. Habibi Gharakheili, "Dynamic Inference From IoT Traffic Flows Under Concept Drifts in Residential ISP Networks," in IEEE Internet of Things Journal, vol. 10, no. 17, pp. 15761-15773, 1 Sept.1, 2023, doi: 10.1109/JIoT.2023.3265012.
keywords: {Internet of Things;Context modeling;Data models;Home automation;Training;Performance evaluation;behavioural sciences;Concept drifts;IoT;IPFIX data;machine learning;traffic inference},

[3] Earthweb, “Smart Home Statistics,” 2022. [Online]. Available:
https://earthweb.com/smart-home-statistics/

[4] Security Sales & Integration, “Global Smart Home Market Projected
to Reach $158B by 2024,” 2020. [Online]. Available: https://www.securitysales.com/research/global-smart-home-158b-2024/

[5] Sevastyanov, E, "Converting ipv4 addresses to decimal: A step-by-step guide," 2024. Available: https://interlir.com/2024/02/19/converting-ipv4-addresses-to-decimal-a-step-by-step-guide/#:~:text=Step%2Dby%2DStep%20Conversion%20Guide,from%200%20on%20the%20right). 

[6] OpenAI ChatGPT, "English Writing Improvement," 2024. Available: https://chat.openai.com/
