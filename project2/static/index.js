// Load initial web page
window.onload = () => {

    // Toggle modal if there is no username in localStorage
    if (!localStorage.getItem('username')) {
        console.log("No username in local storage!");
        $('#nicknameModal').modal('toggle');
    };

    // Load placeholder for chat
    console.log("No active channel is selected!")
    const div = document.createElement('div');
    div.className = 'empty';
    div.innerHTML = "No active channel is selected";
    document.querySelector('#content-area').append(div);
};

// Store username in localStorage
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#nicknameForm').onsubmit = () => {
        const username = document.querySelector('#usernameInput').value;
        localStorage.setItem('username', username);
    };
});

// Push username from localStorage to header
document.querySelector('#usernameHeader').innerHTML = localStorage.getItem('username');

// Ajax request for channel creation
document.addEventListener('DOMContentLoaded', () => {
   document.querySelector('#channelCreation').onsubmit = () => {

       // Initialize new ajax request
       const request = new XMLHttpRequest();
       const name = document.querySelector('#newChannel').value;
       request.open('POST', '/create_channel');

       // Callback function for when request completes
       request.onload = () => {

           const data = JSON.parse(request.responseText);
           if (data.success) {
                document.querySelector('#channelsList').innerHTML = '';
                let channel;
                for (channel of data.channels) {
                  const div = document.createElement('div');
                  div.className = 'channel';
                  div.innerHTML = `#${channel}`;
                  document.querySelector('#channelsList').append(div);
                }
                document.querySelector('#newChannel').value = '';
           }
           else {
                document.querySelector('#channelsList').innerHTML = data.error;
           }
       }

       // Add data to send with request
       const data = new FormData();
       data.append('name', name);

       // Send request
       request.send(data);
       return false;
   };
});

// Channels list navigation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.channel').forEach(channel => {
        channel.onclick = () => {
          document.querySelectorAll('.channel.active').forEach(channel => {
            channel.classList.remove('active');
          });
          channel.classList.add('active');
          document.querySelector('.empty').remove();
          document.querySelector('#content-area').append(channel.innerHTML);
        };
    });
});
