
# Characterising IoT devices according to their IPFIX records



## **Project Description**  

The specific objective of this project is to create a data frame from which different Internet of Things (IoT) devices are able to be identified from their flow using features such as the flow duration, packet count and octet count. IoT devices are devices that are able to connect to the internet and exchange data with other devices and systems via sensors, software and other technologies. From the KDDI-IoT-2019 dataset provided, some of the IoT devices which will be classified in this project include smart speakers, network cameras, lights and remote controllers, but more information about the dataset will be provided in the Sources section. There are several reasons why being able to identify different IoT devices from their records is important, with security being the main concern. By analysing the records of an IoT device, the risk level of different IoT devices can potentially be assessed, however, currently with the data that is provided, only classification of different IoT devices is possible. 

Previous work on this problem include identifying IoT devices via collecting Mac addresses, collecting IP flows to identify properties of network attacks, and by conducting surveys to collect large amounts of traffic data (Okui et al., 2022). This project is related to previous works in the sense that features of different IoT devices will be collected for modelling, however features such as the IP addresses and Mac addresses will not be involved in the modelling process. To be more specific, although Mac addresses and IP addresses will be provided in the data frames, they must not be included in the model because the objective is to identify IoT devices via traffic flows. Mac addresses can be helpful in filtering out different devices for modelling, however can lead to overfitting in models if included, while IP addresses should not be used in the models as they can change when using the model to predict the presence of devices in a different home network. 

It is to be noted that there are many IoT devices that reach millions of observations, therefore it is necessary to split the data files first in order to read them in such cases and it will have been done so in the data provided. Consequently, the data frames are provided in periods of 5 months, and it has been decided that those modelling the data will be given the freedom to decide whether every month and feature is relevant to the model. They must also take into consideration that not every month has the same amount of observations. Furthermore, some observations may have missing values. Therefore, a new is_missing column has been added in the data frames provided which signals TRUE when there is at least one missing value for that observation, and FALSE otherwise. With this information, the modelling team can choose to filter out the columns with missing values or keep them if there are not enough observations with no missing values, because for some devices such as the Nature Remo, most of the observations have at least one missing value. 

## **Sources**

The data sources used to construct this product are a set of IPFIX records collected by research from the Japanese telecommunication company KDDI over 108 days and 5 months in 2019 from 25 different IOT devices ranging from light bulbs to smart speakers. IPFIX, or IP Flow Information Export, is a "standard protocol for transmitting IP flow data from network devices" (Pashamokhtari et al., 2021). Essentially, what these records capture are the details of the flows of different devices, and the data from IPFIX allows for analysis and monitoring of the networks. Many features are included in the records, but as mentioned in the Project Description, some features such as the Source/Destination Mac Address and Source/Destination IP Address should not be included for modelling. However, some of the key properties captured in the IPFIX records that should be included in modelling include flow duration, packet and octet (byte) count, protocol identifier and small/large packet count.

### Protocol Identifier: 

Identifies what protocol (how data is transmitted and communicated between devices over a network) is being used. Examples of identifiers are 6 for TCP and 17 for UDP. 

### Packet and octet count: 

The number of packets exchanged during the flow and the overall number of bytes transmitted in the flow from the source to the destination. A packet contains bits of information known as bytes, and a flow is a communication of this information between devices. The more information a device has to send, the more packets are observed.

### Flow duration: 

Duration of the flow. Some devices will have a longer flow duration compared to others. For example, a TV will naturally have a longer flow duration on average than a door lock. 
Small/large packet count: How many small or large packets are counted in a particular observation. 

### Bytes per packet: 

How many bytes per packet are being sent over the network. Generally, more bytes per packet means more information is being sent. 

With observations such as packet and octet count and bytes per packet, there is an additional observation which is just the same but reverse, meaning that the flow is now from the destination to the source. These should also be included in the model as they are still flows transmitted over the network.

Finally, the classes of each device is shown in the table below:

### Smart Speaker
Amazon Echo gen2

Google Home gen1

