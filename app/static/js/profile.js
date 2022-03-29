function loadUpload() { document.getElementById('upload').click() }

function show(){
    document.getElementById('image').classList.add('d-none')
    if(document.getElementById('upload').files.length == 0){
        document.getElementById('preview').classList.add('d-none')
        document.getElementById('add').classList.remove('d-none')
    }
    else{
        document.getElementById('preview').classList.remove('d-none')
        document.getElementById('add').classList.add('d-none')
    }

    document.getElementsByClassName('show')[0].classList.add('d-none')
    document.getElementsByClassName('show')[1].classList.remove('d-none')

    document.getElementsByClassName('fa-pen')[0].classList.add('d-none')
    document.getElementsByClassName('fa-times')[0].classList.remove('d-none')
}

function hide(){
    document.getElementById('image').classList.remove('d-none')
    document.getElementById('add').classList.add('d-none')
    document.getElementById('preview').classList.add('d-none')

    document.getElementsByClassName('show')[0].classList.remove('d-none')
    document.getElementsByClassName('show')[1].classList.add('d-none')

    document.getElementsByClassName('fa-pen')[0].classList.remove('d-none')
    document.getElementsByClassName('fa-times')[0].classList.add('d-none')
}

function showImage(){
    document.getElementById('preview').lastElementChild.src = URL.createObjectURL(document.getElementById('upload').files[0])

    document.getElementById('preview').classList.remove('d-none')
    document.getElementById('add').classList.add('d-none')
}