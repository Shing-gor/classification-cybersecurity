# Modelling the identification and behaviour of IoT devices

# Project description
Within the next few years, major technological trends will shape how we interact with our world, one of which is the development and presence of IoT. According to research provider IoT analytics, there were 16.6 billion connected devices at the end of 2023 with a predicted growth of 13% to 18.8 billion by the end of 2024[1]. But unfortunately IoT devices typically lack the required built-security to counter cyberattacks which means that there has also been an increasing number of cyberattacks with the organisation EC Council reporting that “In 2022, there were approximately 112 million IoT cyberattacks, up from about 32 millions in 2018”[2]. Such cyberattacks are usually done with malicious intent resulting in a slew of problems including the interruption and damage of IoT devices, unauthorised access, and the loss of privacy over data theft. 

Hence our primary objective in this project is to characterise the behaviours of said IoT devices using the data provided. We do this in the hopes that the ISP will have device visibility, that is the detection and classification of these devices within their network when they analyse their network flow. By developing a model that enables us to identify the normal behaviour of an IoT device, ISP can use it to define what is considered to be normal activity for an entity given their network of IoT devices. This is important as network visibility is integral to cybersecurity with a technique known as anomaly-based threat detection. Past research indicates that when an IoT device is infected, the data it sends may exhibit abnormalities such as increased volume hence enabling the ISP to distinguish it from its normal behaviour and flag it for  cyberattack. 




## Sources
The data product is built using the KDDI-IoT-2019 dataset, which contains network traffic records from 25 different IoT devices. These devices include smart speakers (like Amazon Echo and Google Home), network cameras, smart locks, TVs, and other smart home devices.


The dataset was created by capturing network packets (PCAP files) over a 108-day period (June 25, 2019, to October 10, 2019). These raw packets were then converted into IPFIX records using two tools:


YAF to convert PCAP files to IPFIX format.


Super Mediator to convert IPFIX binary files into JSON format for easier analysis.


Each IPFIX record contains information such as the source and destination IP addresses, MAC addresses, packet counts, data volume, and timestamps, giving a detailed view of the communication between IoT devices and other systems. The data also captures both the outgoing and incoming traffic, allowing analysis of the full network flow.


In summary, the dataset provides a comprehensive look at how IoT devices communicate over the network, making it ideal for analyzing traffic patterns and security.



## Workflow
The complete analysis process is done in Python and Alteryx, and the original code is written as a step-by-step process code. First, we need to read the original data file, and read the compressed file through the code.

The initial task is to process the irregular JSON format data provided. Using Python, we convert each line of the original JSON data into a structured format, specifically CSV, which is more suitable for further analysis.

For further analysis, we used Alteryx, a visual data processing tool, to efficiently handle the structured CSV files. This tool allows for quick merging, filtering, and cleaning of large datasets.

 Step 1: Combine all device data into a unified dataset, merging similar fields and ensuring consistency across files.
 
 Step 2: Filter out Internet of Things (IoT) devices by identifying their macaddress. We extract these addresses from the data and create a new column combined_macaddress that holds the merged addresses.
 
 Step 3: Filter TCP data, ensuring that tcp values are non-null, as required for analysis. This is done by identifying records where protocolidentifier = 6 (indicating TCP) and removing null values in tcpurgcount. For udp values, since they can be null, no such restrictions are imposed, and null values in udp (protocolidentifier = 12) are handled appropriately.
 
Next, we extract and engineer important features for analysis:

  IP Address Feature: We identify IPaddress based on whether the device is remote:
  
    If the remote device acts as the destination, it is labeled as Destination IPaddress.
    
    If the remote device acts as the source, it is labeled as Source IPaddress.
    
  Timestamp Processing: The original timestamp format is unsuitable for analysis, so we reformat the time data, splitting it into year, month, day, and second components. Additionally, we calculate the time difference in milliseconds between data transmission and reception to allow for better time-based analysis.

After reading the text, we performed a statistical analysis of the file content through Python. The purpose of the analysis is to view the format of the data and the proportion of the numerical distribution. Through the proportion of the distribution, we can further clarify the clear steps, including visualization steps and other related steps.

After the features are completed, modeling can be performed. This step includes training and verifying the model using training data and features, mainly to verify the effect of the model. At the same time, we also need to compare the performance of different models, such as using regression models or other classification models, and finally select the model with the best performance.

Therefore, this workflow mainly includes the complete modeling process, covering all steps of data reading, visualization, statistical analysis and modeling. The whole process can analyze, count and model the raw data in turn, and the main libraries used include pandas, matplotlib, seaborn and scikit-learn.

### Timeline:
As a summary, our scheduled timeline follows as: 

#### Week 1:
Understand what primary objective the organisation KDDI wanted from this project as well as researching industry knowledge relevant to our work including terminology and how the environments of IoTs worked

#### Week 2: 
Exploring our data and its features as well as further research in terms of past relevant papers

#### Week 3: 
Performed basic EDA with relation to our objectives. This included finding and cleaning data for missing and null data. Composed a draft readme file ready for feedback by peers

#### Week 4: 
Implemented feature engineering to create new usable variables. Read and implemented feedback given by peers and supervisors into final readme file so that it can be ready next week

#### Week 5: 
Present final readme file that has been checked by all members and fix any mistakes within the readme and dataframe so it can be ready to model

#### Week 7 - 9: 
Create a model that allows ISPs to accurately identify IoT devices within their network and be ready to present research in week 10 as well as being able to answer any questions if asked

