# Classification of IoT Devices Based on Analysis of Internet Flow Data

## Project description:
**What is the specific objective of this project?**

Internet of Things (‘IoT’) Devices are becoming more and more integrated to our daily lives and professional environment. Durate (2024) highlights that there are now more than 15 billion of IoT devices as of 2024, and predicts this number will increase significantly in the foreseeable future. Nevertheless, while the sheer number of IoT devices has increased, they come along with significant security risks. Two of the most crucial security risks involve using weak or default passwords and connecting with unsafe service ports. In the meantime, the lack of essential knowledge on device safety of ordinary family user also exacerbates the security risks of IoT devices (Pashamokhtari et al., 2023). As such, this project aims to identify the type of IoT device in family networks by analysing IPFix records, providing insightful information to improve existing safety measures.

Therefore, the primary objective of this project is to construct models to classify IoT devices, with the use of datasets in relation to network flow. The data product is thus designed around network flow features, which are critical for a model that is able to conduct analysis of IoT devices’ behaviour. This is how the data product is closely aligned with the primary objective of this project.

**Why is it important or significant?**

From medical equipment to GPS sensors, IoT devices are common in every single professional industry. These devices are therefore the frequent targets of cyberattacks and have concerns regarding privacy data leakage, causing significant financial and reputational harm to both individuals and many corporations. Unfortunately, many family users disregard the existing safety risks of these devices, and fail to take measures such as adopting strong passwords and enhancing the safety strength of network ports. As such, they are not only vulnerable to cyberattacks, but also suffer more losses from such attacks.

Accordingly, classification and management of these devices become crucial, especially for issues in relation to cyber security and user behaviour analysis. The critical objective of this project is to accurately classify the exact type of IoT device in family networks through analysis of IPFix records. A flexible structure is adopted in this project to handle differences between IoT devices and protocols. This project would help our client in enhancing managerial efficiency and cyber security by mitigating potential cyber risks through unknown or unsafe device connection. 
 
**How does this relate to previous work on this problem?**

This project’s contributions are based on the research products from 2021 and 2023. The 2021 research identifies the type of device through analysing post-NAT IPFix flow data. This project further utilises IPFix data to monitor the behaviour of IoT devices. One improvement is that this project has a higher visibility for devices and tends to enhance network safety. The 2023 research introduces the idea of ‘concept shift’, which refers to dynamic changes in data over time. The data of this project integrates this concept, acknowledging the evolving nature of data, ensuring the robustness and security of network systems. 

**The significance of the data product**

It is critical for the modelling group to formulate a model to accurately identify the type of IoT device. Our data product provides necessary information to assist in such classification. Our data regarding network flow include the type of protocol used, transport port, IP address etc. that may reveal the behaviours of these IoT devices. The modelling group may wish to use machine learning and other modelling methods to create efficient classification model. 

## Sources:
The data of this project sourced from the IPFix flow records of 25 different IoT devices in the pre-NAT environment between 25 June 2019 and 10 October 2019. The dataset is constituted by fields based on network flow capture.

## Workflow:

For the purpose of cleansing the dataset such that the modelling team could easily employ, we will delete irrelevant data, deal with missing values and ensure the consistency of key fields.

Our essential approach is to combine all steps to become a cleansing function. This function would perform all necessary cleansing to the subject datasets, including deleting meaningless rows (e.g. rows in theory cannot have N/A value but in reality they have), replacing some N/A values to 0, cleaning invalid IPv4 addresses, introducing further variables such as protocol identifiers and remote server IP address. Please see the attachment for the details of our code. As such, every dataset would be cleansed through the performance of following steps.

1.	Delete all NULL rows from data$flows and only keep the rows that are not NULL.
2.	Delete the rows that have either invalid source or destination IPv4 addresses based on https://www.ipv4mall.com/blogs/valid-ipv4-address/ <img width="416" alt="image" src="https://github.com/user-attachments/assets/c8bf9049-c591-42b8-ba71-9c8077446375">
3.	We will delete variables that are completely irrelevant. These variables are either 0 or 0x000 in all available datasets, providing no valid information. They are deleted to ensure the data is not redundant and improve the efficiency of the potential models applied. These variables are: ingressInterface, egressInterface, vlanId, silkAppLabel, observationDomainId, collectorName.
4.	We acknowledge that there are exceptional variables such as flowEndReason. It has blank values for some datasets, but it has meaningful values for others. To ensure the consistency of data and to make further handling convenient, we will replace the blank values to be NR (No Reason).
5.	We will perform following steps to protocolIdentifier:

For rows that have protocolIdentifier being 6 (TCP), we will delete the entire row if it has any N/A value. This is because TCP protocol is bidirectional transmission protocol. When a packet is sent from the source device to the destination device, a packet would typically be returned as a response. Hence, for IoT devices that has a TCP protocal, there should be no missing value in relation to variables regarding both forward and reverse. If there is any N/A value in our records, this will mean some key transmission information is lost, therefore impacting the integrity and accuracy of the entire connection. 

6.	Handling missing value

We have divided all variables into four different categories (this is inspired from the 2023 research in how they selected key variables and characteristics):

a.	Critical variables

Step – If any important variables are N/A, we will delete the subject rows entirely.
Important variables include: 

flowStartMilliseconds, flowEndMilliseconds: they represent the starting and ending times of the relevant flows. The duration of the flow is essential in our analysis, and N/A would mean invalid flow records.

sourceIPv4Address, destinationIPv4Address: source and destination IP addresses are fundamental features of network flows. N/A or missing values mean the network flow is incomplete. 

sourceTransportPort, destinationTransportPort: source and destination transport port are important compoents in transmitting information. N/A would indicate a missing information of port.

protocolIdentifier: it represents the type of protocol and is directly relevant to the nature of a network flow.

tcpSequenceNumber, reverseTcpSequenceNumber: TCP sequence numbers could be used to track the sequence of data packets. Missing these values would mean network flow could not be tracked.

b.	Text variables:

Step – N/A would be replaced by other texts.

For initialTCPFlags, reverseInitialTCPFlags, unionTCPFlags, reverseunionTCPFlags: we would use NF (No flags) for any missing values.

c.	Count variables

Step – Replace N/A with 0

packetTotalCount, reversePacketTotalCount, octetTotalCount ，reverseOctetTotalCount, smallPacketCount, reversepacSmallPacketCount, largePacketCount, reverseLargePacketCount, reverseTcpUrgTotalCount，TcpUrgTotalCount: these variables record the size and number of network packets. N/A typically means no packet being transmitted.

nonEmptyPacketCount, reverseNonEmptyPacketCount, bytesPerPacket, dataByteCount, reverseDataByteCount: these values mean the number of valid bytes for non-empty packets. N/A means no packets or bytes transmitted, and therefore replacing them by 0 is reasonable.
firstNonEmptyPacketSize, reverseFirstNonEmptyPacketSize, reverseMaxPacketSize, maxPacketSize: missing values indicate no information packet sizes or transmission, and therefore inserting 0 is reasonable.

reverseStandardDeviationPayloadLength, standardDeviationPayloadLength, reverseStandardDeviationInterarrivalTime, standardDeviationInterarrivalTime: missing values indicate no packet transmitted or only one packet transmitted, and therefore replacing 0 is reasonable. 

reverseSmallPacketCount, reverseNonEmptyPacketCount, reverseBytesPerPacket, reverseDataByteCount: missing values indicate no reverse packets, inserting 0 is therefore reasonable. 

averageInterarrivalTime, reverseaverageInterarrivalTime: if there is no interarrival time, 0 could be a default value as there is no calculable time between packets.

d.	Other variables

For ipClassOfService: missing value would be replaced by 0x00 (default value). This variable represents class of IP service, used to determine priorities between network flows. 0x00 is the default value, meaning that no priority treatment is required. N/A would mean that this class of IP service is not recorded, which also means that no priority treatment is required.

For firstEightNonEmptyPacketDirections, reverseFlowAttributes: missing value would be replaced by 00 (default value). For similar reasons regarding ipClassOfService, using 00 to replace any missing values is reasonable as 00 means ‘not recorded’ or ‘no direction’. 

For rows that have protocolIdentifier other than 6 (TCP), e.g. rows that have protocolIdentifier of 17 (UDP), we will replace any N/A value of that row to be 0. This is because for non-TCP protocols, N/A means no packet being transmitted, rather than any packet being lost. As such replace any N/A value to 0 is reasonable under these circumstances.

7.	Introducing six binary variables regarding protocol characteristics: HTTP, HTTPS, DNS, NTP, TCP, UDP

These protocol characteristics represent the protocol used by devices in connecting network, providing information regarding their internet behaviour. Different IoT devices use different protocol to proceed communication. The original dataset does not outline the specific protocol used by each IoT device. These variables are therefore crucial in helping the modelling group to capture the communication behaviour of each IoT device, enhancing the efficiency in formulating a relevant model.
 
8.	Creating a remote server IP address variable

