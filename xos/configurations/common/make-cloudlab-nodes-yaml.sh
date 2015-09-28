#FN=/opt/xos/configurations/common/cloudlab-nodes.yaml
FN=cloudlab-nodes.yaml

rm -f $FN

cat >> $FN <<EOF
tosca_definitions_version: tosca_simple_yaml_1_0

imports:
   - custom_types/xos.yaml

topology_template:
  node_templates:
    MyDeployment:
        type: tosca.nodes.deployment
    mysite:
        type: tosca.nodes.site
EOF

NODES=$( sudo bash -c "source /root/setup/admin-openrc.sh ; nova hypervisor-list" |grep cloudlab|awk '{print $4}' )
I=0
for NODE in $NODES; do
    echo $NODE
    cat >> $FN <<EOF
    $NODE:
      type: tosca.nodes.Node
      requirements:
        - site:
            node: mysite
            relationship: tosca.relationships.MemberOfSite
        - deployment:
            node: MyDeployment
            relationship: tosca.relationships.MemberOfDeployment
EOF
done
