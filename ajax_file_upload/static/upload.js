let progress = document.getElementById('progress')
let progress_wrapper = document.getElementById('progress_wrapper')
let progress_status = document.getElementById('progress_status')

let upload_btn = document.getElementById('upload_btn')
let loading_btn = document.getElementById('loading_btn')
let cancel_btn = document.getElementById('cancel_btn')

let input = document.getElementById('file_input')
let file_input_label = document.getElementById('file_input_label')

function show_alert(message, alert){
  alert_wrapper.innerHTML = `
    <div class="alert alert-${alert} alert-dismissible fade show mt-3" role="alert">
      <span>${message}</span>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  `;
};

function input_filename(){
  file_input_label.innerText = input.files[0].name;
};

function upload(url){
  if(!input.value){
    show_alert('No file selected', 'warning');
    return;
  }
  let data = new FormData();
  let request = new XMLHttpRequest();
  request.responseType = 'json';
  alert_wrapper.innerHTML = '';
  input.disabled = true;
  upload_btn.classList.add('d-none');
  loading_btn.classList.remove('d-none');
  cancel_btn.classList.remove('d-none');
  progress_wrapper.classList.remove('d-none');
  let file = input.files[0];
  let filename = file.name;
  let filesize = file.size;
  document.cookie = `filesize=${filesize}`;
  data.append('file', file);

  request.upload.addEventListener('progress', function(e){
    let loaded = e.loaded;
    let total = e.total;
    let percentage_complete = (loaded / total) * 100;
    progress.setAttribute('style', `width: ${Math.floor(percentage_complete)}%`);
    progress_status.innerText = `${Math.floor(percentage_complete)}% uploaded`;
  })

  request.addEventListener('load', function(e){
    if(request.status == 200){
      show_alert(`${request.response.message}`, 'success');
    } else {
      show_alert(`Error uploading file`, 'danger');
    }
    reset();
  })

  request.addEventListener('error', function(e){
    reset();
    show_alert('Error uploading file', 'danger')
  })

  request.addEventListener('abort', function(e){
    reset();
    show_alert('Uploaded cancelled', 'primary')
  })

  request.open('post', url);
  request.send(data);

  cancel_btn.addEventListener('click', function(){
    request.abort();
  })

};

function reset(){
  input.value = null;
  input.disabled = false;
  cancel_btn.classList.add('d-none');
  loading_btn.classList.add('d-none');
  upload_btn.classList.remove('d-none');
  progress_wrapper.classList.add('d-none');
  progress.setAttribute('style', 'width: 0%');
  file_input_label.innerText = 'Select File';
}