This variable checks if a device is connected to a remote server. A remote server IP address is critical for the initiator of any communication. The modelling group may compare this IP address with the source and destination IP addresses to determine which device initiates the communication. This variable is highly helpful especially in further analysing network flows and device behaviour.

## Data Description:

**Accessing the product**

The data would be stored in the format of data.frame in R. It could be loaded through read.csv() function, using view(), summary() and other R functions to further explore. The datasets are stored in terms of rows and columns. Each row represents a network flow and each column shows a feature of that flow. 

Accessibility was a major factor kept in mind when developing the data product. Instead of developing a large singular file that may not be accessible to certain devices used by the modelling team, the product is broken down into 25 cleaned datasets. Each dataset is an IoT device.  This allows for the modelling team to access the data without compromising the integrity of the product. The modelling team should utilise all the datasets for their models to ensure there is diversity within the data without bias and overfitting in their discoveries.

Furthermore, the separation of the dataset allows for the modelling team to deep dive into each IoT and gain a more holistic understanding of why protecting IoT devices from cybersecurity attacks is crucial. The breakdown also allows for tailored approaches to pre-processing and modelling for improved performance and optimises data retrieval time which would help the overall run time and processing power of the modelling team’s models.

**Observations**

The dataset includes many observations. Each row represents an observation in the form of network flow, and records all required information regarding the transmission between two IoT devices.

**Features (Columns)**

Our product contains 55 features. They can be mainly divided into the following categories:

•	Time related features: such as flowStartMilliseconds/flowEndMilliseconds to record the beginning and ending of network flows.

•	Protocol related features: such as protocolIdentifier to indicate the type of protocol used (e.g. TCP, UDP)

•	Address and transport port features: such as sourceIPv4Address / destinationIPv4Address and sourceTransportPort / destinationTransportPort

•	Packets and bytes features: such as packetTotalCount / octetTotalCount to represent the total packets transmitted

•	TCP related features: such as tcpSequenceNumber to track the sequence of packet

•	Other: such as flowEndReason to describe the reason why a flow ended

## Purpose:

Our data product is mainly network flow data. It includes detailed information regarding each flow transmitted between devices, such as IP addresses, protocol types, the number of packets, the duration of each flow etc. It could be mainly applied in analysis regarding network safety and device behaviour. Classification models and cluster analysis may also be helpful in analysing the network flow. 

In terms of further modelling and analysis, a classification model aims to analyse network flow features to identify the type of network device would be desirable. In relation to model selection, random forest is a got fit with the data product. Random forest is capable of handling a large number of features or variables (there are 55 variables in the data product). Random forest could automatically evaluate the importance of each variable, helping to identify the variables that contribute most to prediction, being the main objective of this project. Random forest also performs well against noise and outliers, and is helpful in preventing any outfitting. Particularly, it provides decent stability in terms of prediction results, by combining multiple decisions trees together. Random forest is therefore highly effective in further fine tuning of the model, especially when the modelling group seeks to analyse device behaviour and network activity.

Should any assistance be required, please contact
Wanyue z5356249@ad.unsw.edu.au, Junyi Hao z5377436@ad.unsw.edu.au
Jacky Gan z5313781@ad.unsw.edu.au

## Contribution

Data product:

Workflow by Junyi Hao and Wanyue

Code by Junyi Hao and Wanyue

Data Cleansing by Junyi Hao and Wanyue

Report:

Project description by Vishwa Desai and Wanyue

Data description by Vishwa Desai and Junyi Hao

Workflow by Shivani Kadiyala, Junyi Hao and Wanyue

Purpose by Jacky Gan and Junyi Hao

Jacky is also responsible for drafting, editing and proofreading 

Every member participates and communicates through group meetings (either remote or in person).

## References:

1.Pashamokhtari, A, Okui, N, Nakahara, M, Kubota, A, Batista, G & Habibi Gharakheili, H 2023, 'Dynamic inference from IoT traffic flows under concept drifts in residential ISP networks', IEEE Internet of Things Journal, vol. 10, no. 17, pp. 15761-15773, accessed 22 September 2024, DOI: 10.1109/JIOT.2023.3265012.

2.Duarte, F. (2024). Number of IoT Devices. Exploding Topics. Available at: https: https://explodingtopics.com/blog/number-of-iot-devices [Accessed 22 September 2024].

3.IPv4 Mall (n.d.) Valid IPv4 address. Available at: https://www.ipv4mall.com/blogs/valid-ipv4-address/ (Accessed: 3 October 2024).
