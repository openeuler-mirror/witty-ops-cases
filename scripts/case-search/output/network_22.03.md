# 案例搜索结果

搜索时间: 2026-04-01T12:28:14.292819
找到案例数: 28

## [1] 920服务器安装openEuler系统因网络IO错误失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\920服务器安装openEuler系统因网络IO错误失败.txt`
**内核版本**: 22.03 SP3
**匹配字段**: title, content
**匹配次数**: 7
**预览**: 在920服务器上安装openEuler 22.03 SP3操作系统时，安装流程启动后无法正常加载安装源，报错显示访问ISO镜像时发生IO错误，导致安装失败。该问题在2025年9月23日首次出现，9月25日重试后安装成功。

## [2] 920B机型系统未按时重启导致网络不可达
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\920B机型系统未按时重启导致网络不可达.txt`
**内核版本**: 22.03 (LTS-SP4)
**匹配字段**: title, content
**匹配次数**: 5
**预览**: 在执行下电重启操作后，目标设备超过600秒无法通过ping连通；系统日志无明显报错；复现步骤为：SSH登录 → 发送下电指令 → 在其他节点持续ping目标IP → 超时未恢复连通。

## [3] MTU值异常波动导致网络不稳定
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\MTU值异常波动导致网络不稳定.txt`
**内核版本**: 22.03 SP4
**匹配字段**: title, content
**匹配次数**: 5
**预览**: 在天工HPC环境中，网络接口的MTU值在4192与1500之间反复切换，导致网络连接不稳定或中断。该现象可通过部署天工HPC环境后监控网络接口配置复现，在特定硬件或固件配置下更易出现。

## [4] dnf-makecache因网络超时失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\dnf-makecache因网络超时失败.txt`
**内核版本**: 22.03 LTS SP4
**匹配字段**: title, content
**匹配次数**: 4
**预览**: 系统在长稳压力测试中，定时任务执行dnf-makecache时失败，日志显示dnf-makecache.service报错“Curl error (28): Timeout was reached”；多次尝试访问https://mirrors.openeuler.org和http://repo.op...

## [5] PXE启动时GRUB下载内核超时卡住
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\PXE启动时GRUB下载内核超时卡住.txt`
**内核版本**: 22.03-LTS-SP4
**匹配字段**: content
**匹配次数**: 4
**预览**: 在PXE网络启动openEuler LiveCD过程中，GRUB自动倒计时结束后尝试从TFTP服务器下载`/84b89f08-.../vmlinuz`失败，报错“time out opening”，随后提示“you need to load the kernel first”，系统卡住，需通过串口人...

## [6] rc.local中ping死循环导致系统启动阻塞
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\rc.local中ping死循环导致系统启动阻塞.txt`
**内核版本**: 22.03-LTS-SP4
**匹配字段**: content
**匹配次数**: 4
**预览**: 系统启动过程中卡在rc.local脚本执行阶段，无法完成初始化；日志显示ping命令持续运行未退出；该现象在配备E810、XL710或82599网卡的服务器上偶发，与CentOS 9 Stream DHCP服务器配合时更易出现。

## [7] HPC现网GRUB阶段卡死问题
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\HPC现网GRUB阶段卡死问题.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 3
**预览**: 设备在启动安装过程中卡在GRUB引导阶段，无法继续进入系统安装流程；复现方式为正常上电启动安装介质后，系统在GRUB加载后无响应。

## [8] AC上下电循环测试中网口丢失
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\AC上下电循环测试中网口丢失.txt`
**内核版本**: 22.03 LTS SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: ...9.88.35.102）进行约200次AC上下电循环测试后，openEuler系统无法识别网卡设备，网络接口消失，导致网络功能中断。

## [9] dnf-makecache服务启动失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\dnf-makecache服务启动失败.txt`
**内核版本**: 22.03 LTS SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 在鲲鹏920Bs硬件平台上运行AC测试时，dmesg日志中出现“dnf-makecache.service: Failed with result 'exit-code'”和“Failed to start dnf makecache”错误信息。systemd无法成功执行dnf makecache命...