Line Clova Wave

Sony smart speaker

### Network Camera
au network camera

I-O Data QWatch

JVC Kenwood HDTV IP camera

PLANEX camera one shot!

PLANEX SmaCam Outdoor

PLANEX SmaCam PanTilt

Sony network camera

### IoT Gateway/Hub
au wireless adapter

JVC Kenwood CU-HB1

Mouse computer room hub

### Environment Sensor
Bitfinder Awair Breathe Easy

### Door Lock
CANDY HOUSE Sesami Wi-Fi access point

Qrio Hub

### Robot Cleaner
iRobot Roomba

### Remote Controller
Link Japan eRemote

Nature Remo

### Doorphone
Panasonic Doorphone

### Light
Philips Hue Bridge

Xiaomi Mijia LED

### Plug
PowerElectric Wi-Fi plug

### TV
Sony Bravia


## **Workflow**

### Data processing steps:

First, all the compressed files (e.g..tar,.gz,.tar.gz) are extracted to the specified directory. The tarfile module automatically detects the type of the compressed file and extracts its contents into the target folder, ensuring that all data can be processed later. The purpose of this step is to extract all the original data files from the compressed package to facilitate further data cleaning and conversion. Next, for those compressed files that have been split into multiple parts (e.g.,.tar.gz 00,.tar.gz 01), we use the shutil library to merge these file parts into a complete compressed file. After the merge is complete, the tarfile module is used to decompress, which ensures that all split files are properly processed and converted into usable complete data.
After the data has been extracted and merged, the extracted JSON file is then read and converted to CSV format. Since these files can be very large, reading them directly can cause memory overflow. Therefore, we use the pandas library chunksize parameter to read JSON files in chunks. In this way, we can divide large files into small chunks for processing, thus effectively avoiding memory problems. When the JSON file is read, we use the pd.json_normalize() function to flatten the nested structures (such as the 'flows' field) into table format. This process converts complex JSON data into a more analyzable CSV format for subsequent data modelling and processing. 
Finally, we split each generated CSV file by month according to the value of the flowStartMilliseconds column. First, we convert the timestamp of the column to a readable date-time format. The data is then grouped by month using pandas' groupby method based on the transformed date-time information. For each month grouping, we save the data separately as separate CSV files. This monthly division of data facilitates subsequent analysis or modelling based on time series and provides data users with a more flexible way to use data.

### How the user accesses the code:

Users can access the full code and related documentation by visiting the project's GitHub repository. In this warehouse, all steps are well documented and explained. Users can repeat these processing steps from source data by simply downloading the relevant code, installing the necessary dependency libraries (pandas, tarfile, shutil, etc.), and following the instructions to run the code. The whole workflow is modular, and users can choose to run part or all of the process according to their own needs. In addition, there is detailed documentation on how to adapt the code to help users work with other similar types of data sets.With these steps, users can easily extract, process, and convert large-scale JSON data into CSV files split by month for further analysis. If you need to know more about specific steps, or have questions about the code, you can refer to the detailed documentation in the repository, or use the contact information provided for support.

## **Data Description**

### How the data frame is accessed, what its format is

The data frame can be accessed in any major programming language, as it is stored in comma-separated values (.csv) format. The csv files are all panel datasets in a tabular format with rows and columns which are filled with either numerical or categorical variables. As the volume of the data was exceptionally large, we have decided to divide the datasets according to individual devices. Within the datasets, we have also separated each set by the numerical index of the month in which the data was collected. In the data.csv folder uploaded on Github, .csv files containing monthly data that exceeded 25MB were also split, and all datasets have been compressed as .zip files. 

Collection started on 25/06/2019 and ended on 10/10/2019, spanning a 108 day period. Consequently, datasets containing June and October’s observations are considerably fewer than sets from July to September which contained a whole month’s worth of observations.


### How many observations (rows) are there and what do they represent

