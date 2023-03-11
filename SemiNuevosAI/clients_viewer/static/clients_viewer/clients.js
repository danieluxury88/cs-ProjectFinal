 (function(){
     console.log("hi");
 })();

function testFunction(){
    console.log("Test1");
}

function disable_btn(val) 
{
    console.log(val);
}

function send_mail_btn(val) 
{
    console.log(val);
}

function contact_whatsapp_btn(val) 
{
    console.log(val);
}

function update_information(val) 
{
    console.log(val);
}

function register_response(owner_id) {
    showModalWindow( owner_id);
}

function showModalWindow( owner_id ){
    // Hidden type to save post_id when updating
    const ownerID = document.getElementById("owner-id");
    ownerID.value = owner_id;

    const myModal = new bootstrap.Modal('#modal_window', {
        keyboard: false
      }).show()
}


function registerContactState(){
    let modalContent = document.getElementById("modal_content_text_area_id");
    let ownerID = document.getElementById("owner-id");

    console.log("registerContactState",ownerID.value, modalContent.value);


    fetch(`/register/${ownerID.value}`, {
      method: 'POST',
      body: JSON.stringify({
          id: ownerID,
          content: modalContent.value,
      })
    })
    .then(response => response.json())
    .then(result => {
        // const postContent = document.getElementById(`post_content_${postNum}`);
        // postContent.innerHTML = modalContent.value;
        console.log(result);
    });


    modalContent.value = '';
}
