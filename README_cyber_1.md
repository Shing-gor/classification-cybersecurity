## Project Title: IoT Device Network Behavior Classification - Data Product Phase

### _Project Description:_

This phase of the project focuses on creating a **data product** derived from processing over 20 million IPFIX records collected from 25 IoT devices. The product will facilitate the accurate classification of these devices based on their typical network behaviour. By analyzing IPFIX records, the goal is to accurately identify and categorize IoT devices through machine learning conducted by our colleagues in the modelling team. Such accurate classification will improve data modelling, contributing to better network security by identifying the normal behaviour of IoT devices, aiding in the detection of anomalies.

_About IoT devices_

IoT, or the Internet of Things, refers to devices that generate traffic and autonomously function on a network without direct human interaction. These include devices such as cameras, printers, smart speakers and digital door locks. Unlike personal computers or mobile phones, which are actively operated by users, IoT devices typically have limited computational power, lower memory capacity and fewer software updates. As these devices constantly interact with networks, they are prone to malware infections and cybersecurity attacks, which can compromise both individual devices and the network as a whole. As a result, IoT devices are known to be particularly vulnerable to cybersecurity attacks. If exploited, these susceptibilities can result in unauthorised access or data breaches.

_Why is it important or significant?_

For KDDI specifically, this classification system addresses a significant cybersecurity challenge by providing insights into IoT device behaviour and what is most distinguishable for certain categories of devices, thus allowing KDDI possible avenues to create machine learning monitoring to detect anomalies and automated responses to shut down such attacks and/or vulnerabilities. By providing a reliable method for device classification, this project contributes to the development of models that can monitor and flag irregular traffic patterns. This enables faster network administration responses, strengthens both device and broader network security and helps allocate network resources more effectively. Moreover, early detection of unusual activity ensures quicker intervention to prevent potential security incidents. Overall, our data product will enhance security measures, optimise network performance, and support ongoing advancements with our industry partner in IoT traffic analysis and management. 

_How does this relate to previous work on this problem?_

This project builds on previous research in network traffic analysis and IoT device classification. It leverages established methodologies in data science and machine learning to create a robust data product and classification system. (Ullah et al., 2024)

_Real-world impact given KDDI's interests_

Given, IoT devices and their increasing prevalence within homes, offices, businesses and day-to-day lives, classification and monitoring of such are critical to prevent data incidences and security breaches. Our work through this data product can support KDDI in further improvements  on device classification based on live feed of network data (in JSON form), allowing our client to further secure its IoT networks, particularly in detecting malicious activities like DDoS attacks or unauthorized data transmissions, particularly given our client is a leading telecommunications and data services provider with a clear focus on strengthening network security.

As such, given how integral enhancing cybersecurity is to KDDI's mission, our project helps to address the classification and detection of IoT anomalies which allow the securing of network and IoT devices from vulnerabilities through collaboration with our modelling colleagues and in creating this data product we have supported our clients efforts to protect vulnerable telecom operators.

### _Sources_

The data for this project is sourced from network traffic logs, courtesy of our client KDDI, which includes IPFIX records from multiple IoT devices with detailed metrics such as:
- Packet count
- Total bytes exchanged
- IPv4 addresses (source and destination)
- Flow timestamps
- Transmission ports and more.

These metrics were captured across a period of over 5 months (108 days) from 25 June to 10 Oct 2019 from 25 IoT devices operating in a live network environment. Devices connected via hubs/gateways were categorised based on IoT devices transmitting information.

Note: We have also referenced our information from the journal article provided by Hasan Habibi (Pashamokhtari et al., 2021).