There are 23,089,118 total observations across 25 IoT devices, of which there are 11 different classes. The device with the least observations is the Mouse computer room hub with 16,932, and the device with the most observations is the Google Home gen1, with 6,142,846 observations. Each observation will display the IP Flow Information Export (IPFIX) records of the device at the given timestamp. 

### Its features and what they represent, and how they were constructed

For a given IPFIX record or observation across all devices, there are 55 columns, the top of which will describe a particular property of the IPFIX record. Some columns have a large number of missing values, which can be retained or omitted from the dataset completely. 

There are several data types which make up the variable features of the dataset. These have been categorised below,

### Numerical
[5] "protocolIdentifier"
[6] "sourceIPv4Address"
[7] "sourceTransportPort"                     
[8] "packetTotalCount"                        
[9] "octetTotalCount"
[11] "sourceMacAddress"                        
[12] "destinationIPv4Address" 
[13] "destinationTransportPort"                
[14] "reversePacketTotalCount"                 
[15] "reverseOctetTotalCount"
[17] "destinationMacAddress" 
[22] "tcpSequenceNumber"                       
[23] "reverseTcpSequenceNumber"
[28] "ipClassOfService"
[31] "observationDomainId" 
[32] "tcpUrgTotalCount"                        
[33] "smallPacketCount"                        
[34] "nonEmptyPacketCount"                     
[35] "dataByteCount"
[36] "averageInterarrivalTime"                 
[37] "firstNonEmptyPacketSize"                 
[38] "largePacketCount"                        
[39] "maxPacketSize"
[41] "standardDeviationPayloadLength"
[42] "standardDeviationInterarrivalTime"      
[43] "bytesPerPacket"                          
[44] "reverseTcpUrgTotalCount"                 
[45] "reverseSmallPacketCount"                 
[46] "reverseNonEmptyPacketCount"              
[47] "reverseDataByteCount"                    
[48] "reverseAverageInterarrivalTime"          
[49] "reverseFirstNonEmptyPacketSize"          
[50] "reverseLargePacketCount"                 
[51] "reverseMaxPacketSize"                    
[52] "reverseStandardDeviationPayloadLength"   
[53] "reverseStandardDeviationInterarrivalTime"
[54] "reverseBytesPerPacket"                   
[55] "is_missing" 

### Categorical
[18] "initialTCPFlags"                         
[19] "unionTCPFlags"                           
[20] "reverseInitialTCPFlags"                  
[21] "reverseUnionTCPFlags"
[29] "flowEndReason" 
[30] "collectorName"
[40] "firstEightNonEmptyPacketDirections"

### Binary
[10] "flowAttributes"
[16] "reverseFlowAttributes"
[24] "ingressInterface"                        
[25] "egressInterface" 

### Date/Time
[1] "flowStartMilliseconds"                   
[2] "flowEndMilliseconds"                     
[3] "flowDurationMilliseconds"                
[4] "reverseFlowDeltaMilliseconds"

Additionally, many columns contain missing values and some almost solely zero entries. For example, we created RStudio code uploaded to the Github repository to detect columns which contained half or more missing values. This was performed on an example dataset for the “au_network_camera” device, taking June’s observations. It was found that one-fifth of the columns’ observations were missing values. 
These columns have been left in the dataset intentionally in case this information is found to be useful, however, the provided code is able to be replicated and columns can be deleted appropriately by adjusting the threshold to a larger interval or smaller interval as preferred.

## Usage

The intended usage for this product describes the optimal method of classifying the IoT devices given their IPFIX records. To correctly identify each IoT device with a high-level of precision,  a multi-class classification model is recommended as a suitable modelling technique for this purpose. Before constructing the classification model, it is recommended that the data is trained and tested at an appropriate ratio. 

The k-fold cross-validation technique can be used for this purpose, but cannot be used cross-sectionally as it cannot be used with validity across time periods as it fails to account for time-variant numerical and categorical variation in the data. Thus, a time-series oriented approach is recommended for the cross-validation.


