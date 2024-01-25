const socket = io('http://lotus1104.synology.me:83'); // Replace with your actual Socket.io server URL

socket.on('connect', () => {
  console.log('Connected to server');
  socket.emit('SOCKET',{"topic":"WSN_GW_01C823","message":"ABC"}); // Request initial status from server on connect
});

socket.on('update_status', (status) => {
  // Update the status of nodes based on received status
  updateNodeStatus('Node1', status.node1);
  updateNodeStatus('Node2', status.node2);
  updateNodeStatus('Node3', status.node3);
});

function updateNodeStatus(nodeName, isActive) {
  const nodeElement = document.getElementById(nodeName);
  if (isActive) {
    nodeElement.classList.add('active');
    nodeElement.classList.remove('inactive');
  } else {
    nodeElement.classList.add('inactive');
    nodeElement.classList.remove('active');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Initial status setup
  updateNodeStatus('Node1', false);
  updateNodeStatus('Node2', true);
  updateNodeStatus('Node3', true);
  
  // Periodically send update status request
  setInterval(() => {
    socket.emit('update_status_request');
  }, 60000);
});
