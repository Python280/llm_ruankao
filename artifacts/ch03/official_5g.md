> 摘录自 官方教程[第二版] 官方 §17.2.3 移动通信网技术架构(5G) · 物理页 p622–626（印刷页=物理页−15）
> 原文照录，仅供浓缩；表格/图版式丢失，见原书对应页。

第17章通信系统架构设计理论与实践

17.2.3移动通信网网络架构

移动通信网为移动互联网提供了强有力的支持，尤其是5G 网络为个人用户、垂直行业等提供了多样化的服务。以下从业务应用角度给出面向5G 网络的组网方式。

1.5GS与DN互连

5GS(5GSystem) 在为移动终端用户(UserEquipment,UE) 提供服务时通常需要DN(DataNetwork) 网络，如Internet、IMS(IPMediaSubsystem)、专用网络等互连来为UE提供所需的业务。各式各样的上网、语音、AR/VR、工业控制和无人驾驶等5GS 中UPF网元作为DN的接入点。5GS 和DN之间通过5GS 定义的N 6接口互连。图17-11给出了5G 网络与DN网络连接关系图。SMF(会话管理功能)N6(UPF连接数据网接口)UE(用户设备)MG=RANUPF(接入网)(用户面功能)5GNetwork(5G网络)DataNetwork(数据网络)DHCP(动态主机控制协议)DNS(域名解析服务)图17-115G 网络与DN 网络连接关系如图17-11所示，5GNetwork属于5G 范畴，包括若干网络功能实体，如AMF/SMF/PCF/NRF/NSSF等。简洁起见，图中仅表示出了与用户会话密切相关的网络功能实体。在5GS 和DN基于IPv4/IPv6 互连时，从DN 来看，UPF 可看作是普通路由器。相反从5GS 来看，与UPF通过N 6 接口互连的设备，通常也是路由器。换言之，5GS和DN之间是一种路由关系。UE 访问DN 的业务流在它们之间通过双向路由配置实现转发。就5G 网络而言，把从UE流向DN的业务流称之为上行(UL,UpLink) 业务流；把从DN流向UE 的业务流称为下行(DL,DownLink) 业务流。UL业务流通过UPF 上配置的路由转发至DN ; DL业务流通过与UPF邻近的路由器上配置的路由转发至UPF。此外，从UE通过5GS 接入DN的方式来说，存在两种模式，即透明模式和非透明模式。

1)透明模式

在透明模式下，5GS 通过UPF 的N 6接口直接连至运营商特定的IP 网络，然后通过防火墙(Firewall) 或代理服务器连至DN (即外部IP网络) , 如Internet 等。UE分配由运营商规划的网络地址空间的IP地址。UE在向5GS发起会话建立请求时，通常5GS 不触发向外部DN - AAA服务器发起认证过程。图17-12给出了UE透明接入5G 网络的示意图。

N6(UPF连接数据网接口)5GS(5G系统)UPF(用户面功能)DHCP(动态主机控制协议)DNS(域名解析服务)Operator)specificIPNetwork(运营商特定的IP网络)Firewall/Proxy(防火墙/代理)ExternalIPNetwork(外部IP网络)图17-12 UE 透明接入5G 网络在此模式下，5GS至少为UE 提供一个基本ISP服务。对于5GS而言，它只须提供基本的隧道QoS 流服务即可。UE访问某个Intranet网络时，UE级别的配置仅在UE 和Intranet 网络之间独立完成，这对5GS而言是透明的。

2)非透明模式

