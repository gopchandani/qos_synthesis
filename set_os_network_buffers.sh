echo 'net.core.wmem_max=26214400' >> /etc/sysctl.conf
echo 'net.core.rmem_max=26214400' >> /etc/sysctl.conf
echo 'net.core.wmem_default=26214400' >> /etc/sysctl.conf
echo 'net.core.rmem_default=26214400' >> /etc/sysctl.conf
echo 'net.core.netdev_max_backlog = 5000' >> /etc/sysctl.conf
sysctl -p