### _Workflow_
1. Data Upload: Downloaded network traffic logs in the form of JSON data from IoT devices courtesy of our sponsor KDDI and processed large JSON files. Converted to a palatable CSV before importing data into a pandas data frame.
2. Data Preprocessing:

   __Handling of missing values and attributes__
    - Removal of missing values and dropping of unnecessary columns of `stats` and `tombstone`
    - Removal of NA rows and duplicate flows in the device network (this was done with precaution)
    - Removal of rows with missing critical information such as IP address, MAC addresses etc.
    - Rows with outlier values removed (e.g. advised maxpacketCount has a threshold of 200,000).
    - Imputation of missing numerical values with appropriate values as can be seen in previous work in the IoT/cybersecurity field e.g. impute of 0 for numerical attributes such as `reversepacketTotalCount`, `reversedataByteCount`, `reverseoctetTotalCount` etc. (Li et al., 2024)
     - Removal of other outliers. Only a few outliers were removed as many theoretical outliers behave normally within the typical range of certain attributes. However, some outliers were still removed, such as values under `totalPacketCount`. Values for packet count cannot exceed 65,000 bytes, however, some entries saw values of over 200,000 bytes and thus were removed.
   __Handling of dummy variables and one-hot encoding of values and attributes__
    - Encoding of `sourceIPv4Address` and `destinationIPv4` to a long integer to maintain a relationship between values using the package '*ipaddress*'. This method was chosen over one-hot encoding as given the sheer number of different IP addresses for some of the devices, it would create too excessively high-dimensional and sparse matrix. This encoding also retains recognition of adjacent nodes and network and in doing so can be an attribute that aids in the classification of devices on the same network. (Alani, 2021)
For instance, when given the following addresses of dtype 'object':
        
        |sourceIPv4Address|destinationIPv4Address|
        |-----------------|-----------------|
        |  192.168.1.225 |	192.168.1.1	|
        
        The encoding using 'ipaddress' would encode into the following corresponding long integers given the code :
        ```rb
        test['sourceIPv4Address'].apply(lambda x: int(ipaddress.IPv4Address(x)))
        ```
        |sourceIPv4Address|destinationIPv4Address|
        |-----------------|-----------------|
        |  3232236001 |	3232235777	|


    - Encoding of `flowStartMilliseconds` and `flowEndMilliseconds` into separate columns for the different time values. Columns were formed for milliseconds, seconds, minutes, hours, days and months. This was done to split the time into more manipulatable integer values rather than maintaining a strict date-time format.
    
    - Removal of columns as the data values did not add further information to any possible model. This includes the following; `egressInterface`, `ingressInterface` and `CollecterName`,  which only contain one value, usually a default format such as "0x000" which indicates no presence of the attribute in any of the network sessions. These columns were removed as they were deemed as redundant and these singular values were common across different device types, hence unsuitable to distinguish between devices.
   
    - Encoding of `FlowEndReason` using one-hot encoding with distinct values of 'active', 'idle', 'Unknown' and 'eof'. Having 3 unique values is suitable for one-hot encoding as it not only avoids excessive dimension complexity being introduced but allows categorical variables to be represented as a numerical input that allows multiple types of machine learning algorithms to be applied. Note: For network flows that fall under 'unknown', this may have occurred as a result of the flow never reaching an end and thus a reason not populated. For example, the data below represents a flow with an 'idle' flow resolution reason and timed out.
  
       | flowEndReason_Unknown | flowEndReason_active | flowEndReason_idle |
       |-----------------|-----------------|------------------|
       |  0 |	0	| 1 |
   
    - Binary encoding of attributes with TCP flags which includes the following attributes of `initialTCPFlags`, `unionTCPFlags`, `reverseInitialTCPFlags` and `reverseUnionTCPFlags`. 
    
      To demonstrate, if a network flow contained 'AP', this would mean it had a '1' value for `initialTCPFlags_A` and `initiaTCPFlags_P` with a '0' for all other attributes. This method of encoding was selected to provide users/modellers with the option to isolate different TCP flags to determine if one flag on its own may be an indicator of a device's network behaviour. (Ullah et al., 2024) The relationship is also still retained if viewed together i.e. with a flow that has initialTCPFlags of AP, it would look like the following: 
          
        
      |initialTCPFlags_A|initialTCPFlags_P|initialTCPFlags_S |initialTCPFlags_R |	unionTCPFlags_A |unionTCPFlags_P |unionTCPFlags_S|	unionTCPFlags_R|
      |-----------------|-----------------|------------------|------------------|-----------------|----------------|---------------|-----------------|
      |  1 |	1	| 0 | 	0 | 1 |	1 |	0 |	0|
      
      This would mean this flow contains an Acknowledgement of received data and data was pushed immediately. See below for a further summary explanation of TCP flags.