#### Week 10 - 11: 
Write up a modelling report to be handed in at week 11


## Data Description
### Overview
The dataset utilized is the KDDI-IoT-2019, containing IP Flow Information Export (IPFIX) records from 25 IoT devices, collected over 108 days (June 25 to October 10, 2019). Each record represents a network traffic flow generated by an IoT device, useful for analyzing traffic patterns, device behavior, and security vulnerabilities.
### Observations
The dataset contains 24 million rows, each representing a unique network flow, a communication session between devices. Each flow includes timestamps, IP addresses, and packet counts, offering insights into the data transfer between devices. An example flow from an Amazon Echo Gen 2 device to a remote server includes details like 18 sent packets and 17 received.


### Data Processing and Software Tools：

（1）
Regarding the format of the data, the final output will be in CSV format. To access and process the data, we recommend using Alteryx, a visual data processing software that offers significant convenience when managing large datasets. This software allows for the customization of formulas and the ability to perform data cleaning and deletion tasks efficiently.

All data processing in our project is conducted using Alteryx. The software provides a user-friendly interface, enabling users to access and review code visually. Alteryx is developed using Python and SQL, making it a powerful tool for data manipulation and analysis. Furthermore, student accounts are eligible to use Alteryx free of charge, providing a cost-effective solution for data processing needs.

（2）
The second issue identified relates to the volume of data generated during the start of communication by IoT devices. Specifically, the IoT device communication initiation process involves approximately 6,985,596 lines of data. In comparison, the non-I/O device start function generates 2,690,000 lines. These lines contain detailed records of the transmission process across different devices
The data includes information about the transmission protocol, which is typically carried out via UDP or TCP, and records the IP address and MAC address of the transmitting device. Additionally, the data captures information regarding transmission times. This detailed information enables the identification of patterns, differences, and characteristics across devices during the transmission of data, providing insights into their behavior and communication processes.

（3）
There are several important columns, such as flow duration time, and the identifier used to distinguish whether it's TCP or UDP transmission. Additionally, there is the port number from the raw data, the packet total count, the network segment, and some converted values. Of course, some address information is also important for identifying the type of device or the method of transmission and reception.


### Summary
The dataset provides rich insights into IoT network behavior with ~24 million rows and over 10 key features. Preprocessing steps ensure data privacy and consistency, making it ready for robust analysis to detect patterns, anomalies, and improve IoT network security.








## Project Status

We are currently in the middle stages of the project, having completed the data frame and developed a preliminary understanding of the dataset and its objective. What we do include

### Project Definition and Setup:
The project description and objectives have been clearly outlined, focusing on identifying and modelling IoT device behaviour using the KDDI-IoT-2019 dataset. The necessary repositories for collaboration within Github Data 3001 have been set up.

### Data Familiarization and modification:
The team has performed an initial review of the dataset, which includes network traffic records from 25 IoT devices over a 108-day period. The structure of the dataset, including key features such as IP addresses, MAC addresses, packet counts, and timestamps have been identified. We have also cleaned and modified the data frame such as creating new columns as well as handling null values so that it can be modelled much easier.

### Next Steps:
Given the data frame, other parties’ focus should now be upon the training and testing of a model to address the primary objective of Iot device identification. Following this, they should now be getting prepared to present their findings as well as creating a report based upon their modelling. 

### Challenges:
As the dataset is large, managing its size efficiently during modelling will require attention. Developing a clear timeline is pivotal given the short timespan to be ready to present as well as a full bodied report one week after.





## Usage
This project aims to use the data product in the form of a data frame  to create a model that can help ISPs such as KDDI to attain network visibility. The model should be able to accurately identify IoT devices within their network based on traffic data that the ISP receives post-NAT. This then can be used to perform anomaly-based threat detection which helps in detecting if there are cases of cyberattacks within their network as well as improving their cybersecurity as a whole. 

Within the data frame, contains labelled data such as sourceMACAddress ideally, this should only be used within the testing phase to determine accuracy and not used when training the model as an ISP cannot attain this data post-NAT. Given the data’s nature and number of variables, it is ideal to either use an random forest model as it is effective for classification as well as being able to handle non linear relationships as well as K-Means clustering given its process to group similar traffic flows together.







## Support information
For support regarding course or assessment information please contact our supervisor Gustavo Batista at:

g.batista@unsw.edu.au



For support regarding general information or have an inquiry with the dataframe please contact us at:

Kelvin Yu - z5361555@ad.unsw.edu.au

Haowen Shi -  z5454779@ad.unsw.edu.au



## Contributors
Kelvin Yu: Project description, Workflow, Project Status, Support information, Usage


Haowen Shi: Data cleasing, Coding



Haozhe Zhu: Workflow, Sources




Yikang Qiu: Data Description, Sources

## References
[1] Satyajit,S.(2024). State of IoT 2024: Number of connected IoT devices growing 13% to 18.8 billion globally. IoT Analytics. https://iot-analytics.com/number-connected-iot-devices/#:~:text=Number%20of%20connected%20IoT%20devices%20to%20grow%2013%25%20by%20end,by%20the%20end%20of%202024

[2] Shekhar,P.(2024). The Rise of IoT Attacks: Endpoint Protection Via Trending Technologies. EG-Council. https://www.eccouncil.org/cybersecurity-exchange/ethical-hacking/the-rise-of-iot-attacks-endpoint-protection-via-trending-technologies/#:~:text=The%20rise%20in%20IoT%20attacks,about%2032%20million%20in%202018