在非透明模式下，5GS 可直接接入Intranet/ISP, 或通过其他IP 网络( 如Internet) 接入Intranet/ISP。如5GS 通过Internet方式接入Intranet/ISP, 通常需要在UPF 和Intranet/ISP之间建立专用隧道来转发UE 访问Intranet/ISP的业务。UE 被指派属于Intranet/ISP 地址空间的IP地址。此地址用于UE业务在UPF、Intranet/ISP 中转发。图17-13 (a) 和(b) 分别给出了UE通过5GS非透明接入DN和UE 的原理图。5GSUPFN6ISP/IntranetAppServer5GSUPFN6ExternalIPNetwork(e.g.Internet)ISP/IntranetAppServer(a) 直接接入(b) 间接接入图17-13 UE通过5GS非透明接入DN原理图综上所述，UE通过5GS访问Intranet/ISP的业务服务器，可基于任何网络如Internet等来进行，即使不安全也无妨，在UPF 和Intranet/ISP之间可基于某种安全协议进行数据通信保护。至于采用何种安全协议由移动运营商和Intranet/ISP提供商之间协商确定。作为UE会话建立的一部分，5GS 中SMF通常通过向外部DN - AAA 服务器( 如Radius、Diameter服务器) 发起对UE进行认证。在对UE认证成功后，方可完成UE会话的建立，之后UE才可访问Internet/ISP 的服务。2 . 5 G 网络边缘计算5 G网络改变以往以设备、业务为中心的导向，倡导以用户为中心的理念。5G 网络在为用户提供服务的同时，更注重用户的服务体验QoE(QualityofExperience)。其中5G 网络边缘计算能力的提供正是为垂直行业赋能、提升用户QoE 的重要举措之一。

