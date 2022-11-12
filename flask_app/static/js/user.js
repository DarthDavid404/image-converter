var input = document.getElementById('file')
var acceptable_inputs = ['jpg','png','webp']

function show_file() {
    
    var fileTypeIn = input.value.split('.').pop()
    
    if (acceptable_inputs.includes(fileTypeIn)) {
        
        var element = document.getElementById("file_name");
        element.classList.remove("redText");
        document.getElementById('file_in').value = fileTypeIn
        document.getElementById('file_name').innerHTML = input.value 
        var element = document.getElementById("file_box");
        element.classList.remove("hide");
    }

    else {

        document.getElementById('file_name').innerHTML = input.value
        document.getElementById('file_in').value = ''
        var element2 = document.getElementById("file_box");
        element2.classList.remove("hide");
        var element3 = document.getElementById("file_name");
        element3.classList.add("redText");
    }
};



function upload(url) {

    var fileTypeIn = input.value.split('.').pop()

    if (acceptable_inputs.includes(fileTypeIn)) {
        var data = new FormData();
        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log('should appear here')
                console.log(this.response)
                
                
                var download_file = new XMLHttpRequest();
                download_file.open('get', 'http://localhost:5000/download_file');
                download_file.send();

                download_file.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById('upload-button').classList.add('hide')
                        document.getElementById('download').classList.remove('hide') 
                        document.getElementById('save-button').classList.remove('hide') 
                        console.log('this is the response')
                        document.getElementById('download').href = this.response
                        
                    }
                    
                }
                
                
        }

        }
        request.responseType = "";
        var file = input.files[0];
        var fileTypeOut = document.getElementById('file_out').value
        data.append('file', file);
        data.append('file_out', fileTypeOut)
        request.open('post', url);
        request.send(data);

}
    else {
        document.getElementById('file_name').innerHTML = 'Please select a compatible file!'
        
    }
}

function remove_file() {
    var request = new XMLHttpRequest();
    var element = document.getElementById("file_box");
    element.classList.add("hide");
    document.getElementById('upload-button').classList.remove('hide')
    document.getElementById('download').classList.add('hide') 
    document.getElementById('save-button').classList.add('hide') 

    request.open('get', 'http://localhost:5000/remove_file');
    request.send();
}

function delete_file() {

        var data = new FormData();
        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var id = document.getElementById('delete_file').value
                document.getElementById(id).remove();
                console.log('should appear here')
                console.log(this.response)
                }   
        }
        request.responseType = "";
        var filename = document.getElementById('filename').innerHTML
        var image_id = document.getElementById('delete_file').value
        console.log(filename)
        data.append('image_name', filename);
        data.append('image_id', image_id)
        
        request.open('post', 'http://localhost:5000/delete_file');
        request.send(data);
    }