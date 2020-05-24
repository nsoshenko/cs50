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

// Initialize navigation for left menu
document.addEventListener('DOMContentLoaded', navigation());
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

               // Modify channels list
               const div = document.createElement('div');
               div.className = 'channel';
               div.innerHTML = `#${data.channel}`;
               document.querySelector('#channelsList').append(div);

               // Empty the input field
               document.querySelector('#newChannel').value = '';

               // Reinitialize navigation for left menu
               document.querySelector('DOMContentLoaded', navigation());
           }
           else {
                // document.querySelector('#channelsList').innerHTML = data.error;
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

// Channels list navigation function
function navigation() {

    document.querySelectorAll('.channel').forEach(channel => {
        channel.onclick = () => {
          document.querySelectorAll('.channel.active').forEach(channel => {
            channel.classList.remove('active');
          });
          channel.classList.add('active');
          // document.querySelector('.empty').remove();
          fetch_messages(channel.innerHTML);
        };
    });
};

function fetch_messages(channel) {

    // Initialize new ajax request
    const request = new XMLHttpRequest();
    const name = document.querySelector('.channel.active').value;
    request.open('POST', '/get_messages');

    // Callback function for when request completes
    request.onload = () => {

        const data = JSON.parse(request.responseText);
        if (data.success) {

          const template = Handlebars.compile(document.querySelector('#messages').innerHTML);
          const content = template({'messages': data.messages});

          document.querySelector('#content-area').innerHTML = content;
        }
        else {
             document.querySelector('#content-area').innerHTML = data.error;
        }
    }

    // Add data to send with request
    const data = new FormData();
    data.append('channel', channel);

    // Send request
    request.send(data);
};