<div align = 'center'>
    
**Summary of TCP Flags:**

|Flag |	IPFIX Value | Description |
|-----|-------------|-------------|
| SYN | S | Synchronize (start the connection)|
| RST |	R | Reset (abort the connection)|
| PSH |	P | Push (deliver data immediately)|
| ACK |	A | Acknowledgment of received data|

</div>

   *Note: Dropping of rows was the preferred method given the incredibly large dataset provided and as such could afford to drop.*

3. Data EDA: Exploration and analysis in preparation for feature extraction. (Note: feature extraction/selection has been descoped given group issues)
    ![image](https://github.com/user-attachments/assets/052c60d9-ec17-4834-82f6-2f0de3854444)


### _How to use_
Each of the following data folders contains the preprocessed data across the months data was collected (June 2019 - October 2019). Each with 25 CSVs corresponding with distinct device types that make up a merged data frame:
- data_clean_month_6
- data_clean_month_7
- data_clean_month_8
- data_clean_month_9
- data_clean_month_10

_Note: We have chosen to group our data in months given the collection of data has not been evenly distributed across the 5 months with the collection of the packet period being  25/6/2019 - 10/10/2019 (108 days)_

To replicate data preprocessing steps, first download the data from KDDI's git repo: https://github.com/nokuik/KDDI-IoT-2019 and ensure .json files are downloaded. For the Sony Bravia, Google Home Gen1 as tar gz has been used to split, use the cat command to combine the split files and extract the contents of the tar.gz files. Instructions are provided at the repo as well as further details at the following link: https://www.synopsys.com/apps/support/est/How_to_split_files_over_2GB.html. Next, refer to the data preprocessing file and ensure necessary libraries are run from the first cell. Check the current working directory contains the necessary files in a folder called final. Then scroll down to the "Final cleaning process" section where the preprocessing of the 25 device data has been split into multiple cells to accommodate for devices with RAMs lower than 8GB. Next, scroll down to the "Merge csvs" section and ensure all outputted CSV split by month are in the current working directory and run the necessary cells.

Alternatively,
1. Download the datapreprocessed_by_month.zip: Clone the zip from the current git repo by downloading the zip.
2. Open your terminal and navigate to the folder that contains the monthly subfolders.
```bash
cd /path/to/preprocesseddata_by_month
```
3. Merge CSV Files for Each Month:
Use the following command to merge all CSVs in each month:
```bash
for dir in data_clean_month_*; do
    cat $dir/*.csv > "$dir"_merged.csv
```
4. After you have merged the CSVs for each month, you can combine all the months into one CSV (Optional)
```bash
cat data_clean_month_*_merged.csv > merged_all_months.csv
```
This will produce a file called merged_all_months.csv containing data from all months.

### _Data Description_
*Observations (Rows):*
Each row represents a unique network session from an IoT device.

*Attributes (Columns):*
Each column consists of a unique attribute obtained from all the network sessions.

Some attributes are listed in two separate columns due to the bidirectional nature of each network session. Network traffic moves in both a forward and a reverse direction, detailing the interaction between the IoT device in question and a local network device. The forward direction explains the movement from the IoT device to the local network device, and vice versa for the reverse direction. For example, the forward direction for total packet count is under `packetTotalCount`, whereas the reverse direction is under `reversePacketTotalCount`.

Below are the list of all the attributes:

| Column Number | Attribute Name | Description |
|---------------|----------------|-------------|
| 1 | `flowDurationMilliseconds` | The total duration of the network session in milliseconds. It is calculated as the difference between flowEndMilliseconds and flowStartMilliseconds. |
| 2 | `reverseFlowDeltaMilliseconds` | The difference in time between the forward flow and reverse flow, potentially indicating latency or delay in bidirectional communication. |
| 3 | `protocolIdentifier` | A numeric code that identifies the protocol used in the communication (e.g., TCP, UDP). |
| 4 | `sourceIPv4Address` | IPv4 address of the IoT device. |
| 5 | `sourceTransportPort` | The port number on the IoT device that was used for the session. |
| 6 | `packetTotalCount` | Total number of packets sent/received during the session. |
| 7 | `octetTotalCount` | The total number of octets (bytes) transmitted in the flow. |
| 8 | `flowAttributes` | Encoded attributes that might provide additional details about the characteristics of the flow, such as direction, type, or QoS settings. |
| 9 | `destinationIPv4Address` | The IPv4 address of the device or server to which the IoT device is sending data, or from which it is receiving data. |
| 10 | `destinationTransportPort` | The port number on the destination device that is being used for the session. This could be a port commonly associated with certain services or protocols, such as port 80 for HTTP or port 443 for HTTPS. |
| 11 | `reversePacketTotalCount` | `packetTotalCount` but for the reverse direction. |
| 12 | `reverseOctetTotalCount` | `octetTotalCount` but for the reverse direction. |
| 13 | `reverseFlowAttributes` | `flowAttributes` but for the reverse direction. |
| 14 | `smallPacketCount` | The number of packets in the flow that were small in size (below 200,000). |
| 15 | `nonEmptyPacketCount` | The total number of packets in the flow that contained actual data (not empty). |
| 16 | `dataByteCount` | The total number of bytes of data (excluding headers) transferred in the flow. |
| 17 | `averageInterarrivalTime` | The average time between consecutive packets in the flow. |
| 18 | `firstNonEmptyPacketSize` | The size of the first packet in the flow that contains data. |
| 19 | `largePacketCount` | The number of large packets (above 200,000) transmitted in the flow. |
| 20 | `maxPacketSize` | The size of the largest packet transmitted in the flow. |
| 21 | `standardDeviationPayloadLength` | The standard deviation of the payload lengths of packets in the flow, indicating variability. |
| 22 | `standardDeviationInterarrivalTime` | The standard deviation of the time intervals between consecutive packets in the flow, indicating jitter or variability in timing. |
| 23 | `bytesPerPacket` | The average number of bytes per packet in the flow. |
| 24 | `reverseSmallPacketCount` | `smallPacketCount` but for the reverse direction. |
| 25 | `reverseNonEmptyPacketCount` | `nonEmptyPacketCount` but for the reverse direction. |
| 26 | `reverseDataByteCount` | `dataByteCount` but for the reverse direction. |
| 27 | `reverseAverageInterarrivalTime` | `averageInterarrivalTime` but for the reverse direction. |
| 28 | `reverseFirstNonEmptyPacketSize` | `firstNonEmptyPacketSize` but for the reverse direction. |
| 29 | `reverseLargePacketCount` | `largePacketCount` but for the reverse direction. |
| 30 | `reverseMaxPacketSize` | `maxPacketSize` but for the reverse direction. |
| 31 | `reverseStandardDeviationPayloadLength` | `standardDeviationPayloadLength` but for the reverse direction. |
| 32 | `reverseStandardDeviationInterarrivalTime` | `standardDeviationInterarrivalTime` but for the reverse direction. |
| 33 | `reverseBytesPerPacket` | `bytesPerPacket` but for the reverse direction. |
| 34-39 | `flowStartMilliseconds` | Time at which the session was first recorded. This has been parsed and the relevant features extracted into `flowStartMonth`, `flowStartDay`, `flowStartHour`, `flowStartMinute`, `flowStartSecond` and `flowStartMillisecond`. |
| 40-45 | `flowEndMilliseconds` | Time at which the session recorded ended. This has also been parsed and the relevant features extracted into `flowEndMonth`, `flowEndDay`, `flowEndHour`, `flowEndMinute`, `flowEndSecond` and `flowEndMillisecond`. |
| 46 | `device_type` | Type of IoT device (e.g., camera, thermostat). |
| 47-50 | `flowEndReason` | The reason the flow ended, which could be due to timeout, normal termination, or forced termination. This has been encoded into separate binary columns as `flowEndReason_Unknown`, `flowEndReason_eof`, `flowEndReason_active` and `flowEndReason_idle`. |
| 51-54 | `initialTCPFlags` | The flags set in the initial TCP packet, used to manage the state of the TCP connection (e.g., SYN, ACK). This has been encoded into separate binary columns as `initialTCPFlags_A`, `initialTCPFlags_P`, `initialTCPFlags_S` and `initialTCPFlags_R`. |
| 55-58 | `unionTCPFlags` | A combination of all TCP flags observed during the entire flow. This has been encoded into separate binary columns as `unionTCPFlags_A`, `unionTCPFlags_P`, `unionTCPFlags_S` and `unionTCPFlags_R`. |
| 59-62 | `reverseInitialTCPFlags` | `initialTCPFlags` but for the reverse direction. |
| 63-66 | `reverseUnionTCPFlags` | `unionTCPFlags` but for the reverse direction. |

### _Project Status_

Progress: Our data product has been finalised and output CSV files have been produced. Despite a reduction in team size and a need to quickly descope certain tasks, we successfully delivered a functional data product for IoT device classification. Key tasks, such as feature selection and preprocessing, were prioritized to meet the project deadlines.

Next Steps: Model training and evaluation are scheduled for Week 6 by the modelling team. Despite the delay, the preprocessed data product is as robust given the deadline and is ready for use in machine learning models. Feature selection and dimension reduction can be customized based on the final model choice.

### _Usage_
The data product is intended to be implemented to model the behaviour of IoT devices in a network, allowing for the classification of devices based on their network activity patterns. By analyzing parameters such as packet size and data flow characteristics, the product forms a set of common attributes of different IoT devices. These can be used to identify and categorize devices in real time, providing critical insights into device behaviour. Once integrated into network monitoring systems, this product enhances both security and management.

A simple analysis model for this data product could be built using supervised machine learning techniques, specifically a classification model. The goal is to classify IoT devices based on their network activity patterns, such as packet size and data flow characteristics, which are key indicators of device behaviour. A common algorithm for classification tasks would be a Random Forest or Support Vector Machine (SVM). These models handle high-dimensional data well and can classify complex behaviour patterns. Labelled data would then be used to train the model, which involves learning the patterns associated with different devices. For example, smart speakers might have frequent bursts of small data packets, while cameras may have larger packet sizes. The model can then be tested on a separate set of labelled data to evaluate its accuracy in classifying devices. (Li et al., 2024) 

Once trained, the model can be applied in real-time, analyzing incoming network data. By using information including packet size, flow duration, and other parameters, the model can classify the type of device and provide insights into whether the device is behaving as expected.

### _Support Information_

Please contact the contributors below on Teams if assistance is needed.

### _Contributors_
- Emma Gao
- John Papathanasiou
- Yipitihaer Abudureyimu (Michael)

### _References_
- Pashamokhtari, A. et al. (2021) ‘Inferring connected IOT devices from IPFIX records in residential ISP Networks’, 2021 IEEE 46th Conference on Local Computer Networks (LCN), pp. 57–64. doi:10.1109/lcn52139.2021.9524954. --(Pashamokhtari et al., 2021).
- Alani, M. (2021) Handling IP Addresses in Machine Learning Datasets, Mohammed M Alani. Available at: https://www.mohammedalani.com/tag/ip-address/ (Accessed: September 2024).
- Ullah, I. et al. (2024) ‘Integration of data science with the intelligent IOT (IIOT): Current challenges and future perspectives’, Digital Communications and Networks [Preprint]. doi:10.1016/j.dcan.2024.02.007.
- Li, J. et al. (2024) ‘Optimizing IOT intrusion detection system: Feature selection versus feature extraction in machine learning’, Journal of Big Data, 11(1). doi:10.1186/s40537-024-00892-y.