## [10] DNF元数据下载超时失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\DNF元数据下载超时失败.txt`
**内核版本**: 22.03 LTS SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 系统启动后通过定时器触发dnf-makecache.service服务，在尝试从http://71.41.15.160下载openEuler 22.03 SP4的repomd.xml文件时发生连接超时（Curl error 28），导致元数据缓存更新失败，dnf-makecache.service状...

## [11] dnf无法下载repo元数据
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\dnf无法下载repo元数据.txt`
**内核版本**: 22.03 LTS SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 在openEuler 22.03 LTS SP4系统上执行整机压力测试时，运行dnf命令（如dnf update）报错：“Error: Failed to download metadata for repo 'OS': Cannot download”。该错误导致软件包管理及系统更新功能不可用，复...

## [12] DNF缓存更新失败导致LDAP错误
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\DNF缓存更新失败导致LDAP错误.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 系统启动后，定时任务触发 dnf-makecache.service 服务更新DNF元数据缓存时失败。日志中记录以下错误信息：“ldapdb_canonuser_plug_init() failed”和“Failed determining last makecache time”。故障期间无法访问...

## [13] hisdk3网卡驱动通信失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\hisdk3网卡驱动通信失败.txt`
**内核版本**: 22.03 LTS SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: ...hannel detect, err: -110”，发生在设备0000:41:00.0上。该问题导致网络通信异常，可能引发网络中断或性能下降，在Kunpeng平台搭载TaiShan服务器并运行AC测试负载时可复现。

## [14] ipmitool读取FRU信息失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\ipmitool读取FRU信息失败.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 执行 ipmitool fru 命令后，返回“No data available”和“Get Device ID command failed”错误，无法获取FRU信息；该问题在天工HPC环境中可稳定复现，影响BMC通信及硬件管理功能。

## [15] numastat导致920C IO丢包
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\numastat导致920C IO丢包.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 在任子行920C设备上运行numastat命令时，业务进程nsdpf出现网络收发包性能下降甚至丢包；该现象在执行numastat期间可稳定复现，且与读取/proc/pid/numa_maps操作直接相关。

## [16] openEuler装机DHCP被动获取失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\openEuler装机DHCP被动获取失败.txt`
**内核版本**: 22.03-LTS-SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: 在openEuler 22.03 LTS SP4装机过程中，加载Kickstart配置阶段系统无法通过DHCP被动获取IP地址；手动执行dhclient命令可成功获取IP。问题复现与使用Intel E810、XL710及e40e网卡相关，且在缺少对应光交换机的家庭环境中难以完全复现。

## [17] Percona-server在openEuler与CentOS性能差异问题
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\Percona-server在openEuler与CentOS性能差异问题.txt`
**内核版本**: 22.03-LTS-SP4
**匹配字段**: content
**匹配次数**: 2
**预览**: ...二进制安装后存在性能差异（04-12反馈）； - 压测期间openEuler网卡流量更高，但调整内核网络参数无明显改善（05-09）； - 虚拟机集群测试结果相反（openEuler性能更优，05-14）； - 物理机单机压测使用客户my.cnf配置后，因前期未执行单机对比测试，导致结论不一致（05...

## [18] 网卡异常down掉问题
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\网卡异常down掉问题.txt`
**内核版本**: 22.03sp4
**匹配字段**: content
**匹配次数**: 2
**预览**: ...uler 22.03 SP4系统中，天工平台出现网卡无故异常down掉现象，端侧硬件正常；问题发生后网络连接中断，需手动重启网卡或系统方可恢复；该现象已在多台设备上复现，但具体复现步骤尚不明确。

## [19] CPU压力测试中Python3因repo源不可达报错
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\CPU压力测试中Python3因repo源不可达报错.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: 在鲲鹏硬件上运行CPU压力测试时，系统日志（/var/log/messages）记录“Nov 21 00:40:52 localhost python3报错”。复现行为为：启动CPU压力测试工具后，系统通过Python脚本尝试访问配置的软件仓库（repo源），因无法连接而触发异常，影响测试稳定性。