A recommended classification model for this task is a decision tree which takes features of the dataset and characterises it by its categorical or numerical properties. After constructing the decision trees, each decision tree should effectively be able to identify each device by its properties to a certain extent. Given the volume of the data, however, and the logistic difficulties of the null-classification problem, the machine learning algorithm will have a certain degree of imprecision. This means that on occasion, the algorithm will classify a device incorrectly, reducing its precision. Precision is calculated by the equation,

Pr_i = TP/(TP+FP)

and average precision can be calculated also,

Pr_average = 1/n sum(i=1 to n) Pr_i
 
where Pr indicates precision and TP denotes true positives, i represents each class of device, and FP denotes false positives. In order to find the optimal predicting model, performing k-fold cross-validation with varying values of k and a varying time window is a possible method to see which sample size performs best (Okui et al., 2022).

After the decision tree reaches the leaf node, the classification will have a given precision which is a ratio of correct classifications divided by the total classifications correct or incorrect. There is a slight problem with this approach, which is that for very low values, the classification is likely to be inaccurate as it is not representative of the whole population. This is because with each classification, the model is only able to classify each device at a certain percentage of confidence, so there can be room for error depending on the degree of confidence that the model accepts. 

A dynamic solution to this problem was conducted in past research into this topic area by Okui et. al (2022), where a classification model used a threshold value to filter out values. The threshold value for the individual class represented by i was calculated as follows,

Threshold_i  = s_mean_i - 2i

where the threshold minimum value is calculated by subtracting 2 times the standard deviation from the mean value for the class. The statistical reasoning for this approach comes from the idea that 2 standard deviations below the threshold value is outside the lower bound of the 95% confidence interval and is likely to be more of a hindrance to the actual classification of the devices. In this case, values below the threshold should be dropped, and values at threshold or above should be kept. This method was found to significantly increase precision by 13.2%.

As such, the focus for the null-classification is advised to be directed towards maximising the precision of the classification process at any scale, because a model that can perform the correct classification at an extremely high precision with a small sample size is to be preferred over a less precise model that predicts for the whole population. 

## **Support Information**

For questions regarding the preprocessing of the data, email the contributors at z5437887@ad.unsw.edu.au (Jeffry), z5416495@ad.unsw.edu.au (Aidan), or z5377408@ad.unsw.edu.au (Zhengdong). For questions relating to the dataset itself, contact the proxy industry representative Dr. Hassan Habibi Gharakheili at h.habibi@unsw.edu.au.  

## **Contributors**

The dataset was provided by KDDI Corporation. The contributors for this project were Aidan Odenthal (z5416495@ad.unsw.edu.au), Jeffry Kwak (z5437887@ad.unsw.edu.au) and Zhengdong Li (z5377408@ad.unsw.edu.au).

### **Breakdown**

For this data product, tasks for completion were divided proportionately amongst its members. The roles were divided as follows,

Aidan organised the delegation of tasks, conducted research into past modelling techniques used related to the objective of the project, and was responsible for writing the data description and usage section of this data product.

Jeffry assisted with the delegation of tasks, conducted research into the features and important variables of the dataset, and was responsible for writing the project description and sources section of this data product.

Zhengdong implemented the preprocessing of the data, which included decompressing and merging the datasets, converting them into csv format and splitting each dataset by month. He was also responsible for writing the workflow section of this data product.

Each member worked initially to identify patterns and characteristics of the dataset in class time, with industry representatives and through their own inspection of the data.

## **References**
Norihiro Okui, Nakahara, M., Miyake, Y., & Kubota, A. (2022). Identification of an IoT Device Model in the Home Domain Using IPFIX Records. 2022 IEEE 46th Annual Computers, Software, and Applications Conference (COMPSAC). https://doi.org/10.1109/compsac54236.2022.00104

‌‌Arman Pashamokhtari, Norihiro Okui, Miyake, Y., Nakahara, M., & Hassan Habibi Gharakheili. (2021). Inferring Connected IoT Devices from IPFIX Records in Residential ISP Networks. https://doi.org/10.1109/lcn52139.2021.9524954