第17章通信系统架构设计理论与实践5 G 网络的边缘计算(MobleEdgeComputing,MEC) 架构如图17-14所示，支持在靠近终端用户UE的移动网络边缘部署5GUPF 网元，结合在移动网络边缘部署边缘计算平台(MobileEdgePlatform,MEP), 为垂直行业提供诸如以时间敏感、高带宽为特征的业务就近分流服务。于是，一来为用户提供极佳服务体验，二来降低了移动网络后端处理的压力。运营商自有应用或第三方应用AF(ApplicationFunction) 通过5GS 提供的能力开放功能网元NEF(NetworkExposureFunction), 触发5G 网络为边缘应用动态地生成本地分流策略，由PCF(PolicyChargingFunction) 将这些策略配置给相关SMF , SMF 根据终端用户位置信息或用户移动后发生的位置变化信息动态实现UPF (即移动边缘云中部署的UPF ) 在用户会话中插入或移除，以及对这些UPF 分流规则的动态配置，达到用户访问所需业务的极佳效果。另外，从业务连续性来说，5G 网络可提供SSC模式1(在用户移动过程中用户会话的IP接入点始终保持不变), SSC模式2(用户移动过程中网络触发用户现有会话释放并立即触发新会话建立), SSC 模式3(用户移动过程中在释放用户现有会话之前先建立一个新的会话)供业务提供者ASP(ApplicationServiceProvider) 或运营商选择。MobileEdgeCloud(移动边缘云)ApplApp2ServiceService(应用服务1)(应用服务2)MEP(MobileEdgePlatform)移动边缘平台UE5G-AN5G接入网UPF(用户面功能AMF(用户设备)(接入移动性管理功能)TrafficFlow (toEdgeApp)业务流(到边缘应用)MobileCentralGloudPCFNET(策略控制(网络能力功能)开放功能)AF(应用功能)SMF(会话管理功能)MobileEdgeCloudApplApp2ServiceServiceUPF(用户面功能)CentralDN(中心DN)MEP(MobileEdgePlatform)UE5g-ANUPFTrafficFlow(toCentralApp)业务流(到中心应用)'图17-145G 网络边缘计算架构

6 1 0

17.2.4存储网络架构

一般来说，计算机访问磁盘存储有3种方式：

(1)直连式存储(DirectAttachedStorage,DAS): 计算机通过I/O端口直接访问存储设备的方式。

(2)网络连接的存储(NetworkAttachedStorage,NAS): 计算机通过分布式文件系统访问存储设备的方式。

(3)存储区域网络(StorageAreaNetwork,SAN): 计算机通过构建的独立存储网络访问存储设备的方式。DAS 采用I/O总线架构，如IDE 或ATA 等将存储设备挂接在计算机中，实现数据存储。多种存储设备适合用作主机连接存储；包括硬盘驱动器、RAID阵列、CD 、DVD 和磁带驱动器。对主机连接存储设备进行数据传输的I/O 指令是针对特定存储单元(例如总线ID和目标逻辑单元)的逻辑数据块的读和写。NAS 和SAN都是基于网络构建存储系统的。网络存储采用面向网络的存储体系结构，使数据处理和数据存储分离，由专门的系统负责数据处理，存储设备或子系统负责数据的存储。网络存储结构通过网络连接服务器和存储资源，具有灵活的网络寻址能力和远距离数据传输能力，实现了在单一区域或多个区域可靠的数据存储、恢复，以及不同主机不同存储设备之间的资源共享。

1.网络连接存储(NAS)

NAS 设备是一种专用存储系统，用户计算机NAS设施客户机通过数据网络(如LAN / WAN等网络)来远程访问。如图17-15所示，用户计算机通过远程过程调用(RPC) 访问NAS存储单元。远程过程调用是通过IP 网络(如基于TCP 或UDP ) 来进行的，NAS设施客户机LAN/WAN/5G等网络NAS 存储单元通常采用RPC 接口软件来实现。通图17-15  网络连接存储过NAS , 使得所有通过数据网络连接的计算机与主机本地连接存储一样方便命名和访问共享存储池。当然，与主机本地连接的存储相比，它的存储访问效率及性能相对较差。最常见的NAS协议以下：

(1)公共Internet文件服务/服务器消息块(CommonInternetFileServices / ServerMessageBlock,CIFS/SMB)。CIFS/SMB 是Windows 通常使用的协议。

(2)网络文件系统(NFS)。NFS 最早为UNIX服务器而开发，也是通用的Linux协议。

2.存储区域网络

存储区域网络(StorageAreaNetwork,SAN) 是一种基于块的存储，利用专用高速通信架构将服务器与其逻辑磁盘单元(LogicalDiskUnit,LDU) 相连。LDU是一系列通过共享存储池配置的块，以逻辑磁盘的形式呈现给服务器。服务器会对这些块进行分区和格式化，通常使用

第17章  通信系统架构设计理论与实践

文件系统，以便可以像在本地磁盘上存储一样在LDU上存储数据。此外，SAN的设计消除了单点故障，具有极高可用性和故障恢复能力。图17-16给出了SAN网络的部署示意图。存储设施服务器客户机存储设施SAN网络服务器LAN/WAN/5G等网络图17-16 SAN网络部署客户机SAN 是企业最常用的存储网络架构。SAN将数据存储在集中式共享存储中，使企业能够运用统一的方法和工具来实施安全防护、数据保护和灾难恢复。对高吞吐量和低延迟有需求的业务关键型应用尤为适用。SAN 为专用网络，采用存储协议而不是网络协议连接服务器和存储单元。SAN交换机允许或禁止主机访问存储，通过配置SAN来为主机提供所需存储容量。SAN可以让服务器集群共享同一存储，让存储阵列为多个主机提供存储服务。可见，SAN通信具有极大灵活性。常见的SAN有FC-SAN 和IP-SAN, 其中FC-SAN 为通过光纤通道协议转发SCSI协议，IP-SAN通过TCP 协议转发SCSI协议。最常见SAN 协议包括以下4种：

(1)光纤通道协议(FibreChannelProtocol,FCP)。应用最为广泛的SAN或块协议，FCP使用具有嵌入式SCSI命令的光纤通道传输协议。

(2)Internet 小型计算机系统接口(iSCSI): 第二大SAN或块协议。iSCSI 将SCSI命令封装在以太网帧内，然后使用IP 以太网络进行传输。

(3)以太网光纤通道(FibreChanneloverEthernet,FCoE): 其应用相对较少。它与iSCSI类似，将FC帧封装在以太网数据报中，然后像iSCSI一样使用IP 以太网络进行传输。

(4)基于光纤通道的非易失性内存标准(Non-VolatileMemoryExpressoverFibreChannel,FC-NVMe): 它是一种用于通过PCIExpress(PCIe) 总线访问闪存存储的接口协议。NVMe 支持若干并行序列，每一个序列又能支持若干并发命令。SAN 有着广泛的应用前景。SAN主要用于存储量大的工作环境，如ISP、银行等，特别地在5G 网络设备部署中得到应用。5G 网络设备通常采用业务处理和数据存储分离的架构进行设计，采用SAN存储网络可有效避免网元处理节点故障切换后业务数据丢失。

3.NAS 与SAN 异同点

SAN 和NAS都可以用于集中管理存储，并供多主机(服务器)共享存储。但是，NAS通常是基于以太网，而SAN可使用以太网和光纤通道。此外，NAS注重易用性、易管理性、可扩展性和更低的总拥有成本(TCO), 而SAN 则注重高性能和低延迟。实际应用中，应根据业务特点灵活选用适合的网络存储架构。