## [20] host3节点运行bwa时系统卡死
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\host3节点运行bwa时系统卡死.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: 在host3节点（IP: 29.204.23.112）运行bwa应用时，系统卡死无法响应；系统日志显示ccagent.service与batch-agent.service持续启动失败，重启次数超过1000次；服务启动参数包含“quiet”，导致缺乏详细错误信息。

## [21] iperf压力测试导致CPU占用率显示异常
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\iperf压力测试导致CPU占用率显示异常.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: 在鲲鹏硬件平台上执行iperf网络压力测试时，top工具显示CPU占用率偏低、看似处于idle状态，但实际CPU仍在处理大量网卡中断；通过对比CPU功耗可验证系统并非真正空闲；复现条件为将网卡中断绑定至CPU0的core1~core4，而系统64个核心均参与运行，造成资源冲突。

## [22] NFS客户端TCP重传延迟问题
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\NFS客户端TCP重传延迟问题.txt`
**内核版本**: 22.03 SP3
**匹配字段**: content
**匹配次数**: 1
**预览**: ...传约10秒，期间I/O操作出现卡顿或失败。可通过配置NFS高可用环境、触发服务端IP漂移并观察客户端网络行为及应用响应进行复现。

## [23] openEuler 22.03 SP1受CVE-2025-32462影响且无官方修复
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\openEuler 22.03 SP1受CVE-2025-32462影响且无官方修复.txt`
**内核版本**: 22.03sp1
**匹配字段**: content
**匹配次数**: 1
**预览**: 用户反馈openEuler 22.03 SP1系统受CVE-2025-32462漏洞影响；经确认，该版本已停止维护，官方未提供对应安全补丁；复现方式为通过比对系统版本与漏洞公告中的受影响版本列表，确认存在安全风险。

## [24] SYN Flood导致系统中断过高
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\SYN Flood导致系统中断过高.txt`
**内核版本**: 22.03-LTS-SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: ...并超出内核参数tcp_max_syn_backlog设定的队列上限，触发SYN Flood告警，导致网络处理性能下降。

## [25] X710网卡在Dell服务器上IP获取异常
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\X710网卡在Dell服务器上IP获取异常.txt`
**内核版本**: 22.03-LTS-SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: ...10网卡安装openEuler-22.03-LTS-SP4系统时，部分设备无法正常获取IP地址，导致网络连通性中断及系统安装失败；相同配置的另一台设备可正常通过LLDP获取IP。类似问题也出现在联想服务器上，而OCP E810网卡未出现该现象。

## [26] 伙伴侧内核升级后PXE引导失败
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\伙伴侧内核升级后PXE引导失败.txt`
**内核版本**: 22.03 SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: 在鲲鹏HPC服务器（项目：920F武超）上执行内核升级后，系统无法通过PXE正常引导启动。具体表现为：设备重启后在PXE引导阶段失败，无有效启动项，导致产线部署中断。该问题可稳定复现，复现步骤为：升级指定内核版本 → 重启设备 → PXE引导失败。

## [27] 双网卡路由冲突导致OS IP不通
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\双网卡路由冲突导致OS IP不通.txt`
**内核版本**: 22.03 LTS-SP4
**匹配字段**: content
**匹配次数**: 1
**预览**: 设备在reboot长稳测试中出现OS IP无法ping通，但BMC带内访问正常。现场环境配置了两个网卡IP并设置自动启动，网卡驱动加载顺序随机，导致路由表添加顺序不一致。当192.168.2.1所在网卡路由先加载时，其默认路由会覆盖9.88.60.1的路由，致使业务网段不可达。

## [28] 服务器软锁导致异常重启
**文件**: `D:\Git\witty-ops-cases-master\community_maintenance\服务器软锁导致异常重启.txt`
**内核版本**: 22.03 SP3
**匹配字段**: content
**匹配次数**: 1
**预览**: ...”，表明CPU 148长时间未响应调度。问题发生时系统负载正常，无明显外部触发因素，日志中加载了大量网络和昇腾相关内核模块（如mlx5_core、nf_log_ipv4等